import { IndexNavigation, IndexNavigationProps } from "./IndexNavigation";

export type SourceLink =
  | { name: string; href: string; active?: false }
  | { name: string; active: true };

export type ToggleLinks = { active: "individual" | "threads"; href: string };

export async function IndexHeader({ t, type, ...rest }: IndexNavigationProps) {
  return (
    <header>
      <h1 className="mb-2 text-4xl font-semibold">
        {type === "emails" ? t("emails") : t("forum_posts")}
      </h1>
      <IndexNavigation t={t} type={type} {...rest} />
    </header>
  );
}
