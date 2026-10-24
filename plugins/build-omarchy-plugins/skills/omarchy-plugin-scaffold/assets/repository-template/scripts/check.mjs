#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import assert from 'node:assert/strict';
import { root, files, hash, readJSON, validate } from './template.mjs';

export function check(base=root) {
  const c=readJSON(path.join(base,'.template/project.json'));
  validate(c);
  const tree=files(base);
  for(const f of tree) {
    if(f.startsWith('.template/blueprint/') || f.startsWith('scripts/') || f.startsWith('tests/')) continue;
    assert(!/@@[A-Z_]+@@/.test(fs.readFileSync(path.join(base,f),'utf8')),`Unresolved token in ${f}`);
  }
  const read=f=>fs.readFileSync(path.join(base,f),'utf8');
  for(const f of ['README.md','LICENSE','CREDITS.md','AGENTS.md','docs/ACCEPTANCE.json','.github/workflows/ci.yml','.github/workflows/release.yml']) assert(tree.includes(f),`Missing ${f}`);
  const readme=read('README.md');
  assert(readme.includes('<h1 align="center">'),'Centered title required');
  assert(!readme.includes('](preview.png)'), 'Do not embed an absent preview');
  for(const m of readme.matchAll(/\]\(([^)]+)\)/g)) {
    const link=m[1].split('#')[0];
    if(link && !/^[a-z]+:/.test(link)) assert(fs.existsSync(path.join(base,link)),`Broken README link ${link}`);
  }
  for(const f of tree.filter(f=>f.startsWith('.github/workflows/'))) {
    for(const m of read(f).matchAll(/uses:\s+([^\s#]+)/g)) assert(/@[a-f0-9]{40}$/.test(m[1]),`Unpinned action in ${f}`);
    assert(read(f).includes('permissions:'),`Missing explicit permissions ${f}`);
    assert(!read(f).includes('pull_request_target'), 'Untrusted PR execution must not get a privileged workflow');
  }
  if(c.kind==='plugin') {
    const m=readJSON(path.join(base,'manifest.json'));
    assert.equal(m.schemaVersion,1);assert.equal(m.id,c.id);
    const kinds={'bar-widget':'barWidget',bar:'bar',panel:'panel',overlay:'overlay',menu:'menu',service:'service'};
    assert(Array.isArray(m.kinds)&&m.kinds.length>0&&new Set(m.kinds).size===m.kinds.length);
    for(const k of m.kinds) assert(kinds[k] && m.entryPoints[kinds[k]],`Missing entry point for ${k}`);
    for(const [k,f] of Object.entries(m.entryPoints)) {
      assert(Object.values(kinds).includes(k));
      assert(typeof f==='string' && /^[A-Za-z0-9_./-]+\.qml$/.test(f) && !f.startsWith('/') && !f.split('/').includes('..'));
      assert(tree.includes(f),`Missing QML ${f}`);
    }
    assert.equal(readJSON(path.join(base,'.omarchy-workbench.json')).schemaVersion,1);
  } else if(c.kind==='theme') {
    const palette={};
    for(const line of read('colors.toml').split('\n')) {
      if(!line.trim()||line.trim().startsWith('#'))continue;
      const m=/^([a-z_]+)\s*=\s*"([^"\n]+)"\s*$/.exec(line);assert(m,`Invalid flat palette line: ${line}`);
      assert(!(m[1] in palette),`Duplicate colour ${m[1]}`);palette[m[1]]=m[2];
      assert(m[1]==='mode'?['dark','light'].includes(m[2]):/^#[a-fA-F0-9]{6}$/.test(m[2]));
    }
    for(const k of ['mode','accent','background','foreground','red','yellow','green','cyan','blue','magenta'])assert(palette[k],`Missing ${k}`);
    const lum=hex=>hex.slice(1).match(/../g).map(v=>parseInt(v,16)/255).map(v=>v<=0.04045?v/12.92:((v+.055)/1.055)**2.4).reduce((a,v,i)=>a+v*[.2126,.7152,.0722][i],0);
    const [a,b]=[lum(palette.foreground),lum(palette.background)].sort((a,b)=>a-b);
    assert((b+.05)/(a+.05)>=4.5,'Foreground/background contrast below 4.5:1');
  } else if(c.kind==='app') {
    assert(read('Cargo.toml').includes(`name = "${c.slug}"`));
    assert(read('src/main.rs').includes(JSON.stringify(c.id)));
    const desktop=read(`packaging/${c.id}.desktop`);
    assert(desktop.includes(`Exec=${c.slug}\n`) && desktop.includes(`Icon=${c.id}\n`));
    assert(tree.includes(`packaging/${c.id}.svg`));
  } else if(c.kind==='package') {
    const p=`pkgbuilds/${c.slug}/`;
    const recipe=read(p+'PKGBUILD');
    for(const f of ['payload.sh','LICENSE'])assert(recipe.includes(hash(read(p+f))),`Checksum mismatch: ${f}`);
    assert(!recipe.includes('SKIP'));assert.equal(readJSON(path.join(base,p+'.omarchy/package.json')).source,'local');
  } else throw Error(`Unknown kind ${c.kind}`);
  return c;
}
if(process.argv[1]===new URL(import.meta.url).pathname) {
  try {const c=check();console.log(`PASS: ${c.kind} structure, identity, links and CI policy (${c.initialized?'initialized project':'template starter'}). Native and live checks are separate.`);}
  catch(e){console.error(e.message);process.exitCode=1;}
}
