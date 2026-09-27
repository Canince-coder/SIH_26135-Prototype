import { NotAvailable } from "../../components/States";

export default function AdminFunnel() {
  return (
    <div>
      <div className="page-header">
        <h1>Application Funnel</h1>
      </div>
      <div className="card">
        <NotAvailable
          endpoint="GET /analytics/applications-by-status"
          note="Once available, this will render APPLIED → SHORTLISTED → INTERVIEW → SELECTED as a funnel, plus REJECTED and WITHDRAWN counts."
        />
      </div>
    </div>
  );
}
