import clsx from "clsx";
import { TFunction } from "i18next";

type ToggleLinksProps = {
  t: TFunction<string, string>;
  active: "individual" | "threads";
  href: string;
  isMobile?: boolean;
};

async function ToggleLinks({
  active,
  href,
  t,
  isMobile = false,
}: ToggleLinksProps) {
  return (
    <div
      className={clsx("flex rounded-lg bg-sand p-0.5 text-center", {
        "mt-4 md:hidden": isMobile,
        "hidden md:flex": !isMobile,
      })}
    >
      {active === "individual" ? (
        <>
          <span
            className={clsx(
              "cursor-pointer rounded-lg bg-white px-4 py-1 shadow",
              { grow: isMobile },
            )}
          >
            {t("individual")}
          </span>
          <a href={href} className={clsx("px-4 py-1", { grow: isMobile })}>
            {t("threads")}
          </a>
        </>
      ) : (
        <>
          <a href={href} className={clsx("px-4 py-1", { grow: isMobile })}>
            {t("individual")}
          </a>
          <span
            className={clsx(
              "cursor-pointer rounded-lg bg-white px-4 py-1 shadow",
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
  sourceLinks: SourceLink[];
  toggleLinks: ToggleLinks;
};

export async function IndexNavigation({
  t,
  sourceLinks,
  toggleLinks,
}: IndexNavigationProps) {
  const toggleLinksProps = { ...toggleLinks, t };

  return (
    <div>
      <div className="flex items-center justify-between border-b-1 border-dashed border-taupe-light">
        <ul className="flex gap-x-4 text-taupe">
          {sourceLinks.map((sourceLink) => (
            <li
              key={sourceLink.name}
              className={clsx(
                "py-3",
                sourceLink.active &&
                  "-mb-[1px] border-b-2 border-cardinal text-dark",
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
