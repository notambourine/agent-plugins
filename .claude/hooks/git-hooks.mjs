#!/usr/bin/env node
/* Points this repo's git at .githooks/, whose pre-push refuses client configs.

   Git never installs hooks from a clone, so a Claude session is the one place every
   teammate's checkout passes through. Each .githooks/ hook chains to the user's global
   hook of the same name, so taking over core.hooksPath drops nothing.

   Config, via `env` in .claude/settings.local.json or the user's:
     NT_GIT_HOOKS=off   leave core.hooksPath alone
*/
import { spawnSync } from 'node:child_process';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const HOOKS_PATH = '.githooks';
const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '..', '..');

if ((process.env.NT_GIT_HOOKS ?? '').trim().toLowerCase() === 'off') process.exit(0);

const git = (...args) => spawnSync('git', ['-C', ROOT, ...args], { encoding: 'utf8' });

const current = git('config', '--local', '--get', 'core.hooksPath');
if (current.stdout.trim() === HOOKS_PATH) process.exit(0);

if (git('config', '--local', 'core.hooksPath', HOOKS_PATH).status === 0) {
  console.log(JSON.stringify({
    systemMessage: `[git-hooks] set core.hooksPath to ${HOOKS_PATH}; global hooks still run through it`,
  }));
}
process.exit(0);
