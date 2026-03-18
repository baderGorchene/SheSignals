export default function About() {
  return (
    <div style={{ maxWidth: "800px", margin: "0 auto", padding: "2rem 16px" }}>
        <h1 style={{ fontSize: "2.5rem", marginBottom: "1.5rem" }}>About the Tool</h1>
        
        <div style={{ background: "var(--panel)", padding: "2.5rem", borderRadius: "12px", border: "1px solid var(--border)", lineHeight: 1.7, color: "var(--text)" }}>
            <p style={{ marginBottom: "1.5rem" }}>
                The IONIS Autism Screening Tool is a clinical prototype developed to assist healthcare professionals in evaluating and pre-screening patients at high risk for Autism Spectrum Disorder (ASD).
            </p>
            <p style={{ marginBottom: "1.5rem" }}>
                By mapping 36 distinct behavioral and demographic indicators through supervised machine learning models, this software provides immediate, data-driven "Refer" or "Do Not Refer" recommendations alongside a calculated confidence probability.
            </p>
            <h3 style={{ fontSize: "1.5rem", marginBottom: "1rem", color: "#38bdf8" }}>Our Mission</h3>
            <p style={{ margin: 0 }}>
                To reduce diagnostic bottlenecks by empowering front-line clinical staff with powerful, interpretable, and instantaneous artificial intelligence decision-support systems.
            </p>
        </div>
    </div>
  );
}
