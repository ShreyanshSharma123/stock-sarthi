import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

export default function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const { login } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setLoading(true);

    try {
      await login(email, password);
      navigate("/");
    } catch (err) {
      // Extract error message safely
      let errorMsg = "Login failed. Please check your credentials.";
      if (err instanceof Error) {
        errorMsg = err.message;
      } else if (err.response?.data?.detail) {
        errorMsg = err.response.data.detail;
      } else if (err.response?.data) {
        const data = err.response.data;
        if (Array.isArray(data)) {
          errorMsg = data
            .map((e) => (typeof e === "object" && e.msg ? e.msg : String(e)))
            .join(", ");
        } else if (typeof data === "string") {
          errorMsg = data;
        }
      }
      setError(errorMsg);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="mt-16 flex items-center justify-center min-h-[calc(100vh-8rem)]">
      <div className="w-full max-w-md">
        <div className="card">
          <div className="text-center mb-6">
            <div className="w-12 h-12 bg-primary-600 rounded-xl flex items-center justify-center mx-auto">
              <span className="text-white text-xl font-bold">S</span>
            </div>
            <h1 className="text-2xl font-bold mt-4">Welcome Back</h1>
            <p className="text-gray-500 mt-1">Login to Stock Saarthi</p>
          </div>

          {error && (
            <div className="bg-red-50 text-red-600 p-3 rounded-lg mb-4 text-sm">
              {error}
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Email
              </label>
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="input-field"
                placeholder="you@example.com"
                required
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Password
              </label>
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="input-field"
                placeholder="••••••••"
                required
              />
            </div>

            <button
              type="submit"
              className="btn-primary w-full"
              disabled={loading}
            >
              {loading ? "Logging in..." : "Login"}
            </button>
          </form>

          <p className="text-center text-sm text-gray-500 mt-4">
            Don't have an account?{" "}
            <Link
              to="/register"
              className="text-primary-600 font-medium hover:underline"
            >
              Sign up
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
}
