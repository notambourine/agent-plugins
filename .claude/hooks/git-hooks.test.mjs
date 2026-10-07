/* git-hooks SessionStart installer, plus the .githooks/ pre-push it installs.

   Run: npm test
*/
import { match, strictEqual } from 'node:assert/strict';
import { spawnSync } from 'node:child_process';
import { chmodSync, cpSync, mkdirSync, mkdtempSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { dirname, join, resolve } from 'node:path';
import { describe, it } from 'node:test';
import { fileURLToPath } from 'node:url';

const HERE = dirname(fileURLToPath(import.meta.url));
const ROOT = resolve(HERE, '..', '..');

/* A scratch repo carrying copies of the hook and .githooks/, with an empty global config. */
function scratch() {
  const dir = mkdtempSync(join(tmpdir(), 'git-hooks-'));
  const home = mkdtempSync(join(tmpdir(), 'git-hooks-home-'));
  const env = { ...process.env, HOME: home, USERPROFILE: home, GIT_CONFIG_NOSYSTEM: '1', NT_GIT_HOOKS: '' };
  const git = (...args) => spawnSync('git', ['-C', dir, ...args], { encoding: 'utf8', env });
  git('init', '-q', '-b', 'main');
  git('config', 'user.email', 't@example.com');
  git('config', 'user.name', 't');
  git('config', 'commit.gpgsign', 'false');
  mkdirSync(join(dir, '.claude/hooks'), { recursive: true });
  cpSync(join(HERE, 'git-hooks.mjs'), join(dir, '.claude/hooks/git-hooks.mjs'));
  cpSync(join(ROOT, '.githooks'), join(dir, '.githooks'), { recursive: true });
  const install = (extra = {}) => spawnSync(process.execPath, [join(dir, '.claude/hooks/git-hooks.mjs')], {
    input: '{}', encoding: 'utf8', env: { ...env, ...extra },
  });
  return { dir, home, env, git, install };
}

describe('installer', () => {
  it('sets core.hooksPath once, then stays quiet', () => {
    const { git, install } = scratch();
    match(install().stdout, /core\.hooksPath/);
    strictEqual(git('config', '--local', '--get', 'core.hooksPath').stdout.trim(), '.githooks');
    strictEqual(install().stdout, '');
  });

  it('NT_GIT_HOOKS=off leaves config alone', () => {
    const { git, install } = scratch();
    install({ NT_GIT_HOOKS: 'off' });
    strictEqual(git('config', '--local', '--get', 'core.hooksPath').status, 1);
  });
});

/* Runs pre-push the way git does: commits not on any remote, ref lines on stdin. */
function prePush(s) {
  const sha = s.git('rev-parse', 'HEAD').stdout.trim();
  return spawnSync('sh', [join(s.dir, '.githooks/pre-push'), 'origin', 'url'], {
    cwd: s.dir, encoding: 'utf8', env: s.env,
    input: `refs/heads/main ${sha} refs/heads/main ${'0'.repeat(40)}\n`,
  });
}

function commit(s, path) {
  mkdirSync(dirname(join(s.dir, path)), { recursive: true });
  writeFileSync(join(s.dir, path), 'x\n');
  s.git('add', path);
  s.git('commit', '-q', '-m', path);
}

describe('pre-push', () => {
  it('passes ordinary commits', () => {
    const s = scratch();
    commit(s, 'README.md');
    strictEqual(prePush(s).status, 0);
  });

  it('refuses a client config anywhere in the pushed commits', () => {
    const s = scratch();
    commit(s, '.claude/refs/nt-pm.md');
    s.git('rm', '-q', '.claude/refs/nt-pm.md');
    s.git('commit', '-q', '-m', 'remove');
    const r = prePush(s);
    strictEqual(r.status, 1);
    match(r.stderr, /nt-pm\.md/);
  });

  it('chains to the global hook with the same stdin', () => {
    const s = scratch();
    const global = join(s.home, 'hooks');
    mkdirSync(global);
    writeFileSync(join(global, 'pre-push'), '#!/bin/sh\ngrep -q refs/heads/main && echo global-ran\n');
    chmodSync(join(global, 'pre-push'), 0o755);
    s.git('config', '--global', 'core.hooksPath', global);
    commit(s, 'README.md');
    const r = prePush(s);
    strictEqual(r.status, 0);
    match(r.stdout, /global-ran/);
  });
});
