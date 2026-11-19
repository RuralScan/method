const {test} = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const crypto = require('node:crypto');

function node(tag, text = '') {
  return {tag, textContent:text, children:[], dataset:{}, isConnected:true, listeners:{}, style:{}, setAttribute(key,value){this[key]=value;},
    append(...children) { this.children.push(...children); },
    replaceChildren(...children) { this.children = children; },
    addEventListener(type, callback) { this.listeners[type] = callback; },
    querySelector() { return this.children.find(c => c.tag === 'div'); },
    matches(selector) { return selector === 'details.source-preview' && this.dataset.preview; }};
}
function walk(root) { return [root, ...root.children.filter(c => typeof c === 'object').flatMap(walk)]; }
async function preview({connected = false, offline = false, library = true, item = null, legacy = false, restricted = false, stale = false} = {}) {
  let toggle, reads = 0, manifestReads = 0;
  const host = node('div'), panel = node('details'); panel.dataset.preview = 'finding'; panel.open = true; panel.append(host);
  const context = {window:{}, TextEncoder, crypto:crypto.webcrypto, document:{createElement:node, addEventListener(type, handler) { if (type === 'toggle') toggle = handler; }},
    LocalLibrary:{subscribe(){}, state:()=>({status:connected?'ready':'empty'}), async pdf(){ reads++; return {status:'found', path:'paper.pdf', url:'blob:fixture'}; }},
    reviewData:{registerRevision:'a'.repeat(40), revision:'b'.repeat(40), legacyPreviews:new Set(legacy?['finding']:[]), registers:{EV_evidence_register:[{evidence_id:'finding',source_id:'paper',page:4}],
      SRC_source_register:[{source_id:'paper',citation:'Test source',library_path:library?'library/paper.pdf':'',url:'https://example.org/paper'}]}},
    vfSharePointUrl: path => 'https://example.sharepoint.com/'+path,
    fetch:async(url)=>{
      if (url.endsWith('manifest.json')) { manifestReads++; return {ok:true,json:async()=>({eids:['finding'],sharepoint:restricted?{finding:'restricted/crop.jpg'}:{}})}; }
      if (offline) throw Error('offline');return {ok:true,json:async()=>item?{finding:item}:{}};}};
  if (item) {
    const ev=context.reviewData.registers.EV_evidence_register[0], src=context.reviewData.registers.SRC_source_register[0];
    const values=['source_id','page','locator_type','locator','quote','claim_basis'].map(k=>ev[k]);
    values.push(...['url','library_path','access_status','license','doi'].map(k=>src[k]));
    item.key=stale?'old-key':crypto.createHash('sha256').update(JSON.stringify(values.map(v=>String(v||'')))).digest('hex');
  }
  vm.createContext(context);vm.runInContext(fs.readFileSync('review/source-previews.js','utf8'),context);
  toggle({target:panel});
  for(let i=0;i<50 && !host.children.length;i++) await new Promise(resolve=>setTimeout(resolve,2));
  await new Promise(resolve=>setTimeout(resolve,5));
  return {host, reads:()=>reads, manifestReads:()=>manifestReads};
}

test('missing or unavailable previews keep online sources usable without local-folder setup',async()=>{
  for (const offline of [false,true]) {
    const p=await preview({offline});const nodes=walk(p.host);
    assert.ok(nodes.some(n=>n.tag==='a' && n.href==='https://example.sharepoint.com/library/paper.pdf#page=4'));
    assert.ok(nodes.some(n=>n.tag==='a' && n.href==='https://example.org/paper'));
    assert.equal(p.reads(),0);
    assert.equal(nodes.some(n=>n.tag==='button'),false,'no unsolicited folder connection prompt');
    const optional=nodes.find(n=>n.className==='local-source-preview');assert.equal(optional.open,false);
    optional.open=true;await optional.listeners.toggle();await new Promise(resolve=>setImmediate(resolve));
    assert.equal(p.reads(),1);assert.ok(walk(p.host).some(n=>n.tag==='iframe'));
  }
});

test('website-only sources and existing local connections retain their access routes',async()=>{
  const web=await preview({library:false});
  assert.ok(walk(web.host).some(n=>n.tag==='a' && n.href==='https://example.org/paper'));
  assert.equal(web.reads(),0);
  const local=await preview({connected:true});
  const optional=walk(local.host).find(n=>n.className==='local-source-preview');
  assert.equal(optional.open,true);
  optional.listeners.toggle();await new Promise(resolve=>setImmediate(resolve));
  assert.equal(local.reads(),1);
});


test('a matched text excerpt does not hide an eligible archived PDF region',async()=>{
  const p=await preview({item:{page:4,match:'Excerpt',partial:true},legacy:true});
  const nodes=walk(p.host), image=nodes.find(n=>n.tag==='img');
  assert.equal(image.src,'https://raw.githubusercontent.com/CIAT/nbs_ruralscan/'+ 'b'.repeat(40) +'/docs/crops/finding.jpg');
  assert.ok(nodes.find(n=>n.tag==='figcaption').textContent.startsWith('Figure 1. PDF page 4:'));
  assert.ok(nodes.indexOf(image)<nodes.findIndex(n=>n.tag==='blockquote'),'PDF context precedes text');
  assert.equal(p.reads(),0);assert.equal(p.manifestReads(),1);
});

test('current PDF image takes precedence and retains highlight overlays',async()=>{
  const p=await preview({item:{page:4,match:'Excerpt',image:'c'.repeat(64)+'.webp',boxes:[[.1,.2,.3,.4]]},legacy:true});
  const nodes=walk(p.host);
  assert.ok(nodes.find(n=>n.tag==='img').src.includes('/publication/source-previews/pages/'));
  assert.equal(nodes.find(n=>n.tag==='i').style.left,'10%');
  assert.equal(p.manifestReads(),0);
});

test('text-only previews retain optional local PDF access and source changes forbid legacy reuse',async()=>{
  for (const stale of [false,true]) {
    const p=await preview({item:{page:4,match:'Excerpt'},stale});
    const nodes=walk(p.host);
    assert.equal(nodes.some(n=>n.tag==='img'),false);
    assert.ok(nodes.some(n=>n.className==='local-source-preview'));
    assert.equal(p.manifestReads(),0);assert.equal(p.reads(),0);
  }
});

test('restricted archived crops remain authenticated links, including when a text match exists',async()=>{
  const p=await preview({item:{page:4,match:'Excerpt'},legacy:true,restricted:true});
  const nodes=walk(p.host);
  assert.equal(nodes.some(n=>n.tag==='img'),false);
  assert.ok(nodes.some(n=>n.tag==='a' && n.href==='https://example.sharepoint.com/restricted/crop.jpg'));
  assert.ok(nodes.some(n=>n.className==='local-source-preview'));
});
