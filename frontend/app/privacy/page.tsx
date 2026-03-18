export default function Privacy() {
  return (
    <div style={{ maxWidth: "800px", margin: "0 auto", padding: "2rem 16px" }}>
        <h1 style={{ fontSize: "2.5rem", marginBottom: "2rem" }}>Privacy Policy</h1>
        
        <div style={{ color: "var(--muted)", lineHeight: 1.6 }}>
            <p style={{ marginBottom: "1.5rem" }}>
                At IONIS Healthcare Analytics, we prioritize the confidentiality and security of medical and demographic data. This privacy policy applies to the Autism Screening Application available via this domain.
            </p>
            
            <h3 style={{ fontSize: "1.25rem", color: "var(--text)", marginTop: "2rem", marginBottom: "1rem" }}>1. In-Memory Data Processing</h3>
            <p style={{ marginBottom: "1.5rem" }}>
                All inputs submitted through the screening form are transferred securely over HTTPS to our backend APIs. Data is processed strictly <strong>in-memory</strong>. We do not write patient variables to a persistent database or third-party logging server.
            </p>

            <h3 style={{ fontSize: "1.25rem", color: "var(--text)", marginTop: "2rem", marginBottom: "1rem" }}>2. Analytics & Logging</h3>
            <p style={{ marginBottom: "1.5rem" }}>
                We collect anonymous application logs to monitor system health and rate-limit API abuse. These logs contain metadata such as timestamps, model response codes, and anonymized identifiers. No Personally Identifiable Information (PII) is recorded.
            </p>

            <h3 style={{ fontSize: "1.25rem", color: "var(--text)", marginTop: "2rem", marginBottom: "1rem" }}>3. Compliance Statement</h3>
            <p style={{ marginBottom: "1.5rem" }}>
                This prototype is designed to comply with standard healthcare data-minimization practices. However, users are strictly advised that this tool provides <strong>decision support</strong>, NOT clinical diagnosis.
            </p>
        </div>
    </div>
  );
}
