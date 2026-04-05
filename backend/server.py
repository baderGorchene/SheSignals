from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Request, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
import joblib
import numpy as np
import pandas as pd
import os
import logging

# Configure production-ready structured logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger("autism_api")

from schemas import PredictionRequest, PredictionResponse

# Resolve paths relative to this file's directory (not CWD)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODELS_DIR = os.path.join(BASE_DIR, "models")

# Global variables to hold the loaded models and features
ml_resources = {
    "models": {},
    "raw_feature_names": None,   # 36 original features (used by RF)
    "xgb_feature_names": None,  # 46 engineered features (used by XGBoost)
    "xgb_threshold": 0.5,       # optimal decision threshold for XGBoost
}

MODEL_FILES = {
    "xgb": os.path.join(MODELS_DIR, "xgboost_model.pkl"),
}


def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    """Must mirror train_optimized_xgboost.py exactly."""
    d = df.copy()
    social_cols = [
        "Appears comfortable in social settings (e.g., classrooms, birthday parties)",
        "Prefers spending time with close friend(s) over group of people with group activities",
        "Seems emotionally or physically exhausted after socializing",
        "Confidently initiates conversations",
        "Appears anxious or withdrawn in unfamiliar social settings",
        "Feels overwhelmed by the need to communicate in social situations?",
    ]
    communication_cols = [
        "Struggles to read facial expressions, tone, or body language",
        "Frequently feels misunderstood during conversations",
        "Becomes upset or frustrated when misunderstood",
        "Struggles to express emotions with words",
        "Rehearses or plans their conversations (phrases, always greet Good Morning/Evening, etc.) in advance",
        "Fnds it difficult to follow multiple conversations happening at once (e.g., in a group setting)?",
    ]
    sensory_cols = [
        "Sensitive to loud noises and/or bright lights or visual clutter",
        "Avoids certain fabrics or textures due to discomfort",
        "Affected by strong smells that others seem to tolerate",
        "Appears overwhelmed in crowded or noisy environments",
    ]
    emotional_cols = [
        "Finds it difficult to calm down after becoming upset or stressed",
        "Finds it difficult to manage emotions during stressful interactions",
        "Internalizes anxiety or stress without showing it",
        "Demonstrates strong emotional reactions in intense situations (e.g., anger, crying, withdrawal)",
    ]
    masking_cols = [
        "Monitors others' reactions to her actions to get a validation that she is acting appropriately",
        "Mimics others' behavior to fit in",
        "Avoids or struggles to maintain eye contact",
    ]
    routine_cols = [
        "Demonstrates ritualized patterns of verbal or nonverbal behavior with extreme distress at small changes (Prefers routines in daily life)",
        "Feels overwhelmed / stressed when something changes on them at the last minute or gets upset when others do not follow through on plans/promises made",
        "Uses the same phrases or greetings in different situations",
    ]

    def safe_sum(cols):
        valid = [c for c in cols if c in df.columns]
        return df[valid].sum(axis=1) if valid else pd.Series(0, index=df.index)

    d["feat_social_score"]        = safe_sum(social_cols)
    d["feat_communication_score"] = safe_sum(communication_cols)
    d["feat_sensory_score"]       = safe_sum(sensory_cols)
    d["feat_emotional_score"]     = safe_sum(emotional_cols)
    d["feat_masking_score"]       = safe_sum(masking_cols)
    d["feat_routine_score"]       = safe_sum(routine_cols)
    d["feat_total_score"]         = (
        d["feat_social_score"] + d["feat_communication_score"] +
        d["feat_sensory_score"] + d["feat_emotional_score"] +
        d["feat_masking_score"] + d["feat_routine_score"]
    )

    walk_col  = "At what age did your child first start to walk?"
    speak_col = "At what age did your child first start to speak in full words or phrases?"
    if walk_col in df.columns and speak_col in df.columns:
        d["feat_dev_delay_interaction"] = df[walk_col] * df[speak_col]
        d["feat_dev_delay_sum"]         = df[walk_col] + df[speak_col]

    fh_col = "Is there a family history of autism or related neurodevelopmental conditions?"
    if fh_col in df.columns:
        d["feat_family_x_symptoms"] = df[fh_col] * d["feat_total_score"]

    return d

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load XGBoost feature names (46 — includes engineered features)
    XGB_FEATURES_PATH = os.path.join(MODELS_DIR, "feature_names.joblib")
    if os.path.exists(XGB_FEATURES_PATH):
        ml_resources["xgb_feature_names"] = joblib.load(XGB_FEATURES_PATH)
        logger.info(f"Loaded {len(ml_resources['xgb_feature_names'])} XGBoost feature names.")
    else:
        logger.warning(f"'{XGB_FEATURES_PATH}' not found.")

    # Derive raw feature names (original 36 schema fields — needed to build engineered features)
    if ml_resources["xgb_feature_names"]:
        ml_resources["raw_feature_names"] = [
            f for f in ml_resources["xgb_feature_names"] if not f.startswith("feat_")
        ]
        logger.info(f"Raw feature names: {len(ml_resources['raw_feature_names'])}")

    # Load optimal XGBoost decision threshold
    THRESHOLD_PATH = os.path.join(MODELS_DIR, "xgb_threshold.joblib")
    if os.path.exists(THRESHOLD_PATH):
        ml_resources["xgb_threshold"] = float(joblib.load(THRESHOLD_PATH))
        logger.info(f"XGBoost decision threshold: {ml_resources['xgb_threshold']:.4f}")
    else:
        logger.warning("xgb_threshold.joblib not found — using default 0.5")

    # Load models
    for model_key, filename in MODEL_FILES.items():
        if os.path.exists(filename):
            logger.info(f"Loading {model_key.upper()} model from {filename}...")
            ml_resources["models"][model_key] = joblib.load(filename)
        else:
            logger.warning(f"Model file '{filename}' not found.")

    yield
    # Clean up on shutdown
    ml_resources.clear()

