import type { Config } from "tailwindcss";
import { PluginAPI } from "tailwindcss/types/config";

const config: Config = {
  content: [
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  safelist: ["twbs-container", "code", "quote", "codeheader", "quoteheader"],
  theme: {
    extend: {
      fontFamily: {
        sans: [
          "system-ui",
          "-apple-system",
          '"Segoe UI"',
          "Roboto",
          '"Helvetica Neue"',
          '"Noto Sans"',
          '"Liberation Sans"',
          "Arial",
          "sans-serif",
          '"Apple Color Emoji"',
          '"Segoe UI Emoji"',
          '"Segoe UI Symbol"',
          '"Noto Color Emoji"',
        ],
        mono: ["var(--font-ibm-plex-mono)", "Courier New", "monospace"],
      },
      fontSize: {
        reg: ["1.5rem", { lineHeight: "1.5", letterSpacing: "-0.01em" }],
      },
      borderWidth: {
        1: "1px",
      },
      letterSpacing: {
        normal: "-0.01em",
      },
      margin: {
        18: "4.5rem",
      },
      typography: ({ theme }: PluginAPI) => ({
        DEFAULT: {
          css: {
            "ol.references,ul.references": {
              listStyle: "none",
              padding: 0,
              "& li": {
                padding: 0,
              },
            },
            "blockquote p:first-of-type::before": null,
            "blockquote p:last-of-type::after": null,
            ".footnotes": {
              fontSize: "1rem",
            },
            pre: {
              strong: { color: "var(--tw-prose-pre-code)" },
            },
            figure: {
              "& > img": {
                marginLeft: "auto",
                marginRight: "auto",
              },
              "& > .img-container": {
                display: "flex",
                flexWrap: "wrap",
                alignItems: "center",
                justifyContent: "center",
                "--tw-prose-img-gap": "12px",
                gap: "var(--tw-prose-img-gap)",
                "& img": {
                  margin: 0,
                },
                "& > *": {
                  "@media (min-width: 65ch)": {
                    flexBasis: "calc(50% - var(--tw-prose-img-gap))",
                  },
                  flexShrink: "0",
                  flexGrow: "1",
                  width: "100%",
                  maxWidth: "max-content",
                },
              },
            },
            "mjx-container": {
              margin: "0.5em 0",
              padding: "0.5em 0",
              overflowX: "scroll",
            },
          },
        },
      }),
    },
  },
  plugins: [require("@tailwindcss/typography")],
};
export default config;
