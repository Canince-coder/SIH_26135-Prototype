import { useEffect, useState } from "react";
import { getMyTraineeProfile, updateMyTraineeProfile } from "../../api/trainees";
import { Loading, ErrorState } from "../../components/States";

export default function Profile() {
  const [profile, setProfile] = useState(null);
  const [form, setForm] = useState({ district: "", education: "", phone: "" });
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [saved, setSaved] = useState(false);
  const [saveError, setSaveError] = useState("");

  const load = () => {
    setLoading(true);
    setError("");
    getMyTraineeProfile()
      .then((p) => {
        setProfile(p);
        setForm({ district: p.district || "", education: p.education || "", phone: p.phone || "" });
      })
      .catch((err) => setError(err.detail || "Unable to load your profile."))
      .finally(() => setLoading(false));
  };

  useEffect(load, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSaving(true);
    setSaveError("");
    setSaved(false);
    try {
      const updated = await updateMyTraineeProfile(form);
      setProfile(updated);
      setSaved(true);
    } catch (err) {
      setSaveError(err.detail || "Could not save your profile.");
    } finally {
      setSaving(false);
    }
  };

  if (loading) return <Loading />;
  if (error) return <ErrorState message={error} onRetry={load} />;

  return (
    <div>
      <div className="page-header">
        <h1>My Profile</h1>
      </div>
      <div className="card profile-card">
        <div className="profile-summary">
          <div>
            <span className="eyebrow">Name</span>
            <p>{profile.user.name}</p>
          </div>
          <div>
            <span className="eyebrow">Email</span>
            <p>{profile.user.email}</p>
          </div>
        </div>

        <form onSubmit={handleSubmit} className="form">
          <label>
            District
            <input
              value={form.district}
              onChange={(e) => setForm({ ...form, district: e.target.value })}
            />
          </label>
          <label>
            Education
            <input
              value={form.education}
              onChange={(e) => setForm({ ...form, education: e.target.value })}
            />
          </label>
          <label>
            Phone
            <input
              value={form.phone}
              onChange={(e) => setForm({ ...form, phone: e.target.value })}
            />
          </label>
          <button className="btn btn-primary" disabled={saving}>
            {saving ? "Saving..." : "Save Changes"}
          </button>
          {saved && <div className="alert alert-success">Profile updated.</div>}
          {saveError && <div className="alert alert-error">{saveError}</div>}
        </form>
      </div>
    </div>
  );
}
