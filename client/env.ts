import { createEnv } from "@t3-oss/env-nextjs";
import { z } from "zod";

export const env = createEnv({
  server: {
    VERCEL_ENV: z.enum(["development", "preview", "production"]),
    VERCEL_URL: z.string(),
    APP_BASE_URL: z.string().url().optional(),
    SATOSHI_HOST: z.string().optional(),
    API_URL: z.string().url(),
    PORT: z.coerce.number().int().positive().max(65536).default(3000),
    FATHOM_ID: z.string().optional(),
    API_KEY: z.string().optional(),
    CDN_BASE_URL: z.string().url(),
  },
  experimental__runtimeEnv: {},
});

if (env.VERCEL_ENV === "production" && !env.APP_BASE_URL) {
  throw new Error("APP_BASE_URL must be defined when VERCEL_ENV is production");
}
if (env.VERCEL_ENV === "production" && !env.SATOSHI_HOST) {
  throw new Error("SATOSHI_HOST must be defined when VERCEL_ENV is production");
}
if (env.VERCEL_ENV === "production" && !env.FATHOM_ID) {
  throw new Error("FATHOM_ID must be defined when VERCEL_ENV is production");
}
