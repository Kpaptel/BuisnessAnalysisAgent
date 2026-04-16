export default function FileUpload({ files, onFilesChange, disabled }) {
  return (
    <div className="card">
      <div className="card-header">
        <h2>Upload CSV files</h2>
      </div>
      <p className="card-meta">
        Select one or more financial CSVs (revenue and expenses columns required; asking price optional for ROI).
      </p>
      <input
        className="file-input"
        type="file"
        accept=".csv"
        multiple
        disabled={disabled}
        onChange={(e) => onFilesChange(e.target.files ? Array.from(e.target.files) : [])}
      />
      {files.length > 0 && (
        <ul className="file-list">
          {files.map((f) => (
            <li key={f.name + f.size}>{f.name}</li>
          ))}
        </ul>
      )}
    </div>
  );
}
