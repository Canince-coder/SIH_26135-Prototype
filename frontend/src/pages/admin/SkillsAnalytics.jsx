import { NotAvailable } from "../../components/States";

export default function AdminSkillsAnalytics() {
  return (
    <div>
      <div className="page-header">
        <h1>Skills Analytics</h1>
      </div>
      <div className="card">
        <NotAvailable
          endpoint="GET /analytics/skills-demand-supply"
          note="Once available, this will chart demand vs supply vs gap per skill."
        />
      </div>
    </div>
  );
}
