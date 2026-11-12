---
name: share
description: Turn a report, notes, deck, screenshot, or folder into a branded deck or document PDF in the client's Google Drive folder and return its Drive link. Use when the user asks to share, send, or get a link for a file or directory.
---

# Share

Put the file in Drive and return its link. Never host it anywhere else.

1. Run `intake` when the file is for a client. With no client, use
   `My Drive/notambourine/`. If the draft holds proposals the user has not confirmed, per
   [../../outputs.md](../../outputs.md#writing), stop here until the user confirms or cuts
   them.
2. Shape the source:
   - Slides, or content the user calls a deck: a `deck` per
     [../../outputs.md](../../outputs.md#decks).
   - Prose, notes, or a report: a `pdf` per
     [../../outputs.md](../../outputs.md#documents).
   - A finished PDF, image, video, or folder: copy it unchanged.
3. Name it and write it per [../../outputs.md](../../outputs.md#files). Rename a finished
   PDF that is named for its tool or as `deck.pdf`. If there is no Drive mount, stop and
   say so, because a local path cannot be shared.
4. Find the synced file with the Google Drive connector and return its link. Without the
   connector, return the Drive path and say that a link needs the connector.

Never change sharing permissions. The file inherits its folder's access, so when the
folder is not the client's shared drive, say who can open it.

A file that leaves the client's own folder describes the client by sector and never by
name.
