import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import RequireAuth from "./components/RequireAuth";

import PracticePage from "./pages/PracticePage";
import SolveProblemPage from "./pages/SolveProblemPage";
import LoginPage from "./pages/LoginPage";
import SignupPage from "./pages/SignupPage";
import DashboardPage from "./pages/DashboardPage";

export default function App() {
  return (
    <BrowserRouter>
      <Routes>

        {/* Public Routes */}
        <Route path="/login" element={<LoginPage />} />
        <Route path="/signup" element={<SignupPage />} />

        {/* Default route -> Practice */}
        <Route path="/" element={<Navigate to="/practice" replace />} />

        {/* Protected Routes */}
        <Route
          path="/practice"
          element={<RequireAuth><PracticePage /></RequireAuth>}
        />

        <Route
          path="/practice/:id"
          element={<RequireAuth><SolveProblemPage /></RequireAuth>}
        />

        <Route
          path="/dashboard"
          element={<RequireAuth><DashboardPage /></RequireAuth>}
        />

        {/* Catch-all */}
        <Route path="*" element={<Navigate to="/practice" />} />
      </Routes>
    </BrowserRouter>
  );
}
