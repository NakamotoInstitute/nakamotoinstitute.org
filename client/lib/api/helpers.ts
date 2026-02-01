import { notFound } from "next/navigation";

export async function getOrNotFound<T>(
  apiCall: Promise<
    ({ data: T; error: undefined } | { data: undefined; error: unknown }) & {
      response: Response;
    }
  >,
): Promise<T> {
  const result = await apiCall;
  if (result.data === undefined) {
    if (result.response.status === 404) notFound();
    throw result.error;
  }
  return result.data;
}
