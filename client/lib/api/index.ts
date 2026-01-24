// Convenience arrays derived from server enums
import { EmailSource, ForumPostSource } from "./generated";

// Re-export all generated types
export * from "./generated";

// Client instance
export { api } from "./client";

// External price API
export { fetchPriceHistory, type Price } from "./prices";

export const EMAIL_SOURCES = Object.values(EmailSource);
export const FORUM_POST_SOURCES = Object.values(ForumPostSource);
