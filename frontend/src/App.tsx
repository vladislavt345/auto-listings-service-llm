import type { ReactElement } from "react";
import { Navigate, Route, Routes } from "react-router-dom";

import { isAuthenticated } from "./utils/token";
import { CarsPage } from "./pages/CarsPage";
import { LoginPage } from "./pages/LoginPage";

/**
 * Render route content only for authenticated users.
 */
function ProtectedRoute({
  children,
}: {
  children: ReactElement;
}): ReactElement {
  if (!isAuthenticated()) {
    return <Navigate to="/login" replace />;
  }
  return children;
}

/**
 * Root SPA routes.
 */
export function App(): ReactElement {
  return (
    <Routes>
      <Route path="/login" element={<LoginPage />} />
      <Route
        path="/"
        element={
          <ProtectedRoute>
            <CarsPage />
          </ProtectedRoute>
        }
      />
    </Routes>
  );
}
