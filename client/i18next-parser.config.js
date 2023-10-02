const languages = require("./locales/languages.json");

module.exports = {
  locales: languages.map((lang) => lang.code),
  defaultValue: (lang, _, key) => {
    if (lang === "en") {
      return key;
    }
    return "";
  },
  defaultNamespace: "common",
  input: ["app/**/*.{js,jsx,ts,tsx}"],
  createOldCatalogs: false,
  keySeparator: false,
  namespaceSeparator: false,
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
