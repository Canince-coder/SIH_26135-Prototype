import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { register } from "../api/auth";

const initialState = {
  name: "",
  email: "",
  password: "",
  role: "TRAINEE",
  district: "",
  education: "",
  phone: "",
  company_name: "",
  location: "",
};

export default function Register() {
  const navigate = useNavigate();
  const [form, setForm] = useState(initialState);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const update = (field) => (e) => setForm({ ...form, [field]: e.target.value });

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      const payload = { name: form.name, email: form.email, password: form.password, role: form.role };
      if (form.role === "TRAINEE") {
        payload.district = form.district || undefined;
        payload.education = form.education || undefined;
        payload.phone = form.phone || undefined;
      } else if (form.role === "EMPLOYER") {
        payload.company_name = form.company_name || undefined;
        payload.location = form.location || undefined;
      }
      await register(payload);
      navigate("/login");
    } catch (err) {
      setError(err.detail || "Registration failed.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-page">
      <div className="auth-card auth-card-wide">
        <Link to="/" className="landing-brand auth-brand">
          <span className="brand-mark">SB</span>
          <span>SkillBridge</span>
        </Link>
        <h2>Create your account</h2>
        {error && <div className="alert alert-error">{error}</div>}
        <form onSubmit={handleSubmit} className="form">
          <label>
            Name
            <input required value={form.name} onChange={update("name")} />
          </label>
          <label>
            Email
            <input type="email" required value={form.email} onChange={update("email")} />
          </label>
          <label>
            Password
            <input
              type="password"
              required
              minLength={8}
              value={form.password}
              onChange={update("password")}
            />
          </label>
          <label>
            Role
            <select value={form.role} onChange={update("role")}>
              <option value="TRAINEE">Trainee</option>
              <option value="EMPLOYER">Employer</option>
              <option value="ADMIN">Admin</option>
            </select>
          </label>

          {form.role === "TRAINEE" && (
            <>
              <label>
                District
                <input value={form.district} onChange={update("district")} />
              </label>
              <label>
                Education
                <input value={form.education} onChange={update("education")} />
              </label>
              <label>
                Phone
                <input value={form.phone} onChange={update("phone")} />
              </label>
            </>
          )}

          {form.role === "EMPLOYER" && (
            <>
              <label>
                Company Name
                <input value={form.company_name} onChange={update("company_name")} />
              </label>
              <label>
                Location
                <input value={form.location} onChange={update("location")} />
              </label>
            </>
          )}

          <button className="btn btn-primary btn-block" disabled={loading}>
            {loading ? "Creating account..." : "Register"}
          </button>
        </form>
        <p className="auth-switch">
          Already have an account? <Link to="/login">Login</Link>
        </p>
      </div>
    </div>
  );
}
