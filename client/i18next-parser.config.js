module.exports = {
  locales: ["en"],
  defaultNamespace: "common",
  input: ["app/**/*.{js,jsx,ts,tsx}"],
  createOldCatalogs: false,
  lexers: {
    js: [
      {
        namespaceFunctions: [
          "useTranslation",
          "withTranslation",
          "i18nTranslation",
        ],
      },
    ],
  },
};
