import { Mail, Phone, MapPin } from 'lucide-react';

export default function Contact() {
  return (
    <div style={{ maxWidth: "800px", margin: "0 auto", padding: "2rem 16px" }}>
        <h1 style={{ fontSize: "2.5rem", marginBottom: "3rem", textAlign: "center" }}>Contact Our Team</h1>
        
        <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(200px, 1fr))", gap: "2rem", marginBottom: "4rem" }}>
            <div style={{ textAlign: "center", padding: "2rem", background: "var(--panel)", borderRadius: "12px", border: "1px solid var(--border)" }}>
                <Mail size={32} color="#38bdf8" style={{ margin: "0 auto 1rem" }} />
                <h3 style={{ margin: "0 0 0.5rem" }}>Email Support</h3>
                <p style={{ color: "var(--muted)", margin: 0 }}>support@ionis-medical.com</p>
            </div>
            
            <div style={{ textAlign: "center", padding: "2rem", background: "var(--panel)", borderRadius: "12px", border: "1px solid var(--border)" }}>
                <Phone size={32} color="#38bdf8" style={{ margin: "0 auto 1rem" }} />
                <h3 style={{ margin: "0 0 0.5rem" }}>Phone Inquiries</h3>
                <p style={{ color: "var(--muted)", margin: 0 }}>+1 (800) 555-0199</p>
            </div>

            <div style={{ textAlign: "center", padding: "2rem", background: "var(--panel)", borderRadius: "12px", border: "1px solid var(--border)" }}>
                <MapPin size={32} color="#38bdf8" style={{ margin: "0 auto 1rem" }} />
                <h3 style={{ margin: "0 0 0.5rem" }}>Headquarters</h3>
                <p style={{ color: "var(--muted)", margin: 0 }}>123 HealthTech Way,<br/>San Francisco, CA</p>
            </div>
        </div>
    </div>
  );
}
