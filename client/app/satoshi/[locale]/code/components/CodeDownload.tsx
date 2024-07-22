import Link from "next/link";

export type CodeDownloadProps = {
  release: AnchorProps & {
    note?: string;
  };
  md5: {
    hash: string;
    note?: string;
  };
  sha1: {
    hash: string;
    note?: string;
  };
};

export function CodeDownload({ release, md5, sha1 }: CodeDownloadProps) {
  return (
    <div className="mb-4 last:mb-0">
      <p>
        <Link className="text-cardinal hover:underline" href={release.href}>
          {release.text}
        </Link>
        {release.note ? ` ${release.note}` : null}
      </p>
      <ul className="pl-8 max-sm:space-y-2.5">
        <li>
          <span className="text-taupe">MD5:</span>{" "}
          <code className="break-words">{md5.hash}</code>
          {md5.note ? ` ${md5.note}` : null}
        </li>
        <li>
          <span className="text-taupe">SHA1:</span>{" "}
          <code className="break-words">{sha1.hash}</code>
          {sha1.note ? ` ${sha1.note}` : null}
        </li>
      </ul>
    </div>
  );
}
