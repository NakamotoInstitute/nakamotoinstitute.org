export type AdditionalNavigationProps = {
  children: React.ReactNode;
};

export async function AdditionalNavigation({
  children,
}: AdditionalNavigationProps) {
  return (
    <nav
      aria-label="additional"
      className="border-b border-dashed border-dark py-3"
    >
      {children}
    </nav>
  );
}
