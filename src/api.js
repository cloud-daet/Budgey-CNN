// Talks to the Budgey backend (FastAPI). The backend is stateless: it never
// stores photos or embeddings, so the app keeps those in the browser/device.
const API_URL = import.meta.env.VITE_API_URL ?? "http://localhost:8000";

async function request(path, options) {
  const res = await fetch(`${API_URL}${path}`, options);
  if (!res.ok) {
    throw new Error(`Backend ${path} failed (${res.status})`);
  }
  return res.json();
}

// Send a photo (data URL from the camera) and get its CNN embedding back.
// Returns { embedding, dim, model }.
export async function embedPhoto(dataUrl) {
  const blob = await (await fetch(dataUrl)).blob();
  const form = new FormData();
  form.append("file", blob, "photo.jpg");
  return request("/v1/embed", { method: "POST", body: form });
}

// Compare an embedding with stored ones: candidates = [{ id, embedding }].
// Returns { matched, matches: [{ id, score }], threshold }.
export function matchEmbedding(embedding, candidates, { topK = 3 } = {}) {
  return request("/v1/match", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ embedding, candidates, top_k: topK }),
  });
}
