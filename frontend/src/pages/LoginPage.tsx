import { useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import { API_BASE_URL } from "../config";
import { Lock, User } from "lucide-react";

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

      localStorage.setItem("access_token", res.data.access_token);
      localStorage.setItem("token_type", res.data.token_type || "bearer");
      localStorage.setItem("user_email", email);

      navigate("/practice", { replace: true });
    } catch {
      setError("Invalid email or password.");
    }

    setLoading(false);
  };

  return (
    <div
      className="
        min-h-screen
        bg-gradient-to-br from-[#0a0f1f] via-[#0b0f19] to-[#111827]
        flex flex-col items-center justify-center px-4
        text-gray-200
      "
    >
      {/* Project Title */}
      <div className="text-center mb-10">
        <h1 className="text-4xl font-extrabold text-cyan-300 drop-shadow-md">
          Logic & Set Theory Drill System
        </h1>
        <p className="text-gray-400 mt-2 text-lg">
          Practice • Improve • Master Discrete Math Concepts
        </p>
      </div>

      {/* Login Card */}
      <form
        onSubmit={handleLogin}
        className="
          bg-gray-900/70 backdrop-blur-xl
          p-8 rounded-2xl shadow-2xl border border-gray-700/60
          w-full max-w-md
        "
      >
        <h2 className="text-2xl font-bold text-white mb-6 text-center">
          Login to Continue
        </h2>

        {error && (
          <div className="bg-red-600/30 text-red-300 p-3 rounded mb-4 text-sm text-center border border-red-500/40">
            {error}
          </div>
        )}

        {/* Email */}
        <div className="relative mb-4">
          <User className="absolute left-3 top-3 text-gray-400" />
          <input
            type="email"
            placeholder="Email"
            className="
              w-full p-3 pl-10 rounded-lg
              bg-gray-800 text-white
              border border-gray-700
              focus:border-cyan-500 outline-none
              transition
            "
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
        </div>

        {/* Password */}
        <div className="relative mb-6">
          <Lock className="absolute left-3 top-3 text-gray-400" />
          <input
            type="password"
            placeholder="Password"
            className="
              w-full p-3 pl-10 rounded-lg
              bg-gray-800 text-white
              border border-gray-700
              focus:border-cyan-500 outline-none
              transition
            "
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>

        {/* Login Button */}
        <button
          type="submit"
          disabled={loading}
          className="
            w-full py-3 rounded-lg
            bg-cyan-600 hover:bg-cyan-700
            shadow-lg shadow-cyan-600/40
            text-white font-bold text-lg
            transition disabled:opacity-50
          "
        >
          {loading ? "Logging in..." : "Login"}
        </button>

        {/* Signup Link */}
        <p className="text-gray-400 mt-4 text-center text-sm">
          Don't have an account?{" "}
          <a
            href="/signup"
            className="text-cyan-400 hover:text-cyan-300 underline"
          >
            Sign Up
          </a>
        </p>
      </form>
    </div>
  );
}
