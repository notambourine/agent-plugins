# Transcript records

Each line is one record keyed by `type` and linked by `uuid` and `parentUuid`.

| Record                                     | Meaning                                                                                 |
| ------------------------------------------ | --------------------------------------------------------------------------------------- |
| `user`, `origin.kind=="human"`             | Typed or queued prompt; string content or `text` and `image` blocks                     |
| `user` with `toolUseResult`                | Tool output as a `tool_result` block keyed by `tool_use_id`                             |
| `user`, `isMeta==true`                     | Skill body, local-command caveat, or pasted-image stub                                  |
| `user`, no `origin`                        | Slash-command stub, interrupt marker, `!` bash I/O, or local command output             |
| `user`, `origin.kind=="task-notification"` | Background task or agent completion                                                     |
| `user`, `origin.kind=="peer"`              | Subagent final report in `origin.body`; read it for what a delegated agent found        |
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
