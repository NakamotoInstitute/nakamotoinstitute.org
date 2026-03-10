import { defineConfig } from 'i18next-cli';

export default defineConfig({
  "locales": [
    "en"
  ],
  "extract": {
    "input": [
      "app/**/*.{js,jsx,ts,tsx}"
    ],
    "output": "locales/{{language}}/{{namespace}}.json",
    "defaultNS": "common",
    "functions": [
      "t",
      "*.t"
    ],
    "transComponents": [
      "Trans"
    ]
  },
  "types": {
    "input": [
      "locales/{{language}}/{{namespace}}.json"
    ],
    "output": "src/types/i18next.d.ts"
  }
});