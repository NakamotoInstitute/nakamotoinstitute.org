type SearchIconProps = {
  className?: string;
};

/** Magnifying-glass icon shared by the navbar palette trigger and the
 *  on-page /search input so the two stay visually identical. */
export function SearchIcon({ className }: SearchIconProps) {
  return (
    <svg
      className={className}
      xmlns="http://www.w3.org/2000/svg"
      fill="none"
      viewBox="0 0 24 24"
      stroke="currentColor"
      strokeWidth={2}
      aria-hidden="true"
    >
      <path
        strokeLinecap="round"
        strokeLinejoin="round"
        d="m21 21-4.35-4.35M11 18a7 7 0 1 0 0-14 7 7 0 0 0 0 14Z"
      />
    </svg>
  );
}
