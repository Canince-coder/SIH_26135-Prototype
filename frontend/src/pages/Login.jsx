import { useState } from "react";
import { Link, useNavigate, useSearchParams } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

export default function Login() {
  const { login } = useAuth();
  const navigate = useNavigate();
  const [params] = useSearchParams();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      const user = await login(email, password);
      navigate(`/${user.role.toLowerCase()}/dashboard`);
    } catch (err) {
      setError(err.detail || "Login failed. Check your credentials.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-page">
      <div className="auth-card">
        <Link to="/" className="landing-brand auth-brand">
          <span className="brand-mark">SB</span>
          <span>SkillBridge</span>
        </Link>
        <h2>Log in</h2>
        {params.get("expired") && (
          <div className="alert alert-warning">Your session has expired. Please login again.</div>
        )}
        {error && <div className="alert alert-error">{error}</div>}
        <form onSubmit={handleSubmit} className="form">
          <label>
            Email
            <input
              type="email"
              required
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="you@example.com"
            />
          </label>
          <label>
            Password
            <input
              type="password"
              required
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="••••••••"
            />
          </label>
          <button className="btn btn-primary btn-block" disabled={loading}>
            {loading ? "Logging in..." : "Login"}
          </button>
        </form>
        <p className="auth-switch">
          No account? <Link to="/register">Register</Link>
        </p>
      </div>
    </div>
  );
}
