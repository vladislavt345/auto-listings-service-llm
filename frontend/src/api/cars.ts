import { api } from "./client";
import type { Car, CarFilters } from "../types/car";

/**
 * Load car listings from protected API endpoint.
 */
export async function fetchCars(filters: CarFilters): Promise<Car[]> {
  const { data } = await api.get("/api/cars", { params: filters });
  return data;
}
