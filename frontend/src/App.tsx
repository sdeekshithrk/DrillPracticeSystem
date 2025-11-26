import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import RequireAuth from "./components/RequireAuth";

import PracticePage from "./pages/PracticePage";
import SolveProblemPage from "./pages/SolveProblemPage";
import LoginPage from "./pages/LoginPage";
import SignupPage from "./pages/SignupPage";

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        {/* Public Routes */}
        <Route path="/login" element={<LoginPage />} />
        <Route path="/signup" element={<SignupPage />} />

        {/* Protected Routes */}
        <Route
          path="/"
          element={
            <RequireAuth>
              <Navigate to="/practice" />
            </RequireAuth>
          }
        />

        <Route
          path="/practice"
          element={
            <RequireAuth>
              <PracticePage />
            </RequireAuth>
          }
        />

        <Route
          path="/practice/:id"
          element={
            <RequireAuth>
              <SolveProblemPage />
            </RequireAuth>
          }
        />

        {/* Catch all → smart redirect */}
        <Route path="*" element={<Navigate to="/login" />} />
      </Routes>
    </BrowserRouter>
  );
}
