#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import os from 'node:os';
import crypto from 'node:crypto';
import { fileURLToPath } from 'node:url';
import { spawnSync } from 'node:child_process';

const skill = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const source = path.join(skill, 'assets/repository-template');
const lockPath = path.join(skill, 'assets/repository-template.lock.json');
const options = new Set(['output', 'owner', 'repo', 'slug', 'name', 'author', 'id', 'description', 'inspiration', 'year']);
const usage = `node "<skill-dir>/scripts/new_repository.mjs" --output /absolute/unused/path
  --owner OWNER --repo REPO --slug SLUG --name "Plugin Name" --author "Author"
  [--id io.github.owner.slug] [--description "Purpose"] [--inspiration https://...]
  [--year 2026]
Node.js 22+. Offline bar-widget repository starter; no GitHub calls or Git commits.
--check verifies the bundled snapshot without generating anything.`;

function inventory(directory, prefix = '') {
  const result = [];
  if (fs.lstatSync(directory).isSymbolicLink()) throw Error('Template directory must not be a symlink');
  for (const entry of fs.readdirSync(directory, { withFileTypes: true })) {
    const relative = prefix + entry.name;
    if (entry.isDirectory()) result.push(...inventory(path.join(directory, entry.name), relative + '/'));
    else if (entry.isFile()) result.push(relative);
    else throw Error(`Unsupported template entry: ${relative}`);
  }
  return result.sort();
}

function snapshot() {
  const lock = JSON.parse(fs.readFileSync(lockPath, 'utf8'));
  if (lock.schemaVersion !== 1 || !/^[a-f0-9]{40}$/.test(lock.commit) || !Array.isArray(lock.files)) throw Error('Invalid template lock');
  const names = lock.files.map(f => f.path);
  if (new Set(names).size !== names.length || JSON.stringify(names.slice().sort()) !== JSON.stringify(inventory(source))) throw Error('Template file inventory differs from lock');
  const files = lock.files.map(f => {
    if (typeof f.path !== 'string' || f.path.split('/').some(p => !p || p === '.' || p === '..') || /[\\:]/.test(f.path) || !['100644', '100755'].includes(f.mode)) throw Error('Unsafe template lock entry');
    const data = fs.readFileSync(path.join(source, f.path));
    if (crypto.createHash('sha256').update(data).digest('hex') !== f.sha256) throw Error(`Template checksum mismatch: ${f.path}`);
    return { ...f, data };
  });
  return { lock, files };
}

function copy(files, destination) {
  for (const f of files) {
    const target = path.join(destination, f.path);
    fs.mkdirSync(path.dirname(target), { recursive: true });
    fs.writeFileSync(target, f.data, { flag: 'wx', mode: parseInt(f.mode.slice(-3), 8) });
    fs.chmodSync(target, parseInt(f.mode.slice(-3), 8));
  }
}

// The pinned upstream snapshot is kept byte-for-byte. Apply these documented
// authoring compatibility fixes only to the new checkout (integration version 1).
function portablePaths(directory) {
  function replace(relative, before, after) {
    const file = path.join(directory, relative);
    const text = fs.readFileSync(file, 'utf8');
    if (text.split(before).length !== 2) throw Error(`Compatibility patch no longer matches: ${relative}`);
    fs.writeFileSync(file, text.replace(before, after));
  }
  replace('scripts/template.mjs', '[path.relative(base, p)]', "[path.relative(base, p).split(path.sep).join('/')]");
  for (const relative of ['scripts/check.mjs', 'scripts/github.mjs']) {
    replace(relative, "import path from 'node:path';", "import path from 'node:path';\nimport { fileURLToPath } from 'node:url';");
    replace(relative, 'new URL(import.meta.url).pathname', 'fileURLToPath(import.meta.url)');
  }
}

function run(directory, args) {
  const result = spawnSync(process.execPath, args, { cwd: directory, encoding: 'utf8' });
  if (result.error || result.status !== 0) throw Error(result.error?.message || result.stderr || result.stdout || 'Template command failed');
  return result.stdout.trim();
}

let temporary;
try {
  if (Number(process.versions.node.split('.')[0]) < 22) throw Error('Node.js 22 or later is required');
  const args = process.argv.slice(2);
  if (args.length === 1 && args[0] === '--help') {
    console.log(usage);
  } else {
    const { lock, files } = snapshot();
    if (args.length === 1 && args[0] === '--check') {
      console.log(`Verified ${files.length} template files at ${lock.commit}`);
    } else {
      const values = {};
      for (let i = 0; i < args.length; i += 2) {
        const key = args[i].slice(2);
        if (!args[i].startsWith('--') || !options.has(key) || key in values || args[i + 1] === undefined) throw Error(`Invalid option: ${args[i]}\n${usage}`);
        values[key] = args[i + 1];
      }
      if (!values.output || !path.isAbsolute(values.output)) throw Error('--output must be an absolute, unused path');
      const destination = path.resolve(values.output);
      if (destination === skill || destination.startsWith(skill + path.sep)) throw Error('Destination must be outside the installed skill');
      // lstat also catches dangling links. Refuse empty directories too.
      if (fs.existsSync(destination) || (() => { try { fs.lstatSync(destination); return true; } catch (e) { if (e.code !== 'ENOENT') throw e; return false; } })()) throw Error('Destination already exists; no files changed');
      if (!fs.statSync(path.dirname(destination)).isDirectory()) throw Error('Destination parent must exist');
      temporary = fs.mkdtempSync(path.join(os.tmpdir(), 'omarchy-repository-'));
      copy(files, temporary);
      portablePaths(temporary);
      const identity = Object.entries(values).filter(([key]) => key !== 'output').flatMap(([key, value]) => ['--' + key, value]);
      run(temporary, ['scripts/init.mjs', ...identity]);
      const result = run(temporary, ['scripts/check.mjs']);
      fs.writeFileSync(path.join(temporary, '.template/source.json'), JSON.stringify({
        repository: lock.repository, commit: lock.commit, templateVersion: lock.templateVersion,
        integrationVersion: 1, compatibility: ['posix-relative-paths', 'file-url-entrypoints'],
      }, null, 2) + '\n');
      // Exclusive creation prevents replacement if another process creates it
      // during validation. Never clean up a pre-existing destination on failure.
      fs.mkdirSync(destination);
      const modes = new Map(files.map(f => [f.path, f.mode]));
      const generated = inventory(temporary).map(p => ({ path: p, data: fs.readFileSync(path.join(temporary, p)), mode: modes.get(p) || '100644' }));
      try { copy(generated, destination); }
      catch (error) { throw Error(`Copy failed; inspect the partial new directory ${destination}: ${error.message}`); }
      console.log(`Created ${destination}\n${result}\nReview the files, run ./tests/run, then initialize Git. Live Omarchy testing remains separate.`);
    }
  }
} catch (error) {
  console.error(error.message);
  process.exitCode = 1;
} finally {
  if (temporary) fs.rmSync(temporary, { recursive: true, force: true });
}
