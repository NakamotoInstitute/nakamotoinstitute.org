import { env } from "@/env";

import { Api } from "./generated";
import { client } from "./generated/client.gen";

client.setConfig({
  baseUrl: env.API_URL,
  headers: env.API_KEY ? { "X-API-Key": env.API_KEY } : undefined,

  cache: env.VERCEL_ENV === "development" ? "no-store" : "force-cache",
});

export const api = new Api({ client });
