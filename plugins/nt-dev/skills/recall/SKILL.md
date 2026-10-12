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

Transcripts are JSONL under `~/.claude/projects/`. Match the directory on the trailing
repo name and confirm the recorded `cwd`. The prior session is usually the second newest.
List with `/bin/ls` and order by JSONL timestamps, not file times.

If the session is ambiguous, show each candidate's start, ID, and first prompt. Search
this repo by topic before trying other repos.

## Extract

Use `jq`. Drop every record type the table does not list; `attachment`, `system`, and the
mode, cost, and history records are harness noise.

| Signal       | Filter                                                                                                                            |
| ------------ | --------------------------------------------------------------------------------------------------------------------------------- |
| User prompts | `type=="user"`, `isMeta!=true`, string content or `text` blocks; skip `tool_result`                                               |
| Model text   | `type=="assistant"`, `text` blocks; `thinking` only for depth                                                                     |
| Tool index   | `type=="assistant"`, `tool_use` blocks as `name` + truncated `input`; grep bodies (`tool_result`, `toolUseResult`) only on a miss |
| Subagents    | `<sessionId>/subagents/agent-*.jsonl` beside the transcript, same shape, first `user` record is the delegation prompt             |

```sh
jq -r 'select(.type=="user" and .isMeta!=true) | .message.content
  | if type=="string" then . else (map(select(.type=="text").text)|join("\n")) end
  | select(length>0)' "$f"
jq -r 'select(.type=="assistant") | .message.content[] | select(.type=="text").text' "$f"
jq -r 'select(.type=="assistant") | .message.content[] | select(.type=="tool_use")
  | "\(.name)\t\(.input|tostring|.[:120])"' "$f"
```

Open `tool-results/` only when the transcript points at persisted output or an expected
keyword is missing.

## Resume

Summarize the decisions, the work done, and the open thread, then continue the task. Never
copy long transcripts into the repo; they can hold secrets.
