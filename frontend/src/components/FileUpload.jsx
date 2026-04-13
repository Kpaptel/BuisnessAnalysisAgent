export default function FileUpload({ files, onFilesChange, disabled }) {
  return (
    <div className="card">
      <h2>Upload CSV files</h2>
      <p style={{ margin: "0 0 0.75rem", fontSize: "0.9rem", color: "#475569" }}>
        Select one or more financial CSVs (revenue and expenses columns required; asking price optional for ROI).
      </p>
      <input
        type="file"
        accept=".csv"
        multiple
        disabled={disabled}
        onChange={(e) => onFilesChange(e.target.files ? Array.from(e.target.files) : [])}
      />
      {files.length > 0 && (
        <ul style={{ margin: "0.75rem 0 0", paddingLeft: "1.25rem", fontSize: "0.9rem" }}>
          {files.map((f) => (
            <li key={f.name + f.size}>{f.name}</li>
          ))}
        </ul>
      )}
    </div>
  );
}
