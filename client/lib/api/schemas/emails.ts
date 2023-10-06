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
export type Email = z.infer<typeof zSatoshiEmail>;

export const zThreadEmail = zEmail.extend({
  parent: zEmail.nullable(),
});
export type ThreadEmail = z.infer<typeof zThreadEmail>;

export const zEmailIndexResponse = z.array(zSatoshiEmail);

export const zEmailResponse = z.object({
  email: zSatoshiEmail,
  previous: zSatoshiEmail.nullable(),
  next: zSatoshiEmail.nullable(),
});

export const zEmailThreadBase = z.object({
  id: z.number().int().min(1),
  title: z.string(),
  source: zEmailSource,
  date: z.coerce.date(),
});
export type EmailThreadBase = z.infer<typeof zEmailThreadBase>;

export const zEmailThreadIndexResponse = z.array(zEmailThreadBase);

export const zEmailThread = z.object({
  thread: zEmailThreadBase,
  emails: z.array(zThreadEmail),
  previous: zEmailThreadBase.nullable(),
  next: zEmailThreadBase.nullable(),
});
