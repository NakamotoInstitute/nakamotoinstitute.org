import { notFound } from "next/navigation";

const API_ID_MAX = 2_147_483_646;

export async function getOrNotFound<T>(
  apiCall: Promise<{
    data: T | undefined;
    error: unknown;
    response?: Response | undefined;
  }>,
): Promise<T> {
  const result = await apiCall;
  if (result.data === undefined) {
    if (result.response?.status === 404 || result.response?.status === 422) {
      notFound();
    }
    throw result.error;
  }
  return result.data;
}

export function parseApiIdOrNotFound(id: string): number {
  if (!/^\d+$/.test(id)) notFound();

  const parsed = Number(id);
  if (parsed < 1 || parsed > API_ID_MAX || String(parsed) !== id) notFound();

  return parsed;
}

export function getStaticParamsOrThrow<T>(result: {
  data: T | undefined;
  error: unknown;
}): T {
  if (result.error || result.data === undefined) {
    throw result.error ?? new Error("Failed to fetch static params");
  }

  return result.data;
}
