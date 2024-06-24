import type { Config } from "tailwindcss";
import plugin from "tailwindcss/plugin";
import { PluginAPI } from "tailwindcss/types/config";

const round = (num: number) =>
  num
    .toFixed(7)
    .replace(/(\.[0-9]+?)0+$/, "$1")
    .replace(/\.0$/, "");
const rem = (px: number) => `${round(px / 16)}rem`;
const em = (px: number, base: number) => `${round(px / base)}em`;

const config: Config = {
  content: [
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  safelist: ["twbs-container", "code", "quote", "codeheader", "quoteheader"],
  theme: {
    extend: {
      colors: {
        cream: "#f5f4ef",
        dark: "#212121",
        cardinal: "#c21324", // Cardinal
        windsor: "#442977", // Windsor purple
        winter: "#5b8e7d", // Winter green
        mariner: "#4059ad", // Mariner blue
      },
      fontFamily: {
        serif: ["var(--font-stix)", "Times New Roman", "serif"],
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
            "--tw-prose-body": theme("colors.dark"),
            "--tw-prose-links": theme("colors.dark"),
            "--tw-prose-counters": theme("colors.dark"),
            "--tw-prose-bullets": theme("colors.dark"),
            "--tw-prose-hr": theme("colors.dark"),
            "--tw-prose-quotes": theme("colors.dark"),
            "--tw-prose-quote-borders": theme("colors.dark"),
            "--tw-prose-captions": theme("colors.dark"),
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
            lineHeight: em(26, 16),
            p: {
              marginTop: em(22, 16),
              marginBottom: em(22, 16),
            },
            h2: {
              fontSize: em(18, 16),
              marginTop: em(32, 18),
              marginBottom: em(8, 18),
            },
            h3: {
              fontSize: em(17, 16),
              marginTop: em(32, 17),
              marginBottom: em(8, 17),
            },
            h4: {
              fontSize: em(16, 16),
              marginTop: em(32, 16),
              marginBottom: em(8, 16),
            },
            h5: {
              fontSize: em(16, 16),
              marginTop: em(32, 16),
              marginBottom: em(8, 16),
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
            figcaption: {
              fontSize: em(13, 16),
              lineHeight: round(16 / 13),
            },
            blockquote: {
              fontWeight: 400,
              borderLeft: "1px dashed",
              quotes: null,
            },
            "figure:has(blockquote)": {
              borderLeft: "1px dashed",
              borderColor: "var(--tw-prose-quote-borders)",
            },
            "figure > blockquote": {
              border: "none",
              paddingInlineStart: em(16, 18),
              "& > p:last-of-type": {
                marginBottom: 0,
              },
            },
            "blockquote ~ figcaption": {
              fontSize: em(16, 16),
              fontWeight: 500,
              paddingInlineStart: em(16, 16),
              fontVariantCaps: "small-caps",
              marginTop: em(12, 16),
            },
            "mjx-container": {
              margin: "0.5em 0",
              padding: "0.5em 0",
              overflowX: "scroll",
            },
          },
        },
        lg: {
          css: {
            lineHeight: em(26, 18),
            "ol.references,ul.references": {
              padding: 0,
              "& li": {
                padding: 0,
              },
            },
            p: {
              marginTop: em(28, 18),
              marginBottom: em(28, 18),
            },
            h2: {
              lineHeight: round(28 / 24),
              marginTop: em(40, 24),
              marginBottom: em(16, 24),
            },
            h3: {
              fontSize: em(22, 16),
              lineHeight: round(26 / 22),
              marginTop: em(40, 22),
              marginBottom: em(16, 22),
            },
            h4: {
              fontSize: em(20, 16),
              lineHeight: round(23 / 22),
              marginTop: em(40, 20),
              marginBottom: em(16, 20),
            },
            h5: {
              fontSize: em(18, 16),
              lineHeight: round(21 / 18),
              marginTop: em(40, 18),
              marginBottom: em(16, 18),
            },
            figcaption: {
              fontSize: em(13, 16),
              lineHeight: round(16 / 13),
            },
            "blockquote ~ figcaption": {
              fontSize: em(16, 18),
              marginTop: em(12, 18),
            },
          },
        },
      }),
    },
  },
  plugins: [
    require("@tailwindcss/typography"),
    plugin(({ addUtilities }) => {
      addUtilities({
        ".small-caps": { "font-variant-caps": "small-caps" },
      });
    }),
  ],
};
export default config;
