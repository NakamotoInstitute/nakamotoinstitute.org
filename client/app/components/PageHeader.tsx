import { ReactNode } from "react";

type PageHeaderProps = {
  title: string;
  superTitle?: string;
  children?: ReactNode;
};

export function PageHeader({ title, superTitle, children }: PageHeaderProps) {
  return (
    <header className="text-center">
      {superTitle ? <h2 className="text-xl">{superTitle}</h2> : null}
      <h1 className="text-4xl">{title}</h1>
      {children}
      <hr className="my-4" />
    </header>
  );
}
