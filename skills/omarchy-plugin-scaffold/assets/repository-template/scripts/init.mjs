#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import { root, hash, readJSON, writeJSON, render } from './template.mjs';

try {
  const input = process.argv.slice(2);
  if (input.includes('--help')) {
    console.log('node scripts/init.mjs --owner OWNER --repo REPO --slug SLUG --name "Project name" --author "Author" [--id io.github.owner.slug] [--description "Purpose"] [--inspiration https://...] [--year 2026]');
    process.exit(0);
  }
  const allowed = new Set(['owner','repo','slug','name','author','id','description','inspiration','year']);
  const args = {};
  for (let i=0; i<input.length; i+=2) {
    const key = input[i].replace(/^--/,'');
    if (!input[i].startsWith('--') || !allowed.has(key) || key in args || input[i+1] === undefined) throw Error(`Invalid option: ${input[i]}`);
    args[key] = input[i+1];
  }
  for (const key of ['owner','repo','slug','name','author']) if (!args[key]) throw Error(`Missing --${key}`);
  const configPath = path.join(root, '.template/project.json');
  const previous = readJSON(configPath);
  const config = {...previous, ...args, id: args.id || `io.github.${args.owner.toLowerCase()}.${args.slug.replaceAll('-','_')}`, year: args.year || String(new Date().getUTCFullYear()), initialized:true};
  const output = render(config);
  if (previous.initialized) {
    if (JSON.stringify(previous) === JSON.stringify(config)) { console.log('Already initialized; files left unchanged.'); process.exit(0); }
    throw Error('Already initialized. Project identity changes require a reviewed migration; no files changed.');
  }
  const receipt = readJSON(path.join(root,'.template/receipt.json'));
  for (const [f, digest] of Object.entries(receipt)) {
    const p = path.join(root,f);
    let cursor = root;
    for (const part of f.split('/')) {
      cursor = path.join(cursor, part);
      if (fs.lstatSync(cursor).isSymbolicLink()) throw Error(`Symlink refused: ${f}`);
    }
    if (hash(fs.readFileSync(p)) !== digest) throw Error(`Edited starter file: ${f}. Initialize a fresh copy, then transfer your edits.`);
  }
  for (const f of output.keys()) {
    let cursor = root;
    for (const part of f.split('/').slice(0,-1)) {
      cursor = path.join(cursor,part);
      if (fs.existsSync(cursor) && (!fs.lstatSync(cursor).isDirectory() || fs.lstatSync(cursor).isSymbolicLink())) throw Error(`Unsafe destination: ${f}`);
    }
    if (!(f in receipt) && fs.existsSync(path.join(root,f))) throw Error(`Would overwrite ${f}`);
  }
  // All inputs and destinations are checked before any project file is changed.
  for (const [f, data] of output) {
    const p = path.join(root,f);
    fs.mkdirSync(path.dirname(p),{recursive:true});
    fs.writeFileSync(p,data.text,{mode:data.mode});
    fs.chmodSync(p,data.mode);
  }
  for (const f of Object.keys(receipt)) if (!output.has(f)) fs.unlinkSync(path.join(root,f));
  writeJSON(configPath,config);
  writeJSON(path.join(root,'.template/receipt.json'),Object.fromEntries([...output].map(([f,d])=>[f,hash(d.text)])));
  console.log(`Initialized ${config.owner}/${config.repo} (${config.id}). Run node scripts/check.mjs, review the diff and commit.`);
} catch (error) { console.error(error.message); process.exitCode = 1; }
