type CloseIconProps = {
  className?: string;
};

/** "X" close/clear icon shared by the navbar palette's clear button and the
 *  on-page /search clear control, so the two stay visually identical. */
export function CloseIcon({ className }: CloseIconProps) {
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
        d="M6 18 18 6M6 6l12 12"
      />
    </svg>
  );
}
