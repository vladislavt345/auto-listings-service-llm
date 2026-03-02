import type { ReactElement } from 'react'
import type { CarFilters } from '../types/car'

type Props = {
  filters: CarFilters
  onChange: (filters: CarFilters) => void
}

export function CarFiltersPanel({ filters, onChange }: Props): ReactElement {
  return (
    <>
      <input
        className="f-input"
        value={filters.make ?? ''}
        onChange={(e) => onChange({ ...filters, make: e.target.value || undefined })}
        placeholder="Make"
      />
      <input
        className="f-input"
        value={filters.model ?? ''}
        onChange={(e) => onChange({ ...filters, model: e.target.value || undefined })}
        placeholder="Model"
      />
      <input
        className="f-input"
        value={filters.color ?? ''}
        onChange={(e) => onChange({ ...filters, color: e.target.value || undefined })}
        placeholder="Color"
      />
      <input
        className="f-input"
        type="number"
        value={filters.max_price ?? ''}
        onChange={(e) => onChange({ ...filters, max_price: e.target.value ? Number(e.target.value) : undefined })}
        placeholder="Max price"
      />
      <input
        className="f-input"
        type="number"
        value={filters.min_year ?? ''}
        onChange={(e) => onChange({ ...filters, min_year: e.target.value ? Number(e.target.value) : undefined })}
        placeholder="Min year"
      />
    </>
  )
}
