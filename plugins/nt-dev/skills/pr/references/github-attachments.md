# GitHub attachments

Capture a stable viewport showing only the relevant state. Keep secrets, client names, and
unrelated chrome out of frame.

```bash
FILE=shot.png
REPO=$(gh repo view --json nameWithOwner --jq .nameWithOwner)
URL=$(curl -s -X POST \
  "https://uploads.github.com/user-attachments/assets?name=$(basename "$FILE")&content_type=image/png&repository_id=$(gh api "repos/$REPO" --jq .id)" \
  -H "Authorization: Bearer $(gh auth token)" \
  -H "Accept: application/json" \
  --data-binary "@$FILE" | jq -r .url)
```

Embed it as `![label]($URL)`.

The endpoint is undocumented. On a `404` or `422`, fall back to a prerelease:

```bash
gh release create pr-<n>-shots --prerelease "$FILE"
```

Embed the asset URL. Delete the prerelease after merge.
