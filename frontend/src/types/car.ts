export type Car = {
  id: number;
  make: string;
  model: string;
  year: number;
  price: string;
  color: string;
  source_url: string;
};

export type CarFilters = {
  make?: string;
  model?: string;
  color?: string;
  max_price?: number;
  min_year?: number;
  limit?: number;
  offset?: number;
};
