import { api } from "./client";
import type { LoginRequest, TokenResponse } from "../types/auth";

/**
 * Authenticate user and return JWT token.
 */
export async function login(
  username: string,
  password: string,
): Promise<string> {
  const payload: LoginRequest = { username, password };
  const { data } = await api.post<TokenResponse>("/api/login", payload);
  return data.access_token;
}
