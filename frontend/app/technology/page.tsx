import { Cpu, Network, Zap } from 'lucide-react';

export default function Technology() {
  return (
    <div style={{ maxWidth: "800px", margin: "0 auto", padding: "2rem 16px" }}>
        <h1 style={{ fontSize: "2.5rem", marginBottom: "1.5rem" }}>Under the Hood</h1>
        <p style={{ fontSize: "1.1rem", color: "var(--muted)", marginBottom: "3rem" }}>
            The screening tool leverages three industry-standard machine learning paradigms, all serialized via Scikit-Learn pipelines.
        </p>
        
        <div style={{ display: "flex", flexDirection: "column", gap: "2rem" }}>
            <div style={{ background: "var(--panel)", padding: "2rem", borderRadius: "12px", border: "1px solid #38bdf8", position: "relative", overflow: "hidden" }}>
                <div style={{ display: "flex", alignItems: "center", gap: "1rem", marginBottom: "1rem" }}>
                    <Network size={28} color="#38bdf8" />
                    <h2 style={{ margin: 0 }}>Logistic Regression</h2>
                </div>
                <p style={{ color: "var(--muted)", margin: 0, lineHeight: 1.6 }}>
                    Known for high interpretability, our LR model provides a strong linear baseline, plotting the log-odds of the target classification against our 36 validated boolean and ordinal features.
                </p>
            </div>

            <div style={{ background: "var(--panel)", padding: "2rem", borderRadius: "12px", border: "1px solid var(--border)" }}>
                <div style={{ display: "flex", alignItems: "center", gap: "1rem", marginBottom: "1rem" }}>
                    <Cpu size={28} color="#94a3b8" />
                    <h2 style={{ margin: 0 }}>Random Forest</h2>
                </div>
                <p style={{ color: "var(--muted)", margin: 0, lineHeight: 1.6 }}>
                    An ensemble learning method consisting of multiple decision trees. This model excels at capturing non-linear relationships and is highly robust against data outliers and feature noise.
                </p>
            </div>

            <div style={{ background: "var(--panel)", padding: "2rem", borderRadius: "12px", border: "1px solid var(--border)" }}>
                <div style={{ display: "flex", alignItems: "center", gap: "1rem", marginBottom: "1rem" }}>
                    <Zap size={28} color="#94a3b8" />
                    <h2 style={{ margin: 0 }}>XGBoost</h2>
                </div>
                <p style={{ color: "var(--muted)", margin: 0, lineHeight: 1.6 }}>
                    Extreme Gradient Boosting provides state-of-the-art predictive performance. By iteratively minimizing the loss function through gradient descent, it handles unbalanced clinical datasets with unparalleled accuracy.
                </p>
            </div>
        </div>
    </div>
  );
}
