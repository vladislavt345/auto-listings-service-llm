import type { ReactElement } from "react";
import { useState } from "react";
import { useNavigate } from "react-router-dom";

import { CarFiltersPanel } from "../components/CarFilters";
import { CarTable } from "../components/CarTable";
import { useCars } from "../hooks/useCars";
import type { CarFilters } from "../types/car";
import { clearToken } from "../utils/token";

/**
 * Protected page with car listings table.
 */
export function CarsPage(): ReactElement {
  const navigate = useNavigate();
  const [filters, setFilters] = useState<CarFilters>({ limit: 50, offset: 0 });
  const { data: cars = [], isLoading, isError } = useCars(filters);

  function logout(): void {
    clearToken();
    navigate("/login");
  }

  if (isLoading) {
    return <div className="page-center">Loading...</div>;
  }

  return (
    <div className="container">
      <header className="header">
        <h1>Cars</h1>
        <button onClick={logout}>Log out</button>
      </header>
      <CarFiltersPanel filters={filters} onChange={setFilters} />
      {isError && <p className="error">Failed to load car listings</p>}
      <CarTable cars={cars} />
    </div>
  );
}
