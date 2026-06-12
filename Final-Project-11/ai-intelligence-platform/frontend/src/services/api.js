const FALLBACK_API_BASE_URL = "http://127.0.0.1:8000";
const API_BASE_URL = (
  import.meta.env.VITE_API_BASE_URL || FALLBACK_API_BASE_URL
).replace(/\/$/, "");

async function request(path, options = {}) {
  const response = await fetch(`${API_BASE_URL}${path}`, options);

  let data = null;
  const text = await response.text();
  if (text) {
    try {
      data = JSON.parse(text);
    } catch {
      data = text;
    }
  }

  if (!response.ok) {
    const message =
      typeof data === "object" && data?.detail
        ? data.detail
        : text || "Request failed";
    throw new Error(message);
  }

  return data;
}

const api = {
  get(path) {
    return request(path);
  },

  post(path, body, headers) {
    return request(path, {
      method: "POST",
      body,
      headers,
    });
  },

  delete(path) {
    return request(path, {
      method: "DELETE",
    });
  },

  stream(path, body) {
    return fetch(`${API_BASE_URL}${path}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });
  },
};


export default api;
