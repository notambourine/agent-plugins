# PR and issue bodies

## Wording

Write plainly: concrete nouns, no inflated adjectives, no `not just X but Y`, no closing
flourish. Never name a client; describe them by sector and shape.

## Body file

Write the body file to an absolute session-scratchpad path, never `$TMPDIR`. `gh` runs
unsandboxed, where `$TMPDIR` is shared and `--body-file` can read another session's file.
