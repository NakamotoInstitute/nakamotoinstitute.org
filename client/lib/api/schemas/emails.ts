import { z } from "zod";

export const zEmailSource = z.enum(["cryptography", "bitcoin-list"]);
export type EmailSource = z.infer<typeof zEmailSource>;

const zEmailBase = z.object({
  date: z.coerce.date(),
  subject: z.string(),
  text: z.string(),
  source: zEmailSource,
  sourceId: z.string(),
  url: z.string(),
  threadId: z.number().int().min(1),
});

export const zEmail = zEmailBase.extend({
  sentFrom: z.string(),
  parentId: z.number().int().min(1).nullable(),
  satoshiId: z.number().int().min(1).nullable(),
  replies: z.array(z.string()),
});

export const zSatoshiEmail = zEmailBase.extend({
  satoshiId: z.number().int().min(1),
});
export type SatoshiEmail = z.infer<typeof zSatoshiEmail>;

export const zThreadEmail = zEmail.extend({
  parent: zEmail.nullable(),
});
export type ThreadEmail = z.infer<typeof zThreadEmail>;

export const zEmailIndex = z.array(zSatoshiEmail);

export const zEmailDetail = z.object({
  email: zSatoshiEmail,
  previous: zSatoshiEmail.nullable(),
  next: zSatoshiEmail.nullable(),
});

export const zEmailThread = z.object({
  id: z.number().int().min(1),
  title: z.string(),
  source: zEmailSource,
  date: z.coerce.date(),
});
export type EmailThread = z.infer<typeof zEmailThread>;

export const zEmailThreadIndex = z.array(zEmailThread);

export const zEmailThreadDetail = z.object({
  thread: zEmailThread,
  emails: z.array(zThreadEmail),
  previous: zEmailThread.nullable(),
  next: zEmailThread.nullable(),
});
