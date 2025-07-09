import { createEnv } from "@t3-oss/env-nextjs";
import { vercel } from "@t3-oss/env-nextjs/presets-zod";
import { z } from "zod";

const isProd = process.env.VERCEL_ENV === "production";
const isPreview = process.env.VERCEL_ENV === "preview";

export const env = createEnv({
  server: {
    VERCEL_ENV: z
      .enum(["development", "preview", "production"])
      .default("development"),
    VERCEL_URL:
      isProd || isPreview
        ? z.string()
        : z.string().optional().default("localhost:3000"),
    MAP_DOMAIN: isProd
      ? z
          .string()
          .optional()
          .transform(() => true)
      : z
          .string()
          .optional()
          .transform((s) => s === undefined || s === "true"),
    API_URL:
      isProd || isPreview ? z.url() : z.url().default("http://127.0.0.1:8000"),
    FATHOM_ID: isProd ? z.string() : z.string().optional(),
    API_KEY: isProd ? z.string() : z.string().optional(),
    CDN_BASE_URL:
      isProd || isPreview
        ? z.url()
        : z.url().default("http://localhost:8000/static"),
  },
  experimental__runtimeEnv: process.env,
  extends: [vercel()],
});
