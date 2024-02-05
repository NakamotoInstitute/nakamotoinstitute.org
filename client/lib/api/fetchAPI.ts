const apiBaseUrl = (() => {
  const environ = process.env.VERCEL_ENV;
  if (environ === "development") {
    return "http://127.0.0.1:8000";
  }
  return process.env.API_URL as string;
})();

export default async function fetchAPI(
  endpoint: string,
  options: RequestInit = {},
) {
  const headers: HeadersInit | undefined = process.env.API_KEY
    ? { "X-API-Key": process.env.API_KEY, ...options.headers }
    : options.headers;
  return fetch(`${apiBaseUrl}${endpoint}`, {
    ...options,
    cache:
      process.env.VERCEL_ENV === "development" ? "no-store" : "force-cache",
    headers,
  });
}
