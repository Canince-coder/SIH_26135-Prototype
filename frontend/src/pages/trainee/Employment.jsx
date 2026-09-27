import { NotAvailable } from "../../components/States";

export default function Employment() {
  return (
    <div>
      <div className="page-header">
        <h1>Employment</h1>
      </div>
      <div className="card">
        <NotAvailable
          endpoint="GET /trainees/me/employment"
          note="Once a trainee is SELECTED, this page will show their company, role, location, joining date, salary and verification status."
        />
      </div>
    </div>
  );
}
