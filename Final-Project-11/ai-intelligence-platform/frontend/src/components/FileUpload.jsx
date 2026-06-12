import { useState } from "react";
import api from "../services/api";

function FileUpload({ files, onUploadComplete, onDeleteFile }) {
  const [file, setFile] = useState(null);
  const [status, setStatus] = useState("");
  const [isUploading, setIsUploading] = useState(false);
  const [isDragging, setIsDragging] = useState(false);

  const uploadFile = async (selectedFile) => {
    const fileToUpload = selectedFile || file;
    if (!fileToUpload) {
      setStatus("Choose a file first.");
      return;
    }

    setIsUploading(true);
    setStatus("Uploading and indexing file...");

    try {
      const formData = new FormData();
      formData.append("file", fileToUpload);

      const response = await api.post("/api/upload", formData);
      setStatus(
        `"${response.filename}" successfully uploaded. Indexed ${response.chunks} chunks.`
      );
      setFile(null);
      onUploadComplete?.(response);
    } catch (error) {
      setStatus(`Upload failed: ${error.message}`);
    } finally {
      setIsUploading(false);
    }
  };

  const handleDragOver = (e) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = (e) => {
    e.preventDefault();
    setIsDragging(false);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setIsDragging(false);
    const droppedFile = e.dataTransfer.files?.[0];
    if (droppedFile) {
      setFile(droppedFile);
      uploadFile(droppedFile);
    }
  };

  const formatSize = (bytes) => {
    if (bytes === 0) return "0 Bytes";
    const k = 1024;
    const sizes = ["Bytes", "KB", "MB"];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + " " + sizes[i];
  };

  return (
    <section className="panel upload-panel">
      <div className="panel-heading">
        <p className="eyebrow">📂 Knowledge Base</p>
        <h2>Project Files</h2>
      </div>

      <p className="panel-copy" style={{ fontSize: "0.85rem", marginBottom: "16px" }}>
        Add `.txt`, `.csv`, or `.pdf` files. The assistant retrieves and grounds answers in their contents.
      </p>

      <div
        className={`upload-zone ${isDragging ? "dragging" : ""}`}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        onClick={() => document.getElementById("file-input").click()}
      >
        <span className="upload-icon">📥</span>
        <p>
          <span className="highlight">Click to browse</span> or drag & drop here
        </p>
        <p style={{ fontSize: "0.72rem", color: "var(--text-muted)" }}>
          {file ? `Selected: ${file.name}` : "Supports TXT, CSV, PDF"}
        </p>
        <input
          id="file-input"
          type="file"
          accept=".txt,.csv,.pdf"
          onChange={(event) => {
            const selected = event.target.files?.[0] ?? null;
            setFile(selected);
            if (selected) {
              uploadFile(selected);
            }
          }}
        />
      </div>

      {status && <div className="upload-status">ℹ️ {status}</div>}

      <div className="uploaded-files-list">
        <h4 style={{ fontSize: "0.85rem", color: "var(--text-secondary)", marginTop: "14px", borderBottom: "1px solid rgba(255,255,255,0.05)", paddingBottom: "6px" }}>
          Ingested Documents ({files.length})
        </h4>
        {files.length === 0 ? (
          <p className="muted" style={{ fontSize: "0.78rem", padding: "10px 0" }}>No documents uploaded yet.</p>
        ) : (
          files.map((f, i) => (
            <div key={`${f.filename}-${i}`} className="file-item">
              <div className="file-info">
                <span className="file-name" title={f.filename}>{f.filename}</span>
                <span className="file-size">{formatSize(f.size)}</span>
              </div>
              <button
                type="button"
                className="trash-button"
                title="Delete file & clear indices"
                onClick={() => onDeleteFile(f.filename)}
              >
                🗑️
              </button>
            </div>
          ))
        )}
      </div>
    </section>
  );
}

export default FileUpload;
