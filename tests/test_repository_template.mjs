import { test } from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { spawnSync } from 'node:child_process';

const repo = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const skill = path.join(repo, 'skills/omarchy-plugin-scaffold');
const generator = path.join(skill, 'scripts/new_repository.mjs');
const identity = ['--owner', 'tester', '--repo', 'omarchy-example', '--slug', 'example', '--name', 'Example & "Friends"', '--author', 'Test Author', '--id', 'io.github.tester.example', '--year', '2026'];
const read = p => JSON.parse(fs.readFileSync(p, 'utf8'));
const run = (args, cwd) => spawnSync(process.execPath, args, { cwd, encoding: 'utf8', env: { ...process.env, HTTP_PROXY: 'http://127.0.0.1:1', HTTPS_PROXY: 'http://127.0.0.1:1' } });
function temporary(t) {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'repository template '));
  t.after(() => fs.rmSync(dir, { recursive: true, force: true }));
  return dir;
}
function generate(t) {
  const parent = temporary(t);
  const output = path.join(parent, 'new plugin');
  const result = run([generator, '--output', output, ...identity], parent);
  assert.equal(result.status, 0, result.stderr);
  assert.match(result.stdout, /PASS: plugin/);
  return output;
}

test('complete pinned snapshot verifies without a network request', () => {
  const result = run([generator, '--check'], os.tmpdir());
  assert.equal(result.status, 0, result.stderr);
  assert.match(result.stdout, /Verified 41 template files at f99681e69937d21c2d4414ac9f65a0fd01fea714/);
});

test('generates initialized project, identity, provenance and executable tests in a path with spaces', t => {
  const output = generate(t);
  const manifest = read(path.join(output, 'manifest.json'));
  assert.equal(manifest.id, 'io.github.tester.example');
  assert.equal(manifest.name, 'Example & "Friends"');
  assert.deepEqual(manifest.entryPoints, { barWidget: 'StarterWidget.qml' });
  assert(fs.readFileSync(path.join(output, 'StarterWidget.qml'), 'utf8').includes('io.github.tester.example'));
  assert.equal(read(path.join(output, '.template/project.json')).initialized, true);
  assert.equal(read(path.join(output, '.template/source.json')).commit, 'f99681e69937d21c2d4414ac9f65a0fd01fea714');
  assert(!fs.existsSync(path.join(output, '.git')));
  assert.equal(read(path.join(output, 'docs/ACCEPTANCE.json')).status, 'not-run');
  if (process.platform !== 'win32') assert(fs.statSync(path.join(output, 'tests/run')).mode & 0o111);
  const tests = run(['--test', 'tests/template.test.mjs'], output);
  assert.equal(tests.status, 0, tests.stdout + tests.stderr);
  const preview = run(['scripts/github.mjs'], output);
  assert.equal(preview.status, 0, preview.stderr);
  const policy = JSON.parse(preview.stdout);
  assert.equal(policy.repository, 'tester/omarchy-example');
  assert.deepEqual(policy.ruleset.rules.find(r => r.type === 'required_status_checks').parameters.required_status_checks, [{ context: 'verify' }]);
  assert.match(policy.note, /Dry run/);
  fs.unlinkSync(path.join(output, 'manifest.json'));
  assert.notEqual(run(['scripts/check.mjs'], output).status, 0, 'check CLI must execute even when its path contains spaces');
});

test('existing empty directory, edited project, file and dangling symlink are preserved', t => {
  const parent = temporary(t);
  const output = path.join(parent, 'existing');
  fs.mkdirSync(output);
  const invoke = () => run([generator, '--output', output, ...identity], parent);
  assert.notEqual(invoke().status, 0);
  assert.deepEqual(fs.readdirSync(output), []);
  fs.writeFileSync(path.join(output, 'mine'), 'user edit');
  assert.notEqual(invoke().status, 0);
  assert.equal(fs.readFileSync(path.join(output, 'mine'), 'utf8'), 'user edit');
  fs.rmSync(output, { recursive: true });
  fs.writeFileSync(output, 'user file');
  assert.notEqual(invoke().status, 0);
  assert.equal(fs.readFileSync(output, 'utf8'), 'user file');
  fs.unlinkSync(output);
  try { fs.symlinkSync(path.join(parent, 'missing'), output, 'junction'); }
  catch (e) { if (process.platform === 'win32' && e.code === 'EPERM') return; throw e; }
  assert.notEqual(invoke().status, 0);
  assert(fs.lstatSync(output).isSymbolicLink());
});

test('invalid identity leaves destination absent', t => {
  const parent = temporary(t);
  const output = path.join(parent, 'invalid');
  const invalid = identity.slice();
  invalid[invalid.indexOf('--id') + 1] = 'omarchy.reserved.plugin';
  const result = run([generator, '--output', output, ...invalid], parent);
  assert.notEqual(result.status, 0);
  assert.match(result.stderr, /reverse-domain/);
  assert(!fs.existsSync(output));
});

test('relocated skill works alone; corrupt or extra assets fail before generating', t => {
  const parent = temporary(t);
  const installed = path.join(parent, 'renamed-skill');
  fs.cpSync(skill, installed, { recursive: true });
  const command = path.join(installed, 'scripts/new_repository.mjs');
  const output = path.join(parent, 'independent');
  assert.equal(run([command, '--output', output, ...identity], parent).status, 0);
  const starter = path.join(installed, 'assets/repository-template/README.md');
  const original = fs.readFileSync(starter);
  fs.appendFileSync(starter, 'tampered');
  const rejected = path.join(parent, 'rejected');
  const attempt = () => run([command, '--output', rejected, ...identity], parent);
  assert.match(attempt().stderr, /checksum mismatch/);
  assert(!fs.existsSync(rejected));
  fs.writeFileSync(starter, original);
  fs.writeFileSync(path.join(installed, 'assets/repository-template/untracked'), 'unexpected');
  assert.match(attempt().stderr, /inventory differs/);
  assert(!fs.existsSync(rejected));
});
