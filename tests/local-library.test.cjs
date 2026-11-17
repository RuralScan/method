const {test} = require('node:test');
const assert = require('node:assert/strict');
const {create, match} = require('../review/local-library.js');

function pdfHandle(name, contents='%PDF-1.7\nfixture', modified=1) {
  let reads=0;
  return {kind:'file',name, get reads(){return reads;}, async getFile(){reads++;return {
    name,size:contents.length,lastModified:modified,slice:(a,b)=>({text:async()=>contents.slice(a,b)})
  };}};
}
function folder(name, children, permission='granted') {
  return {kind:'directory',name, permission, permissions:[],
    async *values(){yield* children;},
    async queryPermission(options){this.permissions.push(options);return this.permission;},
    async requestPermission(options){this.permissions.push(options);return this.permission;}
  };
}
function setup(saved=null,picked=saved) {
  const storage={saved,async get(){return this.saved;},async set(value){this.saved=value;},async remove(){this.saved=null;}};
  const revoked=[],picks=[];let next=0;
  const make=()=>create({store:storage,pick:async options=>{picks.push(options);if(picked instanceof Error)throw picked;return picked;},
    createURL:()=> 'blob:test-'+(++next),revokeURL:url=>revoked.push(url)});
  return {make,storage,revoked,picks};
}
const ev={source_id:'zhao'},src={library_path:'project/library/riparian/zhao.pdf'};

test('folder connection indexes subfolders without reading PDFs, and reload restores it',async()=>{
  const target=pdfHandle('zhao.pdf'),unopened=pdfHandle('other.pdf');
  const root=folder('library',[folder('riparian',[target]),unopened]);
  const f=setup(null,root),a=f.make();await a.ready;await a.connect();
  assert.equal(a.state().count,2);assert.equal(target.reads,0);assert.equal(unopened.reads,0);
  assert.equal(f.picks[0].mode,'read');assert.equal(f.storage.saved,root);
  const result=await a.pdf(ev,src);assert.equal(result.status,'found');assert.equal(result.path,'riparian/zhao.pdf');
  assert.equal(unopened.reads,0);
  const b=f.make();await b.ready;assert.equal(b.state().status,'ready');
  assert.equal((await b.pdf(ev,src)).status,'found');assert.equal(f.picks.length,1);
  assert.ok(root.permissions.every(p=>p.mode==='read'));
});

test('remembered folder waits for permission without reading files or opening picker',async()=>{
  const target=pdfHandle('zhao.pdf'),root=folder('library',[target],'prompt'),f=setup(root),a=f.make();await a.ready;
  assert.equal(a.state().status,'permission');assert.equal((await a.pdf(ev,src)).status,'permission');
  assert.equal(target.reads,0);assert.equal(f.picks.length,0);
  await a.allow();assert.equal(a.state().status,'permission');
  root.permission='granted';await a.allow();assert.equal((await a.pdf(ev,src)).status,'found');
  assert.equal(f.picks.length,0);
});

test('registered path disambiguates filenames; ambiguous basenames never choose a random PDF',()=>{
  const entries=[{path:'riparian/zhao.pdf'},{path:'wetlands/zhao.pdf'}];
  assert.equal(match(entries,ev,src).entry.path,'riparian/zhao.pdf');
  assert.equal(match(entries,ev,{}).status,'ambiguous');
  assert.equal(match([{path:'cache/ZHAO.PDF'}],ev,src).entry.path,'cache/ZHAO.PDF');
  assert.equal(match(entries,{source_id:'unknown'},{}).status,'missing');
});

test('disconnect removes stored handle, revokes previews, and stops future local reads',async()=>{
  const target=pdfHandle('zhao.pdf'),f=setup(folder('library',[target])),a=f.make();await a.ready;
  const before=await a.pdf(ev,src);await a.disconnect();
  assert.equal(f.storage.saved,null);assert.deepEqual(f.revoked,[before.url]);
  assert.equal((await a.pdf(ev,src)).status,'empty');assert.equal(target.reads,1);
});

test('cancelled chooser preserves existing connection and preview',async()=>{
  const error=Object.assign(new Error('cancelled'),{name:'AbortError'});
  const f=setup(folder('library',[pdfHandle('zhao.pdf')]),error),a=f.make();await a.ready;
  const before=await a.pdf(ev,src);await a.connect();
  assert.equal(a.state().status,'ready');assert.equal((await a.pdf(ev,src)).url,before.url);
  assert.equal(f.revoked.length,0);
});

test('refresh discovers new files and missing or invalid PDFs fail clearly',async()=>{
  const children=[],f=setup(folder('library',children)),a=f.make();await a.ready;
  assert.equal((await a.pdf(ev,src)).status,'missing');
  children.push(pdfHandle('zhao.pdf'));await a.refresh();assert.equal((await a.pdf(ev,src)).status,'found');
  children[0]=pdfHandle('zhao.pdf','not a PDF');await a.refresh();
  assert.equal((await a.pdf(ev,src)).status,'invalid');
});

test('inaccessible file reports unavailable; revoked permission offers reconnection',async()=>{
  const entry=pdfHandle('zhao.pdf'),f=setup(folder('library',[entry])),a=f.make();await a.ready;
  entry.getFile=async()=>{throw Object.assign(new Error('offline'),{name:'NotFoundError'});};
  assert.equal((await a.pdf(ev,src)).status,'unavailable');
  entry.getFile=async()=>{throw Object.assign(new Error('denied'),{name:'NotAllowedError'});};
  assert.equal((await a.pdf(ev,src)).status,'permission');
});

test('file-input fallback includes relative subfolders and makes session-only status explicit',async()=>{
  const f=setup(),a=f.make();await a.ready;
  const file=await pdfHandle('zhao.pdf').getFile();file.webkitRelativePath='library/riparian/zhao.pdf';
  await a.useFiles([file]);assert.equal(a.state().sessionOnly,true);assert.equal(a.state().remembered,false);
  assert.equal((await a.pdf(ev,src)).status,'found');assert.equal(f.storage.saved,null);
});

test('blocked browser storage still permits temporary connection',async()=>{
  const a=create({store:{get:async()=>{throw Error('blocked');},set:async()=>{throw Error('blocked');}},
    pick:async()=>folder('library',[pdfHandle('zhao.pdf')]),createURL:()=> 'blob:temp',revokeURL:()=>{}});
  await a.ready;await a.connect();assert.equal(a.state().remembered,false);
  assert.equal((await a.pdf(ev,src)).status,'found');
});

test('disconnect during scan cannot reconnect a stale folder',async()=>{
  let release;const pause=new Promise(resolve=>{release=resolve;});
  const root=folder('library',[]);root.values=async function*(){await pause;yield pdfHandle('zhao.pdf');};
  const f=setup(null,root),a=f.make();await a.ready;
  const connecting=a.connect();await new Promise(resolve=>setImmediate(resolve));
  await a.disconnect();release();await connecting;
  assert.equal(a.state().status,'empty');assert.equal((await a.pdf(ev,src)).status,'empty');assert.equal(f.storage.saved,null);
});
