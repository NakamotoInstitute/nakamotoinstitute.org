import { NextRequest } from "next/server";

/**
 * In-memory fixed-window per-IP rate limiter for the public search route
 * handler (S6/S9). Single-region only — swap for Upstash/Vercel KV if the route
 * is ever served from multiple regions. Defaults: 30 requests per 10s window.
 */
const WINDOW_MS = 10_000;
const MAX_REQUESTS = 30;
const MAX_TRACKED_IPS = 10_000;

type Bucket = { count: number; resetAt: number };

const buckets = new Map<string, Bucket>();

function clientIp(req: NextRequest): string {
  const forwarded = req.headers.get("x-forwarded-for");
  if (forwarded) return forwarded.split(",")[0]!.trim();
  return req.headers.get("x-real-ip") ?? "unknown";
}

export function rateLimit(req: NextRequest): {
  allowed: boolean;
  retryAfter: number;
} {
  const ip = clientIp(req);
  const now = Date.now();
  const bucket = buckets.get(ip);

  if (!bucket || now >= bucket.resetAt) {
    if (buckets.size >= MAX_TRACKED_IPS) {
      // Opportunistic cleanup of expired buckets to bound memory.
      for (const [key, value] of buckets) {
        if (now >= value.resetAt) buckets.delete(key);
      }
      // Hard cap: if the table is still full (e.g. a burst of distinct or spoofed
      // IPs within one window, none yet expired), stop tracking new keys and fail
      // open rather than grow unbounded. The backend statement_timeout stays the
      // real backstop.
      if (buckets.size >= MAX_TRACKED_IPS) {
        return { allowed: true, retryAfter: 0 };
      }
    }
    buckets.set(ip, { count: 1, resetAt: now + WINDOW_MS });
    return { allowed: true, retryAfter: 0 };
  }

  if (bucket.count >= MAX_REQUESTS) {
    return { allowed: false, retryAfter: Math.ceil((bucket.resetAt - now) / 1000) };
  }

  bucket.count += 1;
  return { allowed: true, retryAfter: 0 };
}
