import { z } from "zod";

export const zEmailSource = z.enum(["cryptography", "bitcoin-list"]);
export type EmailSource = z.infer<typeof zEmailSource>;
