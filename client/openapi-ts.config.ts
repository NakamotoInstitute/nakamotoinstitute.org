import { defineConfig } from "@hey-api/openapi-ts";

// Convert snake_case to camelCase
function toCamelCase(str: string): string {
  return str.replace(/_([a-z])/g, (_, c) => c.toUpperCase());
}

export default defineConfig({
  input: "./openapi.json",
  output: {
    path: "lib/api/generated",
  },
  postProcess: ["prettier"],
  plugins: [
    {
      name: "@hey-api/typescript",
      enums: "javascript",
    },
    {
      name: "zod",
      dates: { offset: true, local: true },
    },
    "@hey-api/client-next",
    {
      name: "@hey-api/sdk",
      validator: "zod",
      operations: {
        strategy: "single",
        containerName: "api",
        // Parse "authors-get_author" -> ["authors", "getAuthor"]
        nesting(operation) {
          const id = operation.operationId || "";
          const [namespace, ...rest] = id.split("-");
          const method = toCamelCase(rest.join("-"));
          return [namespace, method];
        },
      },
    },
  ],
});
