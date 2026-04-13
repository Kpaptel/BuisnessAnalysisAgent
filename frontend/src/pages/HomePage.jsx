import { useState } from "react";
import FileUpload from "../components/FileUpload.jsx";
import ResultsDashboard from "../components/ResultsDashboard.jsx";
import ComparisonTable from "../components/ComparisonTable.jsx";
import InsightsPanel from "../components/InsightsPanel.jsx";
import { uploadCsv, analyzeFile, compareFiles } from "../services/api.js";

export default function HomePage() {
  const [files, setFiles] = useState([]);
  const [uploaded, setUploaded] = useState([]);
  const [busy, setBusy] = useState(false);
  const [globalError, setGlobalError] = useState("");
  const [analyzeResult, setAnalyzeResult] = useState(null);
  const [analyzeError, setAnalyzeError] = useState("");
  const [comparison, setComparison] = useState(null);
  const [compareError, setCompareError] = useState("");

  async function handleUploadAndAnalyze() {
    setGlobalError("");
    setAnalyzeError("");
    setCompareError("");
    setAnalyzeResult(null);
    setComparison(null);
    if (!files.length) {
      setGlobalError("Choose at least one CSV file.");
      return;
    }
    setBusy(true);
    try {
      const results = [];
      for (const f of files) {
        const r = await uploadCsv(f);
        results.push(r);
      }
      setUploaded(results);
      if (results[0]) {
        const a = await analyzeFile(results[0].file_id);
        setAnalyzeResult(a);
      }
      if (results.length >= 2) {
        const ids = results.map((r) => r.file_id);
        const c = await compareFiles(ids);
        setComparison(c);
      }
    } catch (e) {
      const msg = e.response?.data?.detail;
      const detail =
        typeof msg === "string"
          ? msg
          : Array.isArray(msg)
            ? msg.map((x) => x.msg || JSON.stringify(x)).join("; ")
            : e.message;
      setGlobalError(detail || "Request failed");
    } finally {
      setBusy(false);
    }
  }

  const lastMetrics = analyzeResult?.metrics || null;

  return (
    <div style={{ maxWidth: 900, margin: "0 auto", padding: "1.25rem" }}>
      <header style={{ marginBottom: "1.25rem" }}>
        <h1>Deal Intelligence Assistant</h1>
        <p style={{ margin: 0, color: "#475569", fontSize: "0.95rem" }}>
          Upload financial CSVs, view metrics, compare deals, and optionally generate AI explanations.
        </p>
      </header>

      {globalError && (
        <div className="card">
          <p className="error" style={{ margin: 0 }}>
            {globalError}
          </p>
        </div>
      )}

      <FileUpload files={files} onFilesChange={setFiles} disabled={busy} />

      <div className="card" style={{ display: "flex", gap: "0.75rem", flexWrap: "wrap", alignItems: "center" }}>
        <button type="button" disabled={busy || !files.length} onClick={handleUploadAndAnalyze}>
          {busy ? "Working…" : "Upload & analyze"}
        </button>
        {uploaded.length > 0 && (
          <span style={{ fontSize: "0.9rem", color: "#64748b" }}>
            {uploaded.length} file(s) on server — IDs ready for compare.
          </span>
        )}
      </div>

      <ResultsDashboard analyzeResult={analyzeResult} error={analyzeError} />
      <ComparisonTable comparison={comparison} error={compareError} />
      <InsightsPanel metrics={lastMetrics} />
    </div>
  );
}
