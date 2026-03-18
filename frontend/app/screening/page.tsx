"use client";

import React, { useState } from "react";
import { FIELDS } from "../fields";

// 🔥 Dynamic API Base for seamless deployment (Vercel -> Render)
const API_BASE = process.env.NEXT_PUBLIC_API_BASE || "http://localhost:8001";

export default function Home() {
  const [output, setOutput] = useState<{ type: string; data?: any; message?: string } | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [selectedModel, setSelectedModel] = useState("lr");

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const formData = new FormData(e.currentTarget);
    const payload: Record<string, unknown> = {};

    let isValid = true;
    for (const f of FIELDS) {
      const val = formData.get(f.id);

      if (!val || val === "") {
        payload[f.question] = null;
        continue;
      }

      const numVal = Number(val);

      if (f.type === "number") {
        if (isNaN(numVal) || (f.min !== undefined && numVal < f.min) || (f.max !== undefined && numVal > f.max)) {
          alert(`Value out of range for: ${f.question}\nExpected ${f.min}–${f.max}`);
          const el = document.getElementById(f.id);
          el?.focus();
          isValid = false;
          break;
        }
      }

      payload[f.question] = numVal;
    }

    if (!isValid) return;

    setOutput({ type: "loading" });
    setIsSubmitting(true);

    try {
      const res = await fetch(`${API_BASE}/v1/predict`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ model: selectedModel, features: payload }),
      });

      if (!res.ok) {
        const data = await res.json().catch(() => ({}));
        
        if (res.status === 422) {
            throw new Error(data.detail ? JSON.stringify(data.detail) : "Invalid or missing input features.");
        }
        if (res.status === 429) {
            throw new Error("You have exceeded the rate limit. Please wait a moment and try again.");
        }
        
        throw new Error(data.detail || `API error ${res.status}`);
      }

      const result = await res.json();
      setOutput({ type: "success", data: result });
      
    } catch (err: unknown) {
      const errorMessage = err instanceof Error ? err.message : String(err);
      setOutput({ type: "error", message: errorMessage });
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleClear = () => {
    const form = document.getElementById("intakeForm") as HTMLFormElement;
    form.reset();
    setOutput(null);
  };

  return (
    <div className="wrap">
      <header>
        <h1>Autism Screening Model Integration</h1>
        <p className="sub">Fill out the clinical intake form below to request a prediction from the selected ML model.</p>
      </header>

      <form id="intakeForm" onSubmit={handleSubmit}>
        
        <div className="model-selector" style={{ marginBottom: "2rem", padding: "1rem", background: "#f8fafc", border: "1px solid #e2e8f0", borderRadius: "8px" }}>
            <label htmlFor="model-select" style={{ fontWeight: 600, display: "block", marginBottom: "0.5rem" }}>
              Prediction Model
            </label>
            <select
                id="model-select"
                value={selectedModel}
                onChange={(e) => setSelectedModel(e.target.value)}
                style={{ width: "100%", padding: "0.75rem", borderRadius: "4px", border: "1px solid #cbd5e1" }}
            >
                <option value="lr">Logistic Regression (High Interpretability)</option>
                <option value="rf">Random Forest (Robust to Outliers)</option>
                <option value="xgb">XGBoost (High Performance)</option>
            </select>
        </div>

        {FIELDS.map((f) => (
          <div className="row" key={f.id}>
            <div className="q">{f.question}</div>
            <div className="a">
              {f.type === "select" ? (
                <select id={f.id} name={f.id} required defaultValue="">
                  <option value="" disabled>Select…</option>
                  {f.options?.map((opt) => (
                    <option key={opt.value} value={opt.value}>
                      {opt.label}
                    </option>
                  ))}
                </select>
              ) : (
                <input
                  id={f.id}
                  name={f.id}
                  type="number"
                  min={f.min}
                  max={f.max}
                  step="1"
                  required
                />
              )}
              <div className="hint">{f.hint}</div>
            </div>
          </div>
        ))}

        <div className="actions">
          <button type="submit" disabled={isSubmitting}>
            {isSubmitting ? "Generating Prediction..." : "Run ML Inference"}
          </button>
          <button type="button" id="clearBtn" onClick={handleClear}>
            Clear Form
          </button>
        </div>
      </form>

      {output && (
        <div className="out" id="output" style={{ marginTop: "2rem" }}>
            {output.type === "loading" && (
                <div style={{ textAlign: "center", padding: "2rem", color: "#64748b" }}>
                    <div className="spinner"></div>
                    <p>Analyzing patient metrics...</p>
                </div>
            )}
            
            {output.type === "error" && (
                <div style={{ background: "#fef2f2", color: "#b91c1c", padding: "1.5rem", borderRadius: "8px", border: "1px solid #fca5a5" }}>
                    <h3 style={{ marginTop: 0 }}>Prediction Error</h3>
                    <p>{output.message}</p>
                </div>
            )}
            
            {output.type === "success" && output.data && (
                <div style={{
                    background: output.data.prediction === 1 ? "#fff1f2" : "#f0fdf4",
                    border: `1px solid ${output.data.prediction === 1 ? "#fda4af" : "#86efac"}`,
                    padding: "2rem",
                    borderRadius: "8px",
                    color: "#0f172a"
                }}>
                    <h2 style={{ fontSize: "1.5rem", marginTop: 0, color: output.data.prediction === 1 ? "#be123c" : "#15803d" }}>
                        {output.data.Recommendation}
                    </h2>
                    
                    <div style={{ display: "flex", gap: "2rem", marginTop: "1.5rem" }}>
                        <div>
                            <p style={{ margin: 0, fontSize: "0.875rem", color: "#64748b" }}>Model Used</p>
                            <p style={{ margin: "0.25rem 0 0", fontWeight: 600 }}>{output.data.model_used.toUpperCase()}</p>
                        </div>
                        <div>
                            <p style={{ margin: 0, fontSize: "0.875rem", color: "#64748b" }}>Confidence</p>
                            <p style={{ margin: "0.25rem 0 0", fontWeight: 600 }}>
                                {Math.round(output.data.probability[String(output.data.prediction)] * 100)}%
                            </p>
                        </div>
                    </div>
                </div>
            )}
        </div>
      )}
    </div>
  );
}
