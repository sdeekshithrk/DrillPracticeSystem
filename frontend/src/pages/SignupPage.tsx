import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import axios from "axios";
import { API_BASE_URL } from "../config";
import { User, Mail, Lock } from "lucide-react";

export default function SignupPage() {
  const navigate = useNavigate();

  const [first, setFirst] = useState("");
  const [last, setLast] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirm, setConfirm] = useState("");

  const [error, setError] = useState("");
  const [strength, setStrength] = useState(0);
  const [success, setSuccess] = useState(false);

  function calcStrength(pwd: string) {
    let s = 0;
    if (pwd.length >= 8) s++;
    if (/[A-Z]/.test(pwd)) s++;
    if (/[0-9]/.test(pwd)) s++;
    if (/[^A-Za-z0-9]/.test(pwd)) s++;
    setStrength(s);
  }

  async function handleSignup(e: React.FormEvent) {
    e.preventDefault();
    setError("");

    if (password !== confirm) {
      setError("Passwords do not match.");
      return;
    }

    try {
      await axios.post(`${API_BASE_URL}/auth/signup`, {
        first_name: first,
        last_name: last,
        email,
        password,
      });

      setSuccess(true);

      setTimeout(() => {
        navigate("/login");
      }, 1600);
    } catch {
      setError("Signup failed. Email may already exist.");
    }
  }

  const strengthColors = ["bg-red-500", "bg-orange-400", "bg-yellow-400", "bg-green-500"];
  const strengthLabel = ["Weak", "Fair", "Good", "Strong"];

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-gray-900 via-gray-800 to-black px-4">
      <div className="bg-gray-800/50 backdrop-blur-lg border border-gray-700 shadow-2xl shadow-black/50 rounded-2xl p-10 w-full max-w-md">

        <h1 className="text-4xl font-extrabold text-cyan-300 text-center mb-6 drop-shadow-lg">
          Create Account
        </h1>

        {success && (
          <p className="text-green-400 text-center font-semibold mb-4 animate-pulse">
            ✔ Signup successful! Redirecting…
          </p>
        )}

        {error && (
          <p className="text-red-400 text-center font-semibold mb-4">
            {error}
          </p>
        )}

        <form className="space-y-5" onSubmit={handleSignup}>

          {/* First + Last Name */}
          <div className="flex gap-4">
            <div className="w-1/2 relative">
              <label className="text-gray-300">First Name</label>
              <User className="input-icon" />
              <input
                required
                value={first}
                onChange={(e) => setFirst(e.target.value)}
                className="input-box"
              />
            </div>

            <div className="w-1/2 relative">
              <label className="text-gray-300">Last Name</label>
              <User className="input-icon" />
              <input
                required
                value={last}
                onChange={(e) => setLast(e.target.value)}
                className="input-box"
              />
            </div>
          </div>

          {/* Email */}
          <div className="relative">
            <label className="text-gray-300">Email</label>
            <Mail className="input-icon" />
            <input
              type="email"
              required
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="input-box"
            />
          </div>

          {/* Password */}
          <div className="relative">
            <label className="text-gray-300">Password</label>
            <Lock className="input-icon" />
            <input
              type="password"
              required
              value={password}
              onChange={(e) => {
                setPassword(e.target.value);
                calcStrength(e.target.value);
              }}
              className="input-box"
            />
          </div>

          {/* Password Strength Bar */}
          {password && (
            <div className="w-full">
              <div className="w-full h-2 rounded-full bg-gray-700">
                <div
                  className={`h-full rounded-full transition-all ${strengthColors[strength - 1]}`}
                  style={{ width: `${strength * 25}%` }}
                />
              </div>
              <p className="text-sm text-gray-300 mt-1">
                Strength: {strengthLabel[strength - 1] || "Too Weak"}
              </p>
            </div>
          )}

          {/* Confirm Password */}
          <div className="relative">
            <label className="text-gray-300">Confirm Password</label>
            <Lock className="input-icon" />
            <input
              type="password"
              required
              value={confirm}
              onChange={(e) => setConfirm(e.target.value)}
              className="input-box"
            />
          </div>

          <button type="submit" className="btn-cyan">
            Sign Up
          </button>
        </form>

        <p className="text-gray-400 text-center mt-4">
          Already have an account?{" "}
          <Link to="/login" className="text-cyan-300 hover:underline">
            Log In
          </Link>
        </p>
      </div>

      {/* Styles */}
      <style>{`
        .input-box {
          width: 100%;
          margin-top: 4px;
          padding: 12px 12px 12px 40px; /* Left padding for icon */
          background: rgba(20,20,20,0.9);
          border: 1px solid #444;
          border-radius: 10px;
          color: white;
          outline: none;
          transition: 0.2s;
        }
        .input-box:focus {
          border-color: #22d3ee;
          box-shadow: 0 0 10px #22d3ee60;
        }
        .input-icon {
          position: absolute;
          left: 12px;
          top: 50%;
          transform: translateY(8px);
          color: #9ca3af;
        }
        .btn-cyan {
          width: 100%;
          padding: 12px;
          border-radius: 10px;
          font-weight: bold;
          background: linear-gradient(to bottom right, #22d3ee, #0891b2);
          color: black;
          box-shadow: 0 0 20px #22d3ee50;
          transition: 0.2s;
        }
        .btn-cyan:hover {
          transform: scale(1.05);
          box-shadow: 0 0 25px #22d3ee80;
        }
      `}</style>
    </div>
  );
}
