import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { getRecommendedJobs } from "../../api/trainees";
import { Loading, ErrorState, EmptyState } from "../../components/States";
import { MatchBadge } from "../../components/Badges";

export default function RecommendedJobs() {
  const [jobs, setJobs] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);

  const load = () => {
    setLoading(true);
    setError("");
    getRecommendedJobs(50)
      .then(setJobs)
      .catch((err) => setError(err.detail || "Unable to load jobs."))
      .finally(() => setLoading(false));
  };

  useEffect(load, []);

  return (
    <div>
      <div className="page-header">
        <h1>Recommended Jobs</h1>
        <p className="page-sub">Ranked by how well your skills match each role.</p>
      </div>
      {loading && <Loading />}
      {error && <ErrorState message={error} onRetry={load} />}
      {!loading && !error && jobs?.length === 0 && (
        <EmptyState message="No recommended jobs found." />
      )}
      {!loading && !error && (
        <div className="job-grid">
          {jobs.map((job) => (
            <div className="card job-card" key={job.job_id}>
              <div className="job-card-top">
                <div>
                  <h3>{job.job}</h3>
                  <p className="job-card-sub">{job.employer} · {job.location}</p>
                </div>
                <MatchBadge percentage={job.match_percentage} />
              </div>
              {job.top_skill_gaps?.length > 0 && (
                <div className="job-card-gaps">
                  <span className="eyebrow">Top skill gaps</span>
                  <p>{job.top_skill_gaps.join(", ")}</p>
                </div>
              )}
              <Link to={`/trainee/jobs/${job.job_id}`} className="btn btn-secondary btn-block">
                View Job
              </Link>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
