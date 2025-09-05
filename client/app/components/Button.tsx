import clsx from "clsx";
import Link, { LinkProps } from "next/link";

export type ButtonLinkProps = Omit<
  React.AnchorHTMLAttributes<HTMLAnchorElement>,
  keyof LinkProps
> &
  LinkProps & {
    className?: string;
    variant?: "primary" | "secondary";
  };

export const ButtonLink = ({
  className,
  variant = "primary",
  href,
  children,
  ...props
}: ButtonLinkProps) => {
  return (
    <Link
      href={href}
      className={clsx(
        "ring-offset-background focus-visible:ring-ring inline-flex h-10 items-center justify-center px-4 py-3 text-sm font-medium whitespace-nowrap transition-colors focus-visible:ring-2 focus-visible:ring-offset-2 focus-visible:outline-hidden disabled:pointer-events-none disabled:opacity-50",
        {
          "bg-cardinal hover:bg-crimson text-white hover:text-white":
            variant === "primary",
          "text-cardinal hover:text-dark bg-white": variant === "secondary",
        },
        className,
      )}
      {...props}
    >
      {children}
    </Link>
  );
};
