import { createEnv } from "@t3-oss/env-nextjs";
import { z } from "zod";

export const env = createEnv({
  server: {
    VERCEL_ENV: z.enum(["development", "preview", "production"]),
    VERCEL_URL: z.string(),
    APP_BASE_URL: z.string().url(),
    SATOSHI_HOST: z.string(),
    API_URL: z.string().url(),
    PORT: z.coerce.number().int().positive().max(65536).default(3000),
    FATHOM_ID: z.string(),
    API_KEY: z.string().optional(),
    CDN_BASE_URL: z.string().url(),
  },
  experimental__runtimeEnv: {},
});
