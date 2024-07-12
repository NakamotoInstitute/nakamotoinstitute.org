import { IndexNavigation, IndexNavigationProps } from "./IndexNavigation";

export type SourceLink =
  | { name: string; href: string; active?: false }
  | { name: string; active: true };

export type ToggleLinks = { active: "individual" | "threads"; href: string };

export type IndexHeaderProps = {
  title: string;
} & IndexNavigationProps;

export async function IndexHeader({ title, ...rest }: IndexHeaderProps) {
  return (
    <header className="mb-6">
      <h1 className="mb-2 text-4xl font-semibold">{title}</h1>
      <IndexNavigation {...rest} />
    </header>
  );
}
