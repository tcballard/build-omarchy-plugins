import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { fileURLToPath } from 'node:url';

export const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
export const hash = data => crypto.createHash('sha256').update(data).digest('hex');
export const readJSON = p => JSON.parse(fs.readFileSync(p, 'utf8'));
export const writeJSON = (p, v) => fs.writeFileSync(p, JSON.stringify(v, null, 2) + '\n');
export function files(dir, base = dir) {
  return fs.readdirSync(dir, { withFileTypes: true }).sort((a,b)=>a.name.localeCompare(b.name)).flatMap(e => {
    if (['.git', 'target', 'dist', 'node_modules'].includes(e.name)) return [];
    const p = path.join(dir, e.name);
    if (e.isSymbolicLink() || (!e.isFile() && !e.isDirectory())) throw Error(`Unsupported file: ${p}`);
    return e.isDirectory() ? files(p, base) : [path.relative(base, p)];
  });
}
export function validate(c) {
  if (!/^[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,37}[a-zA-Z0-9])?$/.test(c.owner)) throw Error('Invalid GitHub owner');
  if (!/^[a-zA-Z0-9][a-zA-Z0-9._-]{0,99}$/.test(c.repo) || c.repo.endsWith('.git') || c.repo.includes('..')) throw Error('Invalid repository name');
  if (!/^[a-z][a-z0-9-]{0,59}$/.test(c.slug)) throw Error('Use a lowercase slug starting with a letter');
  if (!/^[a-z][a-z0-9]*(?:\.[a-z][a-z0-9_-]*){2,}$/.test(c.id) || c.id.startsWith('omarchy.')) throw Error('Use a lowercase reverse-domain ID outside omarchy.*');
  for (const k of ['name','author','description']) {
    if (typeof c[k] !== 'string' || !c[k].trim() || /[\x00-\x1f\x7f]/.test(c[k]) || c[k].length > 240) throw Error(`Invalid ${k}`);
  }
  if (!/^20\d{2}$/.test(String(c.year))) throw Error('Invalid copyright year');
  if (c.inspiration) {
    const u = new URL(c.inspiration);
    if (u.protocol !== 'https:' || u.username || u.password || /[\s<>"'()]/.test(c.inspiration)) throw Error('Inspiration must be a plain HTTPS URL');
  }
}
const html = s => s.replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('>','&gt;').replaceAll('"','&quot;');
export function render(c, blueprintRoot = path.join(root, '.template', 'blueprint')) {
  validate(c);
  const values = {};
  for (const [key, value] of Object.entries(c)) {
    if (typeof value !== 'string' && typeof value !== 'number') continue;
    values[key.toUpperCase()] = String(value);
    values[key.toUpperCase() + '_HTML'] = html(String(value));
    values[key.toUpperCase() + '_JSON'] = JSON.stringify(String(value));
    values[key.toUpperCase() + '_DESKTOP'] = String(value).replaceAll('\\','\\\\');
  }
  values.REPO_URL = `https://github.com/${c.owner}/${c.repo}`;
  values.CRATE = c.slug.replaceAll('-', '_');
  values.INSPIRATION_NOTE = c.inspiration ? `**Inspired by [the original project](${c.inspiration}).** See [credits](CREDITS.md) for provenance and licence boundaries.` : 'Original starter; no external product inspiration has been declared. Add prominent credit here when adapting an existing project.';
  const replace = text => text.replace(/@@([A-Z_]+)@@/g, (_, k) => {
    if (!(k in values)) throw Error(`Unknown token ${k}`);
    return values[k];
  });
  const output = new Map();
  for (const f of files(blueprintRoot)) {
    const dest = replace(f).replace(/\.tpl$/, '');
    if (path.isAbsolute(dest) || dest.split(path.sep).includes('..')) throw Error('Unsafe output path');
    output.set(dest, {text: replace(fs.readFileSync(path.join(blueprintRoot, f), 'utf8')), mode: fs.statSync(path.join(blueprintRoot,f)).mode & 0o777});
  }
  if (c.kind === 'package') {
    const base = `pkgbuilds/${c.slug}/`;
    const sums = ['payload.sh', 'LICENSE'].map(f => hash(output.get(base+f).text));
    output.get(base+'PKGBUILD').text = output.get(base+'PKGBUILD').text.replaceAll('SOURCE_SHA256',sums[0]).replaceAll('LICENSE_SHA256',sums[1]);
  }
  return output;
}
