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
    "feature_names": None
}

MODEL_FILES = {
    "lr": os.path.join(MODELS_DIR, "logistic_regression_model.pkl"),
    "rf": os.path.join(MODELS_DIR, "random_forest_model.pkl"),
    "xgb": os.path.join(MODELS_DIR, "xgboost_model.pkl"),
}

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load features
    FEATURES_PATH = os.path.join(MODELS_DIR, "feature_names.joblib")
    if os.path.exists(FEATURES_PATH):
        ml_resources["feature_names"] = joblib.load(FEATURES_PATH)
        logger.info(f"Loaded {len(ml_resources['feature_names'])} feature names.")
    else:
        logger.warning(f"'{FEATURES_PATH}' not found.")
        
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
        # Verify that all 3 required models are loaded
        for required_model in ["lr", "rf", "xgb"]:
            if required_model not in ml_resources["models"]:
                raise HTTPException(status_code=500, detail=f"Required model '{required_model}' is not loaded.")
            
        feature_names = ml_resources.get("feature_names")
        if not feature_names:
             raise HTTPException(status_code=500, detail="Feature names are not loaded.")

        # Extract values in the exact training order using the Pydantic model dump with aliases
        features_dict = payload.features.model_dump(by_alias=True)
        
        input_list = []
        for feat in feature_names:
            val = features_dict.get(feat, 0.0)
            input_list.append(val)
        
        # Use DataFrame to preserve column names (required by some models, e.g. XGBoost, Pipelines)
        X_input = pd.DataFrame([input_list], columns=feature_names)
        
        # Ensemble Prediction
        predictions = []
        probabilities = {0: 0.0, 1: 0.0}
        
        for model_id in ["lr", "rf", "xgb"]:
            model = ml_resources["models"][model_id]
            pred = int(model.predict(X_input)[0])
            prob = model.predict_proba(X_input)[0].tolist()
            
            predictions.append(pred)
            probabilities[0] += prob[0]
            probabilities[1] += prob[1]
            
        # Majority voting
        majority_vote = 1 if sum(predictions) >= 2 else 0
        avg_prob_0 = probabilities[0] / 3
        avg_prob_1 = probabilities[1] / 3
        
        recommendation_text = "after consulting with 3 different solid computer programs (machine learning models) we are confident that this subject must see a specialist (think of this as your second and third opinion)" if majority_vote == 1 else "No immediate referral indicated"
        
        return PredictionResponse(
            prediction=majority_vote,
            Recommendation=recommendation_text,
            model_used="Ensemble (Majority Vote)",
            probability={
                "0": round(avg_prob_0, 4),
                "1": round(avg_prob_1, 4)
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
