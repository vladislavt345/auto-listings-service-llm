import type { ReactElement } from "react";
import { useState } from "react";
import { useNavigate } from "react-router-dom";

import { CarFiltersPanel } from "../components/CarFilters";
import { CarTable } from "../components/CarTable";
import { useCars } from "../hooks/useCars";
import type { CarFilters } from "../types/car";
import { clearToken } from "../utils/token";

/* ── sidebar icons ──────────────────────────────────── */
const IconGrid = () => (
  <svg viewBox="0 0 16 16" fill="currentColor">
    <rect x="1" y="1" width="6" height="6" rx="1" />
    <rect x="9" y="1" width="6" height="6" rx="1" />
    <rect x="1" y="9" width="6" height="6" rx="1" />
    <rect x="9" y="9" width="6" height="6" rx="1" />
  </svg>
);

const IconCar = () => (
  <svg viewBox="0 0 16 16" fill="currentColor">
    <path d="M3.5 6.5 5 3h6l1.5 3.5H3.5Z" />
    <rect x="1" y="6.5" width="14" height="5" rx="1.2" />
    <circle cx="4" cy="13" r="1.3" />
    <circle cx="12" cy="13" r="1.3" />
  </svg>
);

const IconFilter = () => (
  <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round">
    <path d="M2 4h12M4.5 8h7M7 12h2" />
  </svg>
);

const IconSettings = () => (
  <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" strokeWidth="1.4">
    <circle cx="8" cy="8" r="2.2" />
    <path d="M8 1v1.5M8 13.5V15M1 8h1.5M13.5 8H15M3.2 3.2l1.1 1.1M11.7 11.7l1.1 1.1M3.2 12.8l1.1-1.1M11.7 4.3l1.1-1.1" strokeLinecap="round" />
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

  if (isLoading) {
    return <div className="page-loading">Loading listings</div>;
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
        <button className="sb-btn" title="Dashboard">
          <IconGrid />
        </button>
        <button className="sb-btn" title="Filters">
          <IconFilter />
        </button>
        <div className="sb-spacer" />
        <button className="sb-btn" title="Settings">
          <IconSettings />
        </button>
      </aside>

      {/* ── main ── */}
      <main className="app-main grid-bg">
        <div className="section-label">
          <span className="dot" />
          Car Listings
        </div>

        <div className="filters-bar">
          <CarFiltersPanel filters={filters} onChange={setFilters} />
        </div>

        {isError && (
          <div className="error-bar">Failed to load car listings</div>
        )}

        <div className="table-wrap">
          <CarTable cars={cars} />
        </div>
      </main>
    </div>
  );
}
