---
name: share
description: Turn a report, notes, deck, screenshot, or folder into a branded deck or document PDF in the client's Google Drive folder and return its Drive link. Use when the user asks to share, send, or get a link for a file or directory.
---

# Share

Land the file in Drive and return a link. Never host it anywhere else.

1. Pick the client per [../../client-config.md](../../client-config.md). With no client,
   use `My Drive/notambourine/`.
2. Shape the source:
   - Slides, or content the user calls a deck: a `deck` per
     [../../outputs.md](../../outputs.md#decks).
   - Prose, notes, or a report: a `pdf` per [../../outputs.md](../../outputs.md#documents).
   - A finished PDF, image, video, or folder: copy as is.
3. Write it where [../../outputs.md](../../outputs.md#brand-kit) lands decks. When no Drive
   mount exists, stop and say so; a local path is not a share.
4. Find the synced file with the Google Drive connector and return its link. Without the
   connector, return the Drive path and say the link needs it.

Never change sharing permissions; the file inherits its folder's access. Say who that
folder reaches when it is not the client's shared drive.

Anything leaving the client's own folder describes the client by sector, never by name.
