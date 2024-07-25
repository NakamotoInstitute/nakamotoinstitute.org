module.exports = {
  plugins: [
    "@trivago/prettier-plugin-sort-imports",
    "prettier-plugin-tailwindcss",
  ],
  importOrder: ["^@/(.*)$", "^@main/(.*)$", "^@satoshi/(.*)$", "^[./]"],
  importOrderSeparation: true,
  importOrderSortSpecifiers: true,
  tailwindFunctions: ["clsx"],
};
