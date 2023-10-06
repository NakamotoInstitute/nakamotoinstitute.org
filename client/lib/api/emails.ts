import { getNumericId } from "@/utils/strings";
import fetchAPI from "./fetchAPI";
import {
  EmailSource,
  zEmailIndexResponse,
  zEmailResponse,
  zEmailThread,
  zEmailThreadIndexResponse,
} from "./schemas/emails";

export async function getSatoshiEmails() {
  const res = await fetchAPI("/satoshi/emails");
  return zEmailIndexResponse.parse(await res.json());
}

export async function getEmail(
  source: EmailSource,
  satoshiId: string | number,
) {
  const satoshiIdNum = getNumericId(satoshiId);
  const res = await fetchAPI(`/satoshi/emails/${source}/${satoshiIdNum}`);
  return zEmailResponse.parse(await res.json());
}

export async function getSatoshiEmailsBySource(source: EmailSource) {
  const res = await fetchAPI(`/satoshi/emails/${source}`);
  return zEmailIndexResponse.parse(await res.json());
}

export async function getEmailThreads() {
  const res = await fetchAPI("/satoshi/emails/threads");
  return zEmailThreadIndexResponse.parse(await res.json());
}

export async function getEmailThread(
  source: EmailSource,
  threadId: string | number,
  satoshiOnly: boolean = false,
) {
  const threadIdNum = getNumericId(threadId);
  const res = await fetchAPI(
    `/satoshi/emails/${source}/threads/${threadIdNum}?satoshi=${satoshiOnly}`,
  );
  return zEmailThread.parse(await res.json());
}

export async function getEmailThreadsBySource(source: EmailSource) {
  const res = await fetchAPI(`/satoshi/emails/${source}/threads`);
  return zEmailThreadIndexResponse.parse(await res.json());
}
