import {test} from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import {spawnSync} from 'node:child_process';
import {root,readJSON,render,validate} from '../scripts/template.mjs';
import {policy,configure} from '../scripts/github.mjs';

test('identity input rejects paths, reserved IDs and multiline values',()=>{
  const c=readJSON(path.join(root,'.template/project.json'));
  for(const patch of [{slug:'../../x'},{owner:'-flag'},{id:'omarchy.foo.bar'},{name:'x\ny'},{repo:'../other'},{inspiration:'https://user:pass@example.com'}]) assert.throws(()=>validate({...c,...patch}));
});
test('render escapes display strings for JSON and HTML',()=>{
  const c={...readJSON(path.join(root,'.template/project.json')),name:'Tom & "Friends" <test>'};
  const out=render(c);
  assert(out.get('README.md').text.includes('Tom &amp; &quot;Friends&quot; &lt;test&gt;'));
  if(c.kind==='plugin')assert.equal(JSON.parse(out.get('manifest.json').text).name,c.name);
});
test('rules require PRs and matching CI without blocking a solo maintainer',()=>{
  const p=policy('app');
  assert.deepEqual(p.bypass_actors,[]);
  assert.equal(p.rules.find(r=>r.type==='pull_request').parameters.required_approving_review_count,0);
  assert.deepEqual(p.rules.find(r=>r.type==='required_status_checks').parameters.required_status_checks.map(s=>s.context),['verify','native']);
});
test('existing policies are never overwritten',()=>{
  let writes=0;const c={owner:'tester',repo:'demo',kind:'plugin'};
  assert.throws(()=>configure(c,true,false,(args)=>{
    if(args.includes('--method'))writes++;
    if(args.includes('--paginate'))return [[{name:'Omarchy main',source:'tester/demo',source_type:'Repository'}]];
    return {full_name:'tester/demo',permissions:{admin:true},default_branch:'main'};
  }),/already exists/);
  assert.equal(writes,0);
});
test('initialization preserves edited files and refuses symlink destinations',()=>{
  const tmp=fs.mkdtempSync(path.join(os.tmpdir(),'omarchy-template-'));
  try {
    fs.cpSync(root,tmp,{recursive:true,filter:s=>!['.git','target','dist'].includes(path.basename(s))});
    const c=readJSON(path.join(tmp,'.template/project.json'));
    if(c.initialized)return; // End-to-end creation is tested on the template itself.
    const args=['scripts/init.mjs','--owner','tester','--repo','demo','--slug','demo','--name','Demo','--author','Test'];
    const run=()=>spawnSync(process.execPath,args,{cwd:tmp,encoding:'utf8'});
    fs.appendFileSync(path.join(tmp,'README.md'),'\nUser edit\n');
    assert.notEqual(run().status,0);
    assert(fs.readFileSync(path.join(tmp,'README.md'),'utf8').includes('User edit'));
    fs.copyFileSync(path.join(root,'README.md'),path.join(tmp,'README.md'));
    fs.renameSync(path.join(tmp,'README.md'),path.join(tmp,'outside.md'));
    fs.symlinkSync('outside.md',path.join(tmp,'README.md'));
    assert.notEqual(run().status,0);
  }finally{fs.rmSync(tmp,{recursive:true,force:true});}
});
