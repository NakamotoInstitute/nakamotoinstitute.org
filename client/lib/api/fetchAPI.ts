const apiBaseUrl = "http://127.0.0.1:5000/api";

export default async function fetchAPI(
  endpoint: string,
  options: RequestInit = {},
) {
  return fetch(`${apiBaseUrl}${endpoint}`, {
    ...options,
    cache:
      process.env.VERCEL_ENV === "development" ? "no-store" : "force-cache",
  });
}
