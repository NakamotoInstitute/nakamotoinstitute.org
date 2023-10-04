export function Chip({ children }: { children: string }) {
  return (
    <div className="inline-flex select-none items-center rounded-lg bg-mariner px-2 pb-1.5 pt-1 text-center font-mono text-xs font-bold leading-none text-white">
      {children}
    </div>
  );
}
