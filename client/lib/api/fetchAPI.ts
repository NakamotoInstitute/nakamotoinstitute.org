import { env } from "@/env";

export default async function fetchAPI(
  endpoint: string,
  options: RequestInit = {},
) {
  const headers: HeadersInit | undefined = env.API_KEY
    ? { "X-API-Key": env.API_KEY, ...options.headers }
    : options.headers;
  return fetch(`${env.API_URL}${endpoint}`, {
    ...options,
    cache: env.VERCEL_ENV === "development" ? "no-store" : "force-cache",
    headers,
  });
}
