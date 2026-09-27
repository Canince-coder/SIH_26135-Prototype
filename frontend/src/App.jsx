import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { AuthProvider } from "./context/AuthContext";
import ProtectedRoute from "./components/ProtectedRoute";
import Layout from "./components/Layout";

import Landing from "./pages/Landing";
import Login from "./pages/Login";
import Register from "./pages/Register";

import TraineeDashboard from "./pages/trainee/Dashboard";
import RecommendedJobs from "./pages/trainee/RecommendedJobs";
import JobDetails from "./pages/trainee/JobDetails";
import SkillGap from "./pages/trainee/SkillGap";
import Skills from "./pages/trainee/Skills";
import Profile from "./pages/trainee/Profile";
import Applications from "./pages/trainee/Applications";
import Employment from "./pages/trainee/Employment";

import EmployerDashboard from "./pages/employer/Dashboard";
import EmployerJobs from "./pages/employer/Jobs";
import EmployerApplications from "./pages/employer/Applications";
import EmployerAnalytics from "./pages/employer/Analytics";

import AdminDashboard from "./pages/admin/Dashboard";
import AdminFunnel from "./pages/admin/Funnel";
import AdminSkillsAnalytics from "./pages/admin/SkillsAnalytics";

export default function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <Routes>
          <Route path="/" element={<Landing />} />
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />

          <Route element={<ProtectedRoute roles={["TRAINEE"]}><Layout /></ProtectedRoute>}>
            <Route path="/trainee/dashboard" element={<TraineeDashboard />} />
            <Route path="/trainee/jobs" element={<RecommendedJobs />} />
            <Route path="/trainee/jobs/:jobId" element={<JobDetails />} />
            <Route path="/trainee/jobs/:jobId/skill-gap" element={<SkillGap />} />
            <Route path="/trainee/skills" element={<Skills />} />
            <Route path="/trainee/profile" element={<Profile />} />
            <Route path="/trainee/applications" element={<Applications />} />
            <Route path="/trainee/employment" element={<Employment />} />
          </Route>

          <Route element={<ProtectedRoute roles={["EMPLOYER"]}><Layout /></ProtectedRoute>}>
            <Route path="/employer/dashboard" element={<EmployerDashboard />} />
            <Route path="/employer/jobs" element={<EmployerJobs />} />
            <Route path="/employer/applications" element={<EmployerApplications />} />
            <Route path="/employer/analytics" element={<EmployerAnalytics />} />
          </Route>

          <Route element={<ProtectedRoute roles={["ADMIN"]}><Layout /></ProtectedRoute>}>
            <Route path="/admin/dashboard" element={<AdminDashboard />} />
            <Route path="/admin/applications" element={<AdminFunnel />} />
            <Route path="/admin/skills" element={<AdminSkillsAnalytics />} />
          </Route>

          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </AuthProvider>
    </BrowserRouter>
  );
}
