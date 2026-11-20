/* Decision table for the artifact-brand PreToolUse hook. Run: npm test

   Session ids carry the pid, so a second run never inherits the first one's markers. */
import { match, ok, strictEqual } from 'node:assert/strict';
import { spawnSync } from 'node:child_process';
import { readdirSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { dirname, join } from 'node:path';
import { after, describe, it } from 'node:test';
import { fileURLToPath } from 'node:url';

const HOOK = join(dirname(fileURLToPath(import.meta.url)), 'artifact-brand.mjs');

let sessions = 0;
const sessionId = () => `test-${process.pid}-${(sessions += 1)}`;

after(() => {
  for (const name of readdirSync(tmpdir())) {
    if (name.startsWith('nt-brand-artifact-') && name.includes(String(process.pid))) {
      rmSync(join(tmpdir(), name), { force: true });
    }
  }
});

function run(tool_name, tool_input, { env = {}, session = sessionId() } = {}) {
  const result = spawnSync(process.execPath, [HOOK], {
    input: JSON.stringify({ session_id: session, tool_name, tool_input }),
    encoding: 'utf8',
    env: { ...process.env, NT_BRAND_ARTIFACT_NUDGE: '', ...env },
  });
  strictEqual(result.status, 0, `hook exited ${result.status}: ${result.stderr}`);
  const out = result.stdout.trim();
  return out ? JSON.parse(out) : null;
}

const denial = (r) => r?.hookSpecificOutput?.permissionDecision === 'deny'
  && r.hookSpecificOutput.permissionDecisionReason;

describe('what it nudges', () => {
  it('a publish with no action, at the brand skill and the design system', () => {
    const reason = denial(run('Artifact', { file_path: 'page.html' }));
    match(reason, /\/nt-brand:system/);
    match(reason, /claude\.ai\/artifact\//);
  });

  it('an explicit publish and a quickstart', () => {
    ok(denial(run('Artifact', { action: 'publish', file_path: 'page.html' })));
    ok(denial(run('Artifact', { action: 'quickstart', intent: 'slides' })));
  });
});

describe('what it leaves alone', () => {
  for (const action of ['read', 'list', 'open', 'pin', 'delete']) {
    it(action, () => strictEqual(run('Artifact', { action, url: 'x' }), null));
  }

  it('an asset upload', () => {
    strictEqual(run('Artifact', { url: 'x', file_path: 'a.png', asset: true }), null);
  });

  it('other skills', () => strictEqual(run('Skill', { skill: 'nt-dev:pr' }), null));

  it('a payload that is not JSON', () => {
    const result = spawnSync(process.execPath, [HOOK], { input: 'nope', encoding: 'utf8' });
    strictEqual(result.status, 0);
    strictEqual(result.stdout.trim(), '');
  });

  it('everything, when NT_BRAND_ARTIFACT_NUDGE=off', () => {
    strictEqual(run('Artifact', { file_path: 'p.html' }, { env: { NT_BRAND_ARTIFACT_NUDGE: 'off' } }), null);
  });
});

describe('session memory', () => {
  it('stops after the skill is read, typed or invoked', () => {
    for (const skill of ['nt-brand:system', '/nt-brand:system']) {
      const session = sessionId();
      strictEqual(run('Skill', { skill }, { session }), null);
      strictEqual(run('Artifact', { file_path: 'p.html' }, { session }), null);
    }
  });

  it('nudges once per session, then steps aside', () => {
    const session = sessionId();
    ok(denial(run('Artifact', { file_path: 'p.html' }, { session })));
    strictEqual(run('Artifact', { file_path: 'p.html' }, { session }), null);
  });
});
