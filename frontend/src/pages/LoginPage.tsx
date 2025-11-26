import { useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import { API_BASE_URL } from "../config";

export default function LoginPage() {
  const navigate = useNavigate();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError("");

    try {
      const res = await axios.post(`${API_BASE_URL}/auth/login`, {
        email,
        password,
      });

      // SAVE TOKEN FOR FUTURE ROUTES
      localStorage.setItem("access_token", res.data.access_token);
      localStorage.setItem("token_type", res.data.token_type || "bearer");
      localStorage.setItem("user_email", email);

      // Redirect after login
      navigate("/practice", { replace: true });

    } catch (err: any) {
      setError("Invalid email or password.");
    }

    setLoading(false);
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-900 px-4">
      <form
        onSubmit={handleLogin}
        className="bg-gray-800 p-8 rounded-xl shadow-2xl border border-gray-700 w-full max-w-md"
      >
        <h1 className="text-3xl font-bold text-white mb-6 text-center">
          Login
        </h1>

        {error && (
          <div className="bg-red-600/30 text-red-300 p-3 rounded mb-4 text-sm text-center">
            {error}
          </div>
        )}

        <input
          type="email"
          placeholder="Email"
          className="w-full p-3 rounded mb-4 bg-gray-700 text-white"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />

        <input
          type="password"
          placeholder="Password"
          className="w-full p-3 rounded mb-6 bg-gray-700 text-white"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />

        <button
          type="submit"
          disabled={loading}
          className="w-full bg-cyan-600 hover:bg-cyan-700 text-white font-bold py-3 rounded-lg shadow-md shadow-cyan-500/30 transition"
        >
          {loading ? "Logging in..." : "Login"}
        </button>

        <p className="text-gray-400 mt-4 text-center text-sm">
          No account?{" "}
          <a
            href="/signup"
            className="text-cyan-400 hover:text-cyan-200 underline"
          >
            Sign Up
          </a>
        </p>
      </form>
    </div>
  );
}
