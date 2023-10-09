import { getNumericId } from "@/utils/strings";
import fetchAPI from "./fetchAPI";
import {
  EmailSource,
  zEmailIndex,
  zEmailDetail,
  zEmailThreadDetail,
  zEmailThreadIndex,
} from "./schemas/emails";

export async function getSatoshiEmails() {
  const res = await fetchAPI("/satoshi/emails");
  return zEmailIndex.parse(await res.json());
}

export async function getEmail(
  source: EmailSource,
  satoshiId: string | number,
) {
  const satoshiIdNum = getNumericId(satoshiId);
  const res = await fetchAPI(`/satoshi/emails/${source}/${satoshiIdNum}`);
  return zEmailDetail.parse(await res.json());
}

export async function getSatoshiEmailsBySource(source: EmailSource) {
  const res = await fetchAPI(`/satoshi/emails/${source}`);
  return zEmailIndex.parse(await res.json());
}

export async function getEmailThreads() {
  const res = await fetchAPI("/satoshi/emails/threads");
  return zEmailThreadIndex.parse(await res.json());
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
  return zEmailThreadDetail.parse(await res.json());
}

export async function getEmailThreadsBySource(source: EmailSource) {
  const res = await fetchAPI(`/satoshi/emails/${source}/threads`);
  return zEmailThreadIndex.parse(await res.json());
}
