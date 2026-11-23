#!/usr/bin/env python3
"""Send files to the Slack upload URLs that slack_get_file_upload_url returned.

  put.py FILE URL [FILE URL ...]

Prints one line per file. The size passed to slack_get_file_upload_url must be `size FILE` below.
  put.py --size FILE...      print the exact byte size of each file, for content_length
"""

import mimetypes
import os
import subprocess
import sys

TYPES = {".webm": "video/webm", ".mov": "video/quicktime", ".mp4": "video/mp4", ".webp": "image/webp"}


def main():
    args = sys.argv[1:]
    if args and args[0] == "--size":
        for name in args[1:]:
            print(f"{os.path.getsize(name)}\t{os.path.basename(name)}")
        return 0
    if not args or len(args) % 2:
        sys.exit(__doc__)
    failed = 0
    for name, url in zip(args[0::2], args[1::2]):
        ext = os.path.splitext(name)[1].lower()
        ctype = TYPES.get(ext) or mimetypes.guess_type(name)[0] or "application/octet-stream"
        # The URL is passed as one argument, untouched: its signed token is case-sensitive.
        proc = subprocess.run(
            ["curl", "-sS", "--max-time", "900", "-X", "POST", url, "-H", f"Content-Type: {ctype}",
             "--data-binary", f"@{name}"],
            capture_output=True, text=True)
        answer = (proc.stdout or proc.stderr).strip()[:200]
        ok = proc.returncode == 0 and answer.startswith("OK")
        failed += not ok
        print(f"{'sent  ' if ok else 'FAILED'} {os.path.basename(name)} ({ctype}): {answer}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
