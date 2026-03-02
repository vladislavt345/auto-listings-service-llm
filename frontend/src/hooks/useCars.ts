import { useQuery } from '@tanstack/react-query'

import { fetchCars } from '../api/cars'
import type { Car, CarFilters } from '../types/car'

/**
 * Query hook for car listings with filter support.
 */
export function useCars(filters: CarFilters) {
  return useQuery<Car[]>({
    queryKey: ['cars', filters],
    queryFn: () => fetchCars(filters),
  })
}
