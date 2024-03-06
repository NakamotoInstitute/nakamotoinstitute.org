import { env } from "@/env";

const apiBaseUrl = (() => {
  const environ = env.VERCEL_ENV;
  if (environ === "development") {
    return "http://127.0.0.1:8000";
  }
  return env.API_URL;
})();

export default async function fetchAPI(
  endpoint: string,
  options: RequestInit = {},
) {
  const headers: HeadersInit | undefined = env.API_KEY
    ? { "X-API-Key": env.API_KEY, ...options.headers }
    : options.headers;
  return fetch(`${apiBaseUrl}${endpoint}`, {
    ...options,
    cache: env.VERCEL_ENV === "development" ? "no-store" : "force-cache",
    headers,
  });
}
