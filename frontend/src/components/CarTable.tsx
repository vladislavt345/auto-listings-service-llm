import type { ReactElement } from 'react'

import type { Car } from '../types/car'

type Props = {
  cars: Car[]
}

/**
 * Cars data table.
 */
export function CarTable({ cars }: Props): ReactElement {
  return (
    <table>
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
            <td>{car.make}</td>
            <td>{car.model}</td>
            <td>{car.year}</td>
            <td>{car.price}</td>
            <td>{car.color}</td>
            <td>
              <a href={car.source_url} target="_blank" rel="noreferrer">
                Open
              </a>
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  )
}
