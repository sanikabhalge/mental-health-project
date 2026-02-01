const API_BASE = import.meta.env.VITE_API_URL || "http://localhost:8000";
const TOKEN_KEY = "mindcare_token";

export function getStoredToken() {
  return localStorage.getItem(TOKEN_KEY);
}

export function setStoredToken(token) {
  if (token) localStorage.setItem(TOKEN_KEY, token);
  else localStorage.removeItem(TOKEN_KEY);
}

export function getAuthHeaders() {
  const token = getStoredToken();
  return {
    "Content-Type": "application/json",
    ...(token ? { Authorization: `Bearer ${token}` } : {}),
  };
}

export async function login(username, password) {
  const res = await fetch(`${API_BASE}/api/auth/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username, password }),
  });
  const data = await res.json().catch(() => ({}));
  if (!res.ok) throw new Error(data.detail || data.error || "Login failed");
  if (data.access_token) setStoredToken(data.access_token);
  return data;
}

export async function register({ username, password, age, gender, emergencyContact, phoneNumber, address }) {
  const res = await fetch(`${API_BASE}/api/auth/register`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      username,
      password,
      age: age ? Number(age) : null,
      gender: gender || null,
      emergency_contact: emergencyContact || null,
      phone_number: phoneNumber || null,
      address: address || null,
    }),
  });
  const data = await res.json().catch(() => ({}));
  if (!res.ok) {
    const msg = Array.isArray(data.detail) ? data.detail.map((d) => d.msg).join(", ") : (data.detail || data.error || "Registration failed");
    throw new Error(msg);
  }
  if (data.access_token) setStoredToken(data.access_token);
  return data;
}

export function logout() {
  setStoredToken(null);
}
