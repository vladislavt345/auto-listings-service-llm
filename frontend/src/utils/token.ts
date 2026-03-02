const TOKEN_KEY = 'als_token'

/**
 * Persist access token.
 */
export function saveToken(token: string): void {
  localStorage.setItem(TOKEN_KEY, token)
}

/**
 * Read access token.
 */
export function getToken(): string | null {
  return localStorage.getItem(TOKEN_KEY)
}

/**
 * Remove stored access token.
 */
export function clearToken(): void {
  localStorage.removeItem(TOKEN_KEY)
}

/**
 * Check whether access token exists.
 */
export function isAuthenticated(): boolean {
  return Boolean(getToken())
}
