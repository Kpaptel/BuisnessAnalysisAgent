export default function ResultsDashboard({ analyzeResult, error }) {
  if (error) {
    return (
      <div className="card">
        <h2>Single-file analysis</h2>
        <p className="error">{error}</p>
      </div>
    );
  }
  if (!analyzeResult) {
    return (
      <div className="card">
        <h2>Single-file analysis</h2>
        <p style={{ margin: 0, color: "#64748b" }}>Upload and analyze a file to see metrics.</p>
      </div>
    );
  }

  const m = analyzeResult.metrics || {};
  return (
    <div className="card">
      <h2>Single-file analysis</h2>
      <p style={{ margin: "0 0 0.75rem", fontSize: "0.9rem" }}>
        <strong>{analyzeResult.filename}</strong>
        <span style={{ color: "#64748b" }}> ({analyzeResult.file_id?.slice(0, 8)}…)</span>
      </p>
      <table>
        <tbody>
          <tr>
            <th>Total revenue</th>
            <td>{m.total_revenue}</td>
          </tr>
          <tr>
            <th>Total expenses</th>
            <td>{m.total_expenses}</td>
          </tr>
          <tr>
            <th>Net profit</th>
            <td>{m.net_profit}</td>
          </tr>
          <tr>
            <th>Profit margin</th>
            <td>{m.profit_margin_percent}%</td>
          </tr>
          <tr>
            <th>ROI</th>
            <td>{m.roi_percent != null ? `${m.roi_percent}%` : "N/A (no asking price)"}</td>
          </tr>
          {m.asking_price_used != null && (
            <tr>
              <th>Asking price used</th>
              <td>{m.asking_price_used}</td>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  );
}
