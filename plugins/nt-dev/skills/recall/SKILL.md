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

## Record types

Each line is one record keyed by `type` and linked by `uuid` and `parentUuid`.

| Record                                     | Meaning                                                                                 |
| ------------------------------------------ | --------------------------------------------------------------------------------------- |
| `user`, `origin.kind=="human"`             | Typed or queued prompt; string content or `text` and `image` blocks                     |
| `user` with `toolUseResult`                | Tool output as a `tool_result` block keyed by `tool_use_id`                             |
| `user`, `isMeta==true`                     | Skill body, local-command caveat, or pasted-image stub                                  |
| `user`, no `origin`                        | Slash-command stub, interrupt marker, `!` bash I/O, or local command output             |
| `user`, `origin.kind=="task-notification"` | Background task or agent completion                                                     |
| `user`, `isCompactSummary==true`           | Summary of the conversation before compaction                                           |
| `assistant`                                | One `text`, `thinking`, or `tool_use` block; records sharing `message.id` are one reply |
| `system`, `subtype=="away_summary"`        | Model-written recap; other `system` subtypes are noise                                  |
| Any other `type`                           | Harness noise: attachments, API requests, modes, cost, file history                     |

Subagents live in `<sessionId>/subagents/agent-*.jsonl` with `isSidechain==true`; the
first `user` record is the delegation prompt. Large tool output persists to
`<sessionId>/tool-results/`.

## Go deeper on request

```sh
# Tool index
jq -r 'select(.type=="assistant") | .message.content[] | select(.type=="tool_use")
  | "\(.name)\t\(.input|tostring|.[:120])"' "$f"
# Thinking
jq -r 'select(.type=="assistant") | .message.content[] | select(.type=="thinking").thinking' "$f"
```

Grep `toolUseResult` bodies or `tool-results/` only to find a specific value.

## Resume

Summarize the decisions, the work done, and the open thread, then continue the task. Never
copy long transcripts into the repo; they can hold secrets.
