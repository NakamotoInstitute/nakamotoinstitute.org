/**
 * Post-process Hey API generated files.
 *
 * Fixes:
 * 1. types.gen.ts - Change date field types from string to Date
 * 2. sdk.gen.ts - Change responseValidator to responseTransformer so zod coercion is used
 */

import { readFileSync, writeFileSync } from "fs";
import { join } from "path";

const GENERATED_DIR = join(import.meta.dirname, "../lib/api/generated");

function main() {
  // Fix types.gen.ts - date fields should be Date, not string
  const typesPath = join(GENERATED_DIR, "types.gen.ts");
  let types = readFileSync(typesPath, "utf-8");
  types = types.replace(/((?:date|added)\??): string(;| \| null;)/g, "$1: Date$2");
  writeFileSync(typesPath, types);

  // Fix sdk.gen.ts - change responseValidator to responseTransformer so zod coercion is used
  const sdkPath = join(GENERATED_DIR, "sdk.gen.ts");
  let sdk = readFileSync(sdkPath, "utf-8");
  sdk = sdk.replace(/responseValidator/g, "responseTransformer");
  writeFileSync(sdkPath, sdk);

  console.log("Post-processed generated API files");
}

main();
