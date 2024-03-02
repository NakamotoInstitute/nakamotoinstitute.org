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
    <div>
      <p>
        <Link className="font-bold" href={release.href}>
          {release.text}
        </Link>
        {release.note ? ` ${release.note}` : null}
      </p>
      <ul className="pl-10">
        <li>
          {"MD5: "}
          <code className="break-words text-sm text-pink-500">{md5.hash}</code>
          {md5.note ? ` ${md5.note}` : null}
        </li>
        <li>
          {"SHA1: "}
          <code className="break-words text-sm text-pink-500">{sha1.hash}</code>
          {sha1.note ? ` ${sha1.note}` : null}
        </li>
      </ul>
    </div>
  );
}
