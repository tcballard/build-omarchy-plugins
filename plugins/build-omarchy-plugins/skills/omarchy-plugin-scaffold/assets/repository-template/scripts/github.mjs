#!/usr/bin/env node
import { spawnSync } from 'node:child_process';
import { root, readJSON } from './template.mjs';
import path from 'node:path';

export function policy(kind) {
  return {
    name:'Omarchy main', target:'branch', enforcement:'active',
    conditions:{ref_name:{include:['~DEFAULT_BRANCH'],exclude:[]}},
    bypass_actors:[],
    rules:[
      {type:'deletion'}, {type:'non_fast_forward'},
      {type:'pull_request',parameters:{required_approving_review_count:0,dismiss_stale_reviews_on_push:true,require_code_owner_review:false,require_last_push_approval:false,required_review_thread_resolution:true}},
      {type:'required_status_checks',parameters:{strict_required_status_checks_policy:true,required_status_checks:[{context:'verify'},...(kind==='app' ? [{context:'native'}] : [])]}},
    ],
  };
}
function gh(args, data) {
  const r = spawnSync('gh',args,{cwd:root,encoding:'utf8',input:data===undefined?undefined:JSON.stringify(data)});
  if (r.error || r.status !== 0) throw Error(r.error?.message || r.stderr || 'GitHub request failed');
  return r.stdout.trim() ? JSON.parse(r.stdout) : null;
}
export function configure(c, apply, template, api=gh) {
  const full = `${c.owner}/${c.repo}`;
  const desired = policy(c.kind);
  const settings = {allow_squash_merge:true,allow_merge_commit:false,allow_rebase_merge:false,delete_branch_on_merge:true,allow_auto_merge:true,has_wiki:false,...(template?{is_template:true}:{})};
  if (!apply) return {repository:full,settings,ruleset:desired,topics:['omarchy',`omarchy-${c.kind}`],note:'Dry run. --apply makes these changes using your authenticated gh session. No bypass actors; solo maintainers use PRs with green CI and no mandatory second reviewer.'};
  const repo = api(['api',`repos/${full}`]);
  if (repo.full_name.toLowerCase() !== full.toLowerCase() || !repo.permissions?.admin) throw Error('Repository admin access required');
  if (repo.default_branch !== 'main') throw Error('Expected main as default branch; inspect before changing policy');
  const current = api(['api','--paginate','--slurp',`repos/${full}/rulesets`]).flat();
  const own = current.filter(r=>r.name===desired.name && r.source===repo.full_name && r.source_type==='Repository');
  if (own.length) {
    // Never weaken an existing policy or discard a maintainer's edits on rerun.
    throw Error('An Omarchy main ruleset already exists. Inspect it; this command will not replace existing rules.');
  }
  api(['api','--method','PATCH',`repos/${full}`,'--input','-'],settings);
  api(['api','--method','PUT',`repos/${full}/topics`,'--input','-'],{names:[...new Set([...(repo.topics||[]),'omarchy',`omarchy-${c.kind}`])]});
  const created = api(['api','--method','POST',`repos/${full}/rulesets`,'--input','-'],desired);
  const actual = api(['api',`repos/${full}/rulesets/${created.id}`]);
  const updated = api(['api',`repos/${full}`]);
  if (actual.enforcement!=='active' || !actual.rules.some(r=>r.type==='required_status_checks') || Object.entries(settings).some(([k,v])=>updated[k]!==v)) throw Error('GitHub settings verification failed; inspect repository settings');
  return {repository:updated.html_url,ruleset:actual.id,verified:true};
}
if (process.argv[1] === new URL(import.meta.url).pathname) {
  try {
    const args=process.argv.slice(2);
    if (args.some(a=>!['--apply','--template'].includes(a))) throw Error('Usage: node scripts/github.mjs [--apply] [--template]');
    const c=readJSON(path.join(root,'.template/project.json'));
    if (!c.initialized && !args.includes('--template')) throw Error('Initialize the project first, or explicitly configure the template repository with --template');
    console.log(JSON.stringify(configure(c,args.includes('--apply'),args.includes('--template')),null,2));
  } catch(e) { console.error(e.message);process.exitCode=1; }
}
