import type { InternalAxiosRequestConfig } from "axios";
import axios from "axios";

import { getToken } from "../utils/token";

const API_BASE: string = import.meta.env.VITE_API_URL || "";

/**
 * Shared API client instance.
 */
export const api = axios.create({
  baseURL: API_BASE,
});

api.interceptors.request.use(
  (config: InternalAxiosRequestConfig): InternalAxiosRequestConfig => {
    const token = getToken();
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
);
