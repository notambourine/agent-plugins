---
name: recall
description: Recover context from prior sessions in this repo. Use when the user points at earlier work, asks what happened last time, or resumes an unfinished task.
allowed-tools:
  - Bash
  - Read
---

# Recall

Recover what the last session decided and left unfinished, then pick the work back up.

## Find the session

Transcripts are `~/.claude/projects/<cwd with / as ->/<sessionId>.jsonl`. Directory names
start with `-`, so pass absolute paths to `ls` and `grep`. Confirm the recorded `cwd`. The
prior session is usually the second newest; order by JSONL timestamps, not file times.

If the session is ambiguous, show each candidate's start, ID, and first prompt. Search
this repo by topic before trying other repos.

## Read the conversation

Default to the dialogue: the user's typed prompts and the model's prose, in order. Skip
tool calls, tool results, file reads, and thinking unless the user asks for them or the
dialogue misses an expected keyword.

```sh
jq -r '
  if .type=="user" and (.origin.kind=="human" or .isCompactSummary==true) then
    .message.content
    | if type=="string" then . else (map(select(.type=="text").text) | join("\n")) end
    | "## USER\n\(.)\n"
  elif .type=="assistant" then
    .message.content[] | select(.type=="text") | "## CLAUDE\n\(.text)\n"
  elif .type=="system" and .subtype=="away_summary" then
    "## RECAP\n\(.content)\n"
  else empty end' "$f"
```

## Go deeper on request

For tool calls, thinking, subagent reports, or a specific tool result, read
[references/records.md](references/records.md) for the record types and the queries.

## Resume

Summarize the decisions, the work done, and the open thread, then continue the task. Never
copy long transcripts into the repo; they can hold secrets.
