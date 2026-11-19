const {test} = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');

function node(tag, text = '') {
  return {tag, textContent:text, children:[], dataset:{}, isConnected:true, listeners:{},
    append(...children) { this.children.push(...children); },
    replaceChildren(...children) { this.children = children; },
    addEventListener(type, callback) { this.listeners[type] = callback; },
    querySelector() { return this.children.find(c => c.tag === 'div'); },
    matches(selector) { return selector === 'details.source-preview' && this.dataset.preview; }};
}
function walk(root) { return [root, ...root.children.filter(c => typeof c === 'object').flatMap(walk)]; }
async function preview({connected = false, offline = false, library = true} = {}) {
  let toggle, reads = 0;
  const host = node('div'), panel = node('details'); panel.dataset.preview = 'finding'; panel.open = true; panel.append(host);
  const context = {window:{}, document:{createElement:node, addEventListener(type, handler) { if (type === 'toggle') toggle = handler; }},
    LocalLibrary:{subscribe(){}, state:()=>({status:connected?'ready':'empty'}), async pdf(){ reads++; return {status:'found', path:'paper.pdf', url:'blob:fixture'}; }},
    reviewData:{registerRevision:'a'.repeat(40), registers:{EV_evidence_register:[{evidence_id:'finding',source_id:'paper',page:4}],
      SRC_source_register:[{source_id:'paper',citation:'Test source',library_path:library?'library/paper.pdf':'',url:'https://example.org/paper'}]}},
    vfSharePointUrl: path => 'https://example.sharepoint.com/'+path,
    fetch:async()=>{if (offline) throw Error('offline');return {ok:true,json:async()=>({})};}};
  vm.createContext(context);vm.runInContext(fs.readFileSync('review/source-previews.js','utf8'),context);
  toggle({target:panel});await new Promise(resolve=>setImmediate(resolve));
  return {host, reads:()=>reads};
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
