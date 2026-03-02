import type { ReactElement } from 'react'
import type { Car } from '../types/car'

type Props = {
  cars: Car[]
}

export function CarTable({ cars }: Props): ReactElement {
  if (cars.length === 0) {
    return (
      <div className="table-empty">No listings found</div>
    )
  }

  return (
    <table className="cars-table">
      <thead>
        <tr>
          <th>Make</th>
          <th>Model</th>
          <th>Year</th>
          <th>Price</th>
          <th>Color</th>
          <th>Source</th>
        </tr>
      </thead>
      <tbody>
        {cars.map((car: Car) => (
          <tr key={car.id}>
            <td className="c-make">{car.make}</td>
            <td>{car.model}</td>
            <td className="c-year">{car.year}</td>
            <td className="c-price">{Number(car.price).toLocaleString()}</td>
            <td>
              <span className="color-pill">
                <span className="color-dot" />
                {car.color}
              </span>
            </td>
            <td>
              <a className="link-open" href={car.source_url} target="_blank" rel="noreferrer">
                Open
              </a>
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  )
}
