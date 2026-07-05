import { useState } from "react";
import { downloadFile, processFile, uploadFile } from "../services/api";

export default function UploadForm({
  file,
  uploadedFile,
  outputFile,
  onUploadSuccess,
  onProcessSuccess,
  onDownloadSuccess,
  onStatusChange,
}) {
  const [loading, setLoading] = useState(false);

  const handleUpload = async () => {
    if (!file) {
      onStatusChange?.("Upload needed", "Please choose a file first.");
      return;
    }

    try {
      setLoading(true);
      const result = await uploadFile(file);
      onUploadSuccess?.(result.filename || "", result.message || "Upload successful");
    } catch (error) {
      console.error(error);
      onStatusChange?.("Upload failed", "Upload failed");
    } finally {
      setLoading(false);
    }
  };

  const handleProcess = async () => {
    if (!uploadedFile) {
      onStatusChange?.("Process needed", "Upload a file before processing.");
      return;
    }

    try {
      setLoading(true);
      const result = await processFile(uploadedFile);
      const downloadedName = result.download || result.result?.output || "";
      onProcessSuccess?.(downloadedName, result.message || "Processing complete");
    } catch (error) {
      console.error(error);
      onStatusChange?.("Processing failed", "Processing failed");
    } finally {
      setLoading(false);
    }
  };

  const handleDownload = () => {
    if (!outputFile) {
      onStatusChange?.("Download needed", "Process a file before downloading.");
      return;
    }

    downloadFile(outputFile);
    onDownloadSuccess?.(`Downloading ${outputFile}`);
  };

  return (
    <div className="space-y-4">
      <button
        className="w-full rounded-xl bg-blue-600 px-4 py-3 font-semibold text-white transition hover:bg-blue-700 disabled:cursor-not-allowed disabled:opacity-70"
        onClick={handleUpload}
        disabled={loading}
      >
        {loading ? "Working..." : "Upload"}
      </button>

      <button
        className="w-full rounded-xl bg-green-600 px-4 py-3 font-semibold text-white transition hover:bg-green-700 disabled:cursor-not-allowed disabled:opacity-70"
        onClick={handleProcess}
        disabled={!uploadedFile || loading}
      >
        Process
      </button>

      <button
        className="w-full rounded-xl bg-purple-600 px-4 py-3 font-semibold text-white transition hover:bg-purple-700 disabled:cursor-not-allowed disabled:opacity-70"
        onClick={handleDownload}
        disabled={!outputFile}
      >
        Download
      </button>
    </div>
  );
}