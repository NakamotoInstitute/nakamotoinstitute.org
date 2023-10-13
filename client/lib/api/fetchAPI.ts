const apiBaseUrl = (() => {
  const environ = process.env.VERCEL_ENV;
  if (environ === "development") {
    return "http://127.0.0.1:5000";
  }
  return process.env.API_URL as string;
})();

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
