function DealRow({ deal, highlightName }) {
  const isBest = deal.filename === highlightName;
  return (
    <tr style={isBest ? { background: "#f0fdf4" } : undefined}>
      <td>{deal.filename}</td>
      <td>{deal.net_profit}</td>
      <td>{deal.profit_margin_percent}%</td>
      <td>{deal.roi_percent != null ? `${deal.roi_percent}%` : "—"}</td>
      <td>{deal.total_revenue}</td>
    </tr>
  );
}

export default function ComparisonTable({ comparison, error }) {
  if (error) {
    return (
      <div className="card">
        <h2>Comparison</h2>
        <p className="error">{error}</p>
      </div>
    );
  }
  if (!comparison || !comparison.deals?.length) {
    return (
      <div className="card">
        <h2>Comparison</h2>
        <p style={{ margin: 0, color: "#64748b" }}>Compare two or more uploaded files to see rankings.</p>
      </div>
    );
  }

  const deals = comparison.deals;
  const bestName = comparison.best_deal?.filename;

  return (
    <div className="card">
      <h2>Comparison</h2>
      <table>
        <thead>
          <tr>
            <th>Deal</th>
            <th>Net profit</th>
            <th>Margin</th>
            <th>ROI</th>
            <th>Revenue</th>
          </tr>
        </thead>
        <tbody>
          {deals.map((d) => (
            <DealRow key={d.file_id} deal={d} highlightName={bestName} />
          ))}
        </tbody>
      </table>
      {comparison.best_deal && (
        <div className="best">
          <strong>Best deal recommendation:</strong> {comparison.best_deal.filename}
          <div style={{ fontSize: "0.9rem", marginTop: "0.35rem" }}>
            {comparison.best_deal.recommendation_reason}
          </div>
        </div>
      )}
    </div>
  );
}
