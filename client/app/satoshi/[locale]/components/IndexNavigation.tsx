import clsx from "clsx";
import { TFunction } from "i18next";

type ToggleLinksProps = {
  t: TFunction<string, string>;
  active: "individual" | "threads";
  href: string;
  individualLabel: string;
  isMobile?: boolean;
};

async function ToggleLinks({
  active,
  href,
  t,
  individualLabel,
  isMobile = false,
}: ToggleLinksProps) {
  return (
    <div
      className={clsx("bg-sand flex rounded-lg p-0.5 text-center", {
        "mt-4 md:hidden": isMobile,
        "hidden md:flex": !isMobile,
      })}
    >
      {active === "individual" ? (
        <>
          <span
            className={clsx(
              "cursor-pointer rounded-lg bg-white px-4 py-1 shadow-sm",
              { grow: isMobile },
            )}
          >
            {individualLabel}
          </span>
          <a href={href} className={clsx("px-4 py-1", { grow: isMobile })}>
            {t("threads")}
          </a>
        </>
      ) : (
        <>
          <a href={href} className={clsx("px-4 py-1", { grow: isMobile })}>
            {individualLabel}
          </a>
          <span
            className={clsx(
              "cursor-pointer rounded-lg bg-white px-4 py-1 shadow-sm",
              { grow: isMobile },
            )}
          >
            {t("threads")}
          </span>
        </>
      )}
    </div>
  );
}

export type SourceLink =
  | { name: string; href: string; active?: false }
  | { name: string; active: true };

export type ToggleLinks = { active: "individual" | "threads"; href: string };

export type IndexNavigationProps = {
  t: TFunction<string, string>;
  type: "emails" | "posts";
  sourceLinks: SourceLink[];
  toggleLinks: ToggleLinks;
};

export async function IndexNavigation({
  t,
  type,
  sourceLinks,
  toggleLinks,
}: IndexNavigationProps) {
  const individualLabel = type === "emails" ? t("emails") : t("posts");
  const toggleLinksProps = { ...toggleLinks, t, individualLabel };

  return (
    <div>
      <div className="border-taupe-light flex items-center justify-between border-b border-dashed">
        <ul className="text-taupe flex gap-x-4">
          {sourceLinks.map((sourceLink) => (
            <li
              key={sourceLink.name}
              className={clsx(
                "py-3",
                sourceLink.active &&
                  "border-cardinal text-dark -mb-[1px] border-b-2",
              )}
            >
              {sourceLink.active ? (
                <span className="cursor-pointer">{sourceLink.name}</span>
              ) : (
                <a href={sourceLink.href}>{sourceLink.name}</a>
              )}
            </li>
          ))}
        </ul>
        <ToggleLinks {...toggleLinksProps} />
      </div>
      <ToggleLinks {...toggleLinksProps} isMobile />
    </div>
  );
}
