#!/usr/bin/env node
// Still frames from a video, taken with headless Chrome, so no ffmpeg is needed.
//
//   node frames.mjs VIDEO [--n 4] [--at 0.1,0.5,0.9] [--out DIR] [--width 1280]
//
// Writes <out>/<video name>-f1.png ... and prints one line per frame: path, time, duration.
// --at takes fractions of the length (0-1) or seconds with an "s" suffix (12s).

import { spawn } from 'node:child_process';
import { mkdtempSync, mkdirSync, readFileSync, writeFileSync, rmSync, existsSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { basename, extname, join, resolve } from 'node:path';
import { pathToFileURL } from 'node:url';

const args = process.argv.slice(2);
const flag = (name, fallback) => {
  const index = args.indexOf(`--${name}`);
  return index === -1 ? fallback : args.splice(index, 2)[1];
};
const count = Number(flag('n', 4));
const at = flag('at', '');
const outDir = resolve(flag('out', '.'));
const width = Number(flag('width', 1280));
const video = args[0] && resolve(args[0]);
if (!video || !existsSync(video)) {
  console.error('frames: give a video file');
  process.exit(2);
}

const chromeBin =
  process.env.CHROME_BIN ||
  ['/usr/bin/google-chrome', '/usr/bin/chromium', '/usr/bin/chromium-browser',
    '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
    'C:/Program Files/Google/Chrome/Application/chrome.exe',
    'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe'].find((path) => existsSync(path));
if (!chromeBin) {
  console.error('frames: no Chrome found, set CHROME_BIN');
  process.exit(2);
}

const profile = mkdtempSync(join(tmpdir(), 'eow-frames-'));
const chrome = spawn(
  chromeBin,
  ['--headless=new', '--no-sandbox', '--disable-gpu', '--hide-scrollbars', '--mute-audio',
    '--autoplay-policy=no-user-gesture-required', '--remote-debugging-port=0',
    `--user-data-dir=${profile}`, 'about:blank'],
  { stdio: 'ignore' },
);
const quit = (code) => {
  chrome.kill('SIGKILL');
  try {
    rmSync(profile, { recursive: true, force: true });
  } catch {}
  process.exit(code);
};
const sleep = (ms) => new Promise((done) => setTimeout(done, ms));

try {
  let port;
  for (let tries = 0; tries < 100 && !port; tries += 1) {
    await sleep(100);
    try {
      port = readFileSync(join(profile, 'DevToolsActivePort'), 'utf8').split('\n')[0];
    } catch {}
  }
  if (!port) throw new Error('Chrome did not start');
  const targets = await (await fetch(`http://127.0.0.1:${port}/json/list`)).json();
  const page = targets.find((target) => target.type === 'page');
  if (!page) throw new Error('no CDP page target');

  const socket = new WebSocket(page.webSocketDebuggerUrl);
  await new Promise((done, fail) => {
    socket.onopen = done;
    socket.onerror = () => fail(new Error('CDP socket failed'));
  });
  let nextId = 0;
  const waiting = new Map();
  socket.onmessage = (event) => {
    const message = JSON.parse(event.data);
    const entry = waiting.get(message.id);
    if (!entry) return;
    waiting.delete(message.id);
    if (message.error) entry.fail(new Error(message.error.message));
    else entry.done(message.result);
  };
  const send = (method, params = {}) =>
    new Promise((done, fail) => {
      nextId += 1;
      waiting.set(nextId, { done, fail });
      socket.send(JSON.stringify({ id: nextId, method, params }));
    });
  const evaluate = async (expression) => {
    const result = await send('Runtime.evaluate', { expression, awaitPromise: true, returnByValue: true });
    if (result.exceptionDetails) {
      throw new Error(result.exceptionDetails.exception?.description || result.exceptionDetails.text);
    }
    return result.result.value;
  };

  await send('Page.enable');
  // Chrome opens a bare video file in its own media document, which gives us the <video>.
  await send('Page.navigate', { url: pathToFileURL(video).href });
  const info = await evaluate(`new Promise((done, fail) => {
    const started = Date.now();
    const poll = () => {
      const v = document.querySelector('video');
      if (v && v.error) return fail(new Error('Chrome cannot decode this video'));
      if (v && v.readyState >= 1 && v.videoWidth) {
        v.pause(); v.controls = false; v.muted = true;
        const fix = () => done({ duration: v.duration, width: v.videoWidth, height: v.videoHeight });
        // A screen recording straight from a recorder can report no length until it is seeked.
        if (!Number.isFinite(v.duration)) {
          v.addEventListener('durationchange', () => Number.isFinite(v.duration) && fix());
          v.currentTime = 1e7;
          return;
        }
        return fix();
      }
      if (Date.now() - started > 20000) return fail(new Error('the video never loaded'));
      setTimeout(poll, 100);
    };
    poll();
  })`);

  const shotWidth = Math.min(width, info.width);
  const shotHeight = Math.round((shotWidth * info.height) / info.width);
  await send('Emulation.setDeviceMetricsOverride', {
    width: shotWidth, height: shotHeight, deviceScaleFactor: 1, mobile: false,
  });
  await evaluate(`(() => {
    document.documentElement.style.cssText = 'margin:0;background:#000;overflow:hidden';
    document.body.style.cssText = 'margin:0;background:#000;overflow:hidden';
    const v = document.querySelector('video');
    v.style.cssText = 'position:fixed;inset:0;width:100vw;height:100vh;object-fit:contain;margin:0';
  })()`);

  const last = Math.max(0, info.duration - 0.15);
  const times = at
    ? at.split(',').map((spot) => (spot.endsWith('s') ? Number(spot.slice(0, -1)) : Number(spot) * info.duration))
    : Array.from({ length: count }, (_, index) => (info.duration * (index + 0.5)) / count);

  mkdirSync(outDir, { recursive: true });
  const stem = basename(video, extname(video));
  console.log(`# ${basename(video)} ${info.width}x${info.height} ${info.duration.toFixed(1)}s`);
  for (const [index, wanted] of times.entries()) {
    const time = Math.min(Math.max(0, wanted), last);
    await evaluate(`new Promise((done) => {
      const v = document.querySelector('video');
      const settle = () => requestAnimationFrame(() => requestAnimationFrame(() => done(true)));
      if (Math.abs(v.currentTime - ${time}) < 0.01 && v.readyState >= 2) return settle();
      v.addEventListener('seeked', settle, { once: true });
      v.currentTime = ${time};
      setTimeout(() => done(false), 8000);
    })`);
    const shot = await send('Page.captureScreenshot', { format: 'png' });
    const file = join(outDir, `${stem}-f${index + 1}.png`);
    writeFileSync(file, Buffer.from(shot.data, 'base64'));
    console.log(`${file}\t${time.toFixed(1)}s of ${info.duration.toFixed(1)}s`);
  }
  quit(0);
} catch (error) {
  console.error(`frames: ${error.message}`);
  quit(1);
}
