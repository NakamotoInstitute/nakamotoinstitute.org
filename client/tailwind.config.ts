import typography from "@tailwindcss/typography";
import type { Config } from "tailwindcss";

const round = (num: number) =>
  num
    .toFixed(7)
    .replace(/(\.[0-9]+?)0+$/, "$1")
    .replace(/\.0$/, "");
const em = (px: number, base: number) => `${round(px / base)}em`;

const config: Config = {
  content: [
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      typography: {
        DEFAULT: {
          css: {
            "--tw-prose-body": "var(--color-dark)",
            "--tw-prose-links": "var(--color-dark)",
            "--tw-prose-counters": "var(--color-dark)",
            "--tw-prose-bullets": "var(--color-dark)",
            "--tw-prose-hr": "var(--color-dark)",
            "--tw-prose-quotes": "var(--color-dark)",
            "--tw-prose-quote-borders": "var(--color-dark)",
            "--tw-prose-captions": "var(--color-dark)",
            "--tw-prose-code": "var(--color-dark)",
            "--tw-prose-pre-code": "var(--color-dark)",
            "--tw-prose-pre-bg": "var(--color-white)",
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
            maxWidth: "var(--spacing-prose)",
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
            code: {
              color: "var(--tw-prose-code)",
              fontWeight: "600",
            },
            "code::before": null,
            "code::after": null,
            pre: {
              border: "1px dashed",
              strong: { color: "var(--tw-prose-pre-code)" },
            },
            figure: {
              "& > img": {
                marginLeft: "auto",
                marginRight: "auto",
                "&.img-dark-bg": {
                  backgroundColor: "var(--tw-prose-pre-code)",
                  padding: "0.5rem",
                },
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
              borderInlineStart: "1px dashed",
              quotes: null,
            },
            "figure:has(blockquote)": {
              borderInlineStart: "1px dashed",
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
              fontSize: em(15, 16),
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
            "ol.bibliography,ul.bibliography": {
              paddingInlineStart: em(40, 16),
              li: {
                listStyle: "none",
                textIndent: em(-40, 16),
              },
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
              fontSize: em(24, 18),
              lineHeight: round(28 / 24),
              marginTop: em(40, 24),
              marginBottom: em(16, 24),
            },
            h3: {
              fontSize: em(22, 18),
              lineHeight: round(26 / 22),
              marginTop: em(40, 22),
              marginBottom: em(16, 22),
            },
            h4: {
              fontSize: em(20, 18),
              lineHeight: round(23 / 22),
              marginTop: em(40, 20),
              marginBottom: em(16, 20),
            },
            h5: {
              fontSize: em(18, 18),
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
      },
    },
  },
  plugins: [typography],
};
export default config;
