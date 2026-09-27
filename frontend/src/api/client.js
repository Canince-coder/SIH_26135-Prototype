import axios from "axios";

export const BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000";

const client = axios.create({ baseURL: BASE_URL });

client.interceptors.request.use((config) => {
  const token = localStorage.getItem("sb_token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

client.interceptors.response.use(
  (response) => response,
  (error) => {
    const status = error.response?.status;
    if (status === 401) {
      localStorage.removeItem("sb_token");
      localStorage.removeItem("sb_user");
      if (!window.location.pathname.startsWith("/login")) {
        window.location.href = "/login?expired=1";
      }
    }
    const detail =
      error.response?.data?.detail ||
      error.response?.data?.message ||
      error.message ||
      "Something went wrong. Please try again.";
    return Promise.reject({ status, detail, raw: error });
  }
);

export default client;
