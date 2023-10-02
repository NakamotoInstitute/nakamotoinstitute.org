import type { Config } from "tailwindcss";
import { PluginAPI } from "tailwindcss/types/config";

const config: Config = {
  content: [
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    fontFamily: {
      serif: ["var(--font-stix)", "Times New Roman", "serif"],
      mono: ["var(--font-ibm-plex-mono)", "Courier New", "monospace"],
    },
    extend: {
      colors: {
        bone: "#FDE6E0",
        night: "#212121",
        cardinal: "#C21324", // Cardinal
        windsor: "#442977", // Windsor purple
        winter: "#5B8E7D", // Winter green
        mariner: "#4059AD", // Mariner blue
        flax: "#F4E98C",
        gray: "#F5F5F5",
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
            "--tw-prose-body": theme("colors.night"),
            "--tw-prose-headings": theme("colors.night"),
            "--tw-prose-lead": theme("colors.night"),
            "--tw-prose-links": theme("colors.night"),
            "--tw-prose-bold": theme("colors.night"),
            "--tw-prose-counters": theme("colors.night"),
            "--tw-prose-bullets": theme("colors.night"),
            "--tw-prose-hr": theme("colors.night"),
            "--tw-prose-quotes": theme("colors.night"),
            "--tw-prose-quote-borders": theme("colors.night"),
            fontSize: "1.25rem",
            lineHeight: 1.5,
            fontWeight: 500,
            "blockquote p:first-of-type::before": null,
            "blockquote p:last-of-type::after": null,
            ".footnotes": {
              fontSize: "1rem",
            },
            "figure > .img-container": {
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
        },
      }),
    },
  },
  plugins: [require("@tailwindcss/typography")],
};
export default config;