limiter = Limiter(key_func=get_remote_address)
app = FastAPI(title="Autism Screening API", lifespan=lifespan)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Custom exception handler for generic Server Errors
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "An internal server error occurred."},
    )

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
@limiter.limit("50/minute")
def read_root(request: Request):
    return {"message": "Autism Screening API is running"}

@app.get("/health")
@limiter.limit("50/minute")
def health_check(request: Request):
    """Returns service status and loaded model names."""
    loaded_models = list(ml_resources.get("models", {}).keys())
    return {
        "status": "ok",
        "loaded_models": loaded_models,
        "feature_names_loaded": ml_resources.get("feature_names") is not None
    }

@app.post("/v1/predict", response_model=PredictionResponse)
@limiter.limit("20/minute")
def predict(request: Request, payload: PredictionRequest):
    try:
        # Verify XGBoost is loaded
        if "xgb" not in ml_resources["models"]:
            raise HTTPException(status_code=500, detail="XGBoost model is not loaded.")

        raw_feature_names = ml_resources.get("raw_feature_names")
        xgb_feature_names = ml_resources.get("xgb_feature_names")
        if not raw_feature_names or not xgb_feature_names:
            raise HTTPException(status_code=500, detail="Feature names are not loaded.")

        # Build raw 36-feature DataFrame from the request payload
        features_dict = payload.features.model_dump(by_alias=True)
        raw_input = pd.DataFrame(
            [[features_dict.get(f, 0.0) for f in raw_feature_names]],
            columns=raw_feature_names
        )

        # Apply feature engineering → 46 features
        xgb_input = engineer_features(raw_input)[xgb_feature_names]

        # XGBoost prediction with tuned threshold
        xgb_model     = ml_resources["models"]["xgb"]
        xgb_threshold = ml_resources["xgb_threshold"]
        xgb_prob      = xgb_model.predict_proba(xgb_input)[0].tolist()
        prediction    = int(xgb_prob[1] >= xgb_threshold)

        recommendation_text = (
            "after an in-depth analysis by our AI, "
            "we are confident that this subject must see a specialist "
            "(think of this as your second and third opinion)"
            if prediction == 1 else "No immediate referral indicated"
        )

        return PredictionResponse(
            prediction=prediction,
            Recommendation=recommendation_text,
            model_used="XGBoost (Optimized)",
            probability={
                "0": round(xgb_prob[0], 4),
                "1": round(xgb_prob[1], 4)
            }
        )
    except HTTPException as e:
        logger.warning(f"Client error ({e.status_code}): {e.detail}")
        raise
    except Exception as e:
        logger.error(f"Prediction error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Error during prediction processing.")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
