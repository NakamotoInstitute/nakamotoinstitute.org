/**
 * Post-process Hey API generated files.
 *
 * Fixes:
 * 1. zod.gen.ts - Convert z.iso.datetime/date() to z.coerce.date() for proper Date objects
 * 2. types.gen.ts - Change date field types from string to Date
 * 3. sdk.gen.ts - Fix ThrowOnError default to match client config
 */

import { readFileSync, writeFileSync } from "fs";
import { join } from "path";

const GENERATED_DIR = join(import.meta.dirname, "../lib/api/generated");

function main() {
  // Fix zod.gen.ts - convert ISO date validators to coerce.date()
  const zodPath = join(GENERATED_DIR, "zod.gen.ts");
  let zod = readFileSync(zodPath, "utf-8");
  zod = zod.replace(/z\.iso\.datetime\(\{[^}]*\}\)/g, "z.coerce.date()");
  zod = zod.replace(/z\.iso\.date\(\)/g, "z.coerce.date()");
  writeFileSync(zodPath, zod);

  // Fix types.gen.ts - date fields should be Date, not string
  const typesPath = join(GENERATED_DIR, "types.gen.ts");
  let types = readFileSync(typesPath, "utf-8");
  types = types.replace(/((?:date|added)\??): string(;| \| null;)/g, "$1: Date$2");
  writeFileSync(typesPath, types);

  // Fix sdk.gen.ts - ThrowOnError default should match client config
  // Also change responseValidator to responseTransformer so zod coercion is used
  const sdkPath = join(GENERATED_DIR, "sdk.gen.ts");
  let sdk = readFileSync(sdkPath, "utf-8");
  sdk = sdk.replace(/ThrowOnError extends boolean = false/g, "ThrowOnError extends boolean = true");
  sdk = sdk.replace(/responseValidator/g, "responseTransformer");
  writeFileSync(sdkPath, sdk);

  console.log("Post-processed generated API files");
}

main();
