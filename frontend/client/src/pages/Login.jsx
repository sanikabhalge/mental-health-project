import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { login } from "../api/auth";

function Login() {
  const navigate = useNavigate();
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleLogin = async (e) => {
    e.preventDefault();
    setError("");
    if (!username || !password) {
      setError("Please enter both username and password");
      return;
    }
    setLoading(true);
    try {
      await login(username, password);
      navigate("/chat");
    } catch (err) {
      setError(err.message || "Login failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-purple-200 via-pink-100 to-blue-100 animate-fadeIn">
      {/* Login Card */}
      <div className="bg-white rounded-3xl shadow-2xl p-10 w-96 flex flex-col items-center transform transition-all duration-700 hover:scale-105">
        
        {/* App Logo / Name */}
        <h1 className="text-5xl font-extrabold text-purple-700 mb-6 drop-shadow-lg animate-bounce">
          MindCare Bot
        </h1>

        {/* Login Form */}
        <form onSubmit={handleLogin} className="w-full flex flex-col gap-5">
          {error && (
            <p className="text-red-600 text-sm bg-red-50 px-3 py-2 rounded-lg">{error}</p>
          )}
          <input
            type="text"
            placeholder="Email or Username"
            className="p-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-purple-400 transition"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
          />

          <input
            type="password"
            placeholder="Password"
            className="p-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-purple-400 transition"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />

          <button
            type="submit"
            disabled={loading}
            className="bg-purple-600 text-white py-3 rounded-xl font-semibold hover:bg-purple-700 shadow-md hover:shadow-lg transition-all disabled:opacity-60"
          >
            {loading ? "Logging in…" : "Log In"}
          </button>
        </form>

        {/* Sign Up */}
        <p className="mt-6 text-gray-600">
          Don’t have an account?{" "}
          <Link to="/signup" className="text-purple-600 font-semibold hover:underline">
            Sign Up
          </Link>
        </p>
      </div>
    </div>
  );
}

export default Login;
