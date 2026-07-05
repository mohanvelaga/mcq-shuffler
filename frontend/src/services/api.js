const API_BASE_URL = "http://127.0.0.1:8000";

export async function uploadFile(file) {
  const formData = new FormData();
  formData.append("file", file);

  const response = await fetch(`${API_BASE_URL}/upload`, {
    method: "POST",
    body: formData,
  });

  if (!response.ok) {
    throw new Error("Upload failed");
  }

  return response.json();
}

export async function processFile(filename) {
  const response = await fetch(`${API_BASE_URL}/process`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ filename }),
  });

  if (!response.ok) {
    throw new Error("Processing failed");
  }

  return response.json();
}

export function downloadFile(filename) {
  window.open(`${API_BASE_URL}/download/${filename}`, "_blank", "noopener,noreferrer");
}
