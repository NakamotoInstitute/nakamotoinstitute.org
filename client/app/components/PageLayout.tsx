import clsx from "clsx";
import { ReactNode } from "react";

export function PageLayout({
  className,
  locale,
  children,
}: {
  className?: string;
  locale: Locale;
  children: ReactNode | ReactNode[];
}) {
  return (
    <body className="flex min-h-screen flex-col">
      <main
        className={clsx(
          "mx-auto w-full max-w-7xl flex-grow px-2 py-12 md:px-6 lg:px-8",
          className,
        )}
      >
        {children}
      </main>
    </body>
  );
}
