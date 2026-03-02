import type { ReactElement } from "react";
import { useState } from "react";
import { useNavigate } from "react-router-dom";

import { CarFiltersPanel } from "../components/CarFilters";
import { CarTable } from "../components/CarTable";
import { useCars } from "../hooks/useCars";
import type { CarFilters } from "../types/car";
import { clearToken } from "../utils/token";

/* ── sidebar icons ──────────────────────────────────── */
const IconCar = () => (
  <svg viewBox="0 0 16 16" fill="currentColor">
    <path d="M3.5 6.5 5 3h6l1.5 3.5H3.5Z" />
    <rect x="1" y="6.5" width="14" height="5" rx="1.2" />
    <circle cx="4" cy="13" r="1.3" />
    <circle cx="12" cy="13" r="1.3" />
  </svg>
);

export function CarsPage(): ReactElement {
  const navigate = useNavigate();
  const [filters, setFilters] = useState<CarFilters>({ limit: 50, offset: 0 });
  const { data: cars = [], isLoading, isError } = useCars(filters);

  function logout(): void {
    clearToken();
    navigate("/login");
  }

  return (
    <div className="app-shell">
      {/* ── header ── */}
      <header className="app-header">
        <span className="hdr-logo">Auto-Listings</span>
        <span className="hdr-sep">|</span>
        <span className="hdr-crumb">Cars / Listings</span>
        <div className="hdr-spacer" />
        <div className="hdr-stat">
          Total <b className="blue">{cars.length}</b>
        </div>
        <button className="btn-logout" onClick={logout}>Logout</button>
      </header>

      {/* ── sidebar ── */}
      <aside className="app-sidebar">
        <button className="sb-btn active" title="Cars">
          <IconCar />
        </button>
      </aside>

      {/* ── main ── */}
      <main className="app-main grid-bg">
        <div className="section-label">
          <span className="dot" />
          Car Listings
          {isLoading && <span className="fetching-label">fetching…</span>}
        </div>

        <div className="filters-bar">
          <CarFiltersPanel filters={filters} onChange={setFilters} />
        </div>

        {isError && (
          <div className="error-bar">Failed to load car listings</div>
        )}

        <div className={`table-wrap${isLoading ? " table-wrap--loading" : ""}`}>
          <CarTable cars={cars} />
        </div>
      </main>
    </div>
  );
}
