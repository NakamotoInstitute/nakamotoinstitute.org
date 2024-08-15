import { z } from "zod";

export const EMAIL_SOURCES = [
  "cryptography",
  "bitcoin-list",
  "p2p-research",
] as const;
export const zEmailSource = z.enum(EMAIL_SOURCES);
export type EmailSource = z.infer<typeof zEmailSource>;

const zEmailBase = z.object({
  date: z.coerce.date(),
  sentFrom: z.string(),
  subject: z.string(),
  text: z.string(),
  source: zEmailSource,
  sourceId: z.string(),
  url: z.string(),
  threadId: z.number().int().min(1),
});

export const zEmail = zEmailBase.extend({
  parentId: z.number().int().min(1).nullable(),
  satoshiId: z.number().int().min(1).nullable(),
});

export const zSatoshiEmail = zEmailBase.extend({
  satoshiId: z.number().int().min(1),
});
export type SatoshiEmail = z.infer<typeof zSatoshiEmail>;

export const zEmailWithParent = zEmail.extend({
  parent: zEmail.nullable(),
  replies: z.array(z.string()),
});
export type EmailWithParent = z.infer<typeof zEmailWithParent>;

export const zEmailIndex = z.array(zSatoshiEmail);

export const zEmailDetail = z.object({
  email: zSatoshiEmail,
  previous: zSatoshiEmail.nullable(),
  next: zSatoshiEmail.nullable(),
});
export type EmailDetail = z.infer<typeof zEmailDetail>;

export const zEmailThread = z.object({
  id: z.number().int().min(1),
  title: z.string(),
  source: zEmailSource,
  date: z.coerce.date(),
  url: z.string(),
});
export type EmailThread = z.infer<typeof zEmailThread>;

export const zEmailThreadIndex = z.array(zEmailThread);

export const zEmailThreadDetail = z.object({
  thread: zEmailThread,
  emails: z.array(zEmailWithParent),
  previous: zEmailThread.nullable(),
  next: zEmailThread.nullable(),
});
