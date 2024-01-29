module.exports = {
    plugins: [
        'prettier-plugin-tailwindcss',
        '@trivago/prettier-plugin-sort-imports',
    ],
    importOrder: ['^@/(.*)$', '^@main/(.*)$', '^@satoshi/(.*)$', '^[./]'],
    importOrderSeparation: true,
    importOrderSortSpecifiers: true,
};
