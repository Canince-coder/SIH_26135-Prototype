import { useEffect, useState } from "react";
import { getMySkills, addMySkill } from "../../api/trainees";
import { Loading, ErrorState, EmptyState } from "../../components/States";

export default function Skills() {
  const [skills, setSkills] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);
  const [skillId, setSkillId] = useState("");
  const [level, setLevel] = useState(3);
  const [formError, setFormError] = useState("");
  const [submitting, setSubmitting] = useState(false);

  const load = () => {
    setLoading(true);
    setError("");
    getMySkills()
      .then(setSkills)
      .catch((err) => setError(err.detail || "Unable to load your skills."))
      .finally(() => setLoading(false));
  };

  useEffect(load, []);

  const handleAdd = async (e) => {
    e.preventDefault();
    setFormError("");
    if (!skillId.trim()) {
      setFormError("Enter a skill ID to add.");
      return;
    }
    setSubmitting(true);
    try {
      await addMySkill({ skill_id: skillId.trim(), proficiency_level: Number(level) });
      setSkillId("");
      setLevel(3);
      load();
    } catch (err) {
      setFormError(err.detail || "Could not add that skill.");
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div>
      <div className="page-header">
        <h1>My Skills</h1>
        <p className="page-sub">Your proficiency levels, from 1 (beginner) to 5 (expert).</p>
      </div>

      {loading && <Loading />}
      {error && <ErrorState message={error} onRetry={load} />}

      {!loading && !error && (
        <>
          {skills.length === 0 ? (
            <EmptyState message="You haven't added any skills yet." />
          ) : (
            <div className="table-card">
              {skills.map((s) => (
                <div className="table-row" key={s.id}>
                  <strong>{s.skill.name}</strong>
                  <div className="proficiency-dots">
                    {[1, 2, 3, 4, 5].map((lvl) => (
                      <span key={lvl} className={`dot ${lvl <= s.proficiency_level ? "filled" : ""}`} />
                    ))}
                  </div>
                </div>
              ))}
            </div>
          )}
        </>
      )}

      <div className="card add-skill-card">
        <h2>Add a skill</h2>
        <p className="page-sub">
          The backend doesn't expose a "list all skills" endpoint yet, so paste the skill's
          ID here (visible via <code>/docs</code> or the seed data). Once a
          <code>GET /skills</code> endpoint exists this can become a dropdown.
        </p>
        <form onSubmit={handleAdd} className="form form-inline">
          <label>
            Skill ID
            <input value={skillId} onChange={(e) => setSkillId(e.target.value)} placeholder="uuid" />
          </label>
          <label>
            Level (1-5)
            <select value={level} onChange={(e) => setLevel(e.target.value)}>
              {[1, 2, 3, 4, 5].map((l) => (
                <option key={l} value={l}>{l}</option>
              ))}
            </select>
          </label>
          <button className="btn btn-primary" disabled={submitting}>
            {submitting ? "Adding..." : "Add Skill"}
          </button>
        </form>
        {formError && <div className="alert alert-error">{formError}</div>}
      </div>
    </div>
  );
}
