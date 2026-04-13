import { useState } from "react";
import { fetchInsights } from "../services/api";

export default function InsightsPanel({ metrics }) {
  const [context, setContext] = useState("");
  const [text, setText] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function run() {
    if (!metrics) {
      setError("Analyze a file first to load metrics for insights.");
      return;
    }
    setLoading(true);
    setError("");
    try {
      const res = await fetchInsights(metrics, context);
      setText(res.text || "");
    } catch (e) {
      setError(e.response?.data?.detail || e.message || "Request failed");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="card">
      <h2>AI insights (optional)</h2>
      <p style={{ margin: "0 0 0.5rem", fontSize: "0.9rem", color: "#475569" }}>
        Uses OpenAI when <code>OPENAI_API_KEY</code> is set on the server; otherwise returns a placeholder summary.
      </p>
      <textarea
        placeholder="Optional context for the model…"
        value={context}
        onChange={(e) => setContext(e.target.value)}
        disabled={loading}
      />
      <div style={{ marginTop: "0.75rem" }}>
        <button type="button" onClick={run} disabled={loading}>
          {loading ? "Generating…" : "Generate insights"}
        </button>
      </div>
      {error && <p className="error">{error}</p>}
      {text && (
        <pre
          style={{
            marginTop: "1rem",
            whiteSpace: "pre-wrap",
            fontSize: "0.9rem",
            background: "#f8fafc",
            padding: "0.75rem",
            borderRadius: 6,
            border: "1px solid #e2e8f0",
          }}
        >
          {text}
        </pre>
      )}
    </div>
  );
}
