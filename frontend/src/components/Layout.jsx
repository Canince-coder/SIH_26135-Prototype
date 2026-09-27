import { NavLink, Outlet, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

const NAV_ITEMS = {
  TRAINEE: [
    { to: "/trainee/dashboard", label: "Dashboard" },
    { to: "/trainee/jobs", label: "Recommended Jobs" },
    { to: "/trainee/skills", label: "My Skills" },
    { to: "/trainee/applications", label: "My Applications" },
    { to: "/trainee/profile", label: "My Profile" },
    { to: "/trainee/employment", label: "Employment" },
  ],
  EMPLOYER: [
    { to: "/employer/dashboard", label: "Dashboard" },
    { to: "/employer/jobs", label: "Jobs" },
    { to: "/employer/applications", label: "Applications" },
    { to: "/employer/analytics", label: "Analytics" },
  ],
  ADMIN: [
    { to: "/admin/dashboard", label: "Dashboard" },
    { to: "/admin/applications", label: "Application Funnel" },
    { to: "/admin/skills", label: "Skills Analytics" },
  ],
};

export default function Layout() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const items = NAV_ITEMS[user?.role] || [];

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="sidebar-brand">
          <span className="brand-mark">SB</span>
          <span>SkillBridge</span>
        </div>
        <nav className="sidebar-nav">
          {items.map((item) => (
            <NavLink
              key={item.to}
              to={item.to}
              className={({ isActive }) => `sidebar-link ${isActive ? "active" : ""}`}
            >
              {item.label}
            </NavLink>
          ))}
        </nav>
        <div className="sidebar-footer">
          <div className="sidebar-user">
            <div className="sidebar-user-name">{user?.name}</div>
            <div className="sidebar-user-role">{user?.role}</div>
          </div>
          <button className="sidebar-link logout" onClick={handleLogout}>
            Logout
          </button>
        </div>
      </aside>
      <main className="content">
        <Outlet />
      </main>
    </div>
  );
}
