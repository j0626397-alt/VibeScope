import axios from "axios";

const BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api";

export const api = axios.create({
  baseURL: BASE_URL,
  timeout: 120000, // 2 min — ML inference can be slow
  headers: {
    "Content-Type": "application/json",
  },
});

export async function analyzeQuery(query) {
  const { data } = await api.post("/analyze", { query });
  return data;
}

export async function getPosts(query, platform, sentiment) {
  const params = { query };
  if (platform) params.platform = platform;
  if (sentiment) params.sentiment = sentiment;
  const { data } = await api.get("/posts", { params });
  return data;
}

export async function getHistory() {
  const { data } = await api.get("/history");
  return data;
}
