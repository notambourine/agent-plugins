# PR and issue bodies

## Wording

Write plainly, with concrete nouns. Use no inflated adjectives, no `not just X but Y`,
and no closing line that restates the body. Never name a client. Describe them by sector
and shape.

## Body file

Write the body file to an absolute session-scratchpad path, never `$TMPDIR`. `gh` runs
unsandboxed, where `$TMPDIR` is shared and `--body-file` can read another session's file.
