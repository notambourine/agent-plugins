#!/usr/bin/env node
/* Points the first artifact of a session at /nt-brand:system, so every page, deck, and
   design ships in the NoTambourine brand on any teammate's machine, not only where a
   personal CLAUDE.md asks for it.

   Same shape as nt-dev's gh-skill-nudge: a `deny` is the only documented way a PreToolUse
   hook reaches the model, so the first publish is refused with the reason, and
   Skill(nt-brand:system) is the all-clear for the rest of the session.

   Self-contained on purpose: each plugin installs on its own, so nothing here may import
   from nt-dev. skills/system/ is a byte mirror of @notambourine/brand-kit, so the hook
   lives outside it.

   Silence a repo with NT_BRAND_ARTIFACT_NUDGE=off under `env` in .claude/settings.json.
*/
import { existsSync, readFileSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';

if ((process.env.NT_BRAND_ARTIFACT_NUDGE ?? '').trim().toLowerCase() === 'off') pass();

const payload = readPayload();
if (!payload) pass();

const sessionId = typeof payload.session_id === 'string' ? payload.session_id : '';
const input = payload.tool_input ?? {};

/* Skills arrive as `nt-brand:system` from the Skill tool and `/nt-brand:system` when typed. */
if (payload.tool_name === 'Skill') {
  if (/nt-brand:system$/.test(String(input.skill ?? ''))) mark('read');
  pass();
}

/* Only the calls that start or change a page. read, list, open, pin, and asset uploads
   carry no design decisions. An omitted action is a publish. */
const action = input.action ?? 'publish';
if (!['publish', 'quickstart'].includes(action) || input.asset === true) pass();

if (marked('read') || marked('nudged')) pass();
mark('nudged');

deny(`🟡 [artifact-brand] Load /nt-brand:system before you make this artifact, then carry on.

Every NoTambourine artifact uses the brand kit: tokens, type, components, and voice. Publish it as a plain HTML page, not from a Slides or Design type, whose design systems are not the brand kit. For a deck, follow references/decks.md (Marp with deck-standalone.css); for a document, follow references/documents.md (doc-template.html with doc-standalone.css). Both build one self-contained HTML file to publish, and the theme files sit beside the skill's SKILL.md. Invoke the skill and this stops asking for the rest of the session. Silence a repo with NT_BRAND_ARTIFACT_NUDGE=off under \`env\` in .claude/settings.json.`);

/* --- helpers --------------------------------------------------------------- */

/* Every exit is clean: a hook that throws blocks a call it had no opinion about. */
function pass() {
  process.exit(0);
}

function deny(reason) {
  console.log(JSON.stringify({
    hookSpecificOutput: { hookEventName: 'PreToolUse', permissionDecision: 'deny', permissionDecisionReason: reason },
  }));
  process.exit(0);
}

/* fd 0, not /dev/stdin, which Windows lacks. */
function readPayload() {
  try {
    return process.stdin.isTTY ? null : JSON.parse(readFileSync(0, 'utf8'));
  } catch {
    return null;
  }
}

/* A hook is a fresh process every call, so session memory is a temp file keyed by the
   session id. No id means no memory, which errs toward nudging. */
function markerPath(key) {
  return sessionId ? join(tmpdir(), `nt-brand-artifact-${key}-${sessionId.replace(/[^\w-]/g, '')}`) : null;
}

function marked(key) {
  const path = markerPath(key);
  return path ? existsSync(path) : false;
}

function mark(key) {
  const path = markerPath(key);
  if (!path) return;
  try {
    writeFileSync(path, '');
  } catch {
    /* Nowhere to write only means the nudge repeats. */
  }
}
