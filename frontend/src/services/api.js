import axios from "axios";

const client = axios.create({
  baseURL: import.meta.env.VITE_API_URL || "",
  headers: { Accept: "application/json" },
});

export async function uploadCsv(file) {
  const form = new FormData();
  form.append("file", file);
  const { data } = await client.post("/upload", form, {
    headers: { "Content-Type": "multipart/form-data" },
  });
  return data;
}

export async function analyzeFile(fileId) {
  const { data } = await client.post("/analyze", { file_id: fileId });
  return data;
}

export async function compareFiles(fileIds) {
  const { data } = await client.post("/compare", { file_ids: fileIds });
  return data;
}

export async function fetchInsights(metrics, context) {
  const { data } = await client.post("/insights", { metrics, context: context || null });
  return data;
}
