/* Wire format consumed by RuralScan/evidence workflows/submissions/intake.py. */
const BatchReceipt = (() => {
  const fixtures = {T4:'test_bench_terrace', 'T3/T6':'test_hazard_scorecard', M2b:'test_operational_risk'};
  const header = 'RuralScan submission v1\n';
  const size = str => new TextEncoder().encode(str).length;
  const reviewHeader = 'RuralScan review submission v2';
  const maxBytes = 1000000;
  function receiptBody(rows) {
    const lanes = new Set(rows.map(r => r.lane));
    const lane = lanes.size === 1 ? rows[0].lane : 'Mixed';
    const fields = ['evidence_id','reviewer','decision','reason','note'];
    if (lane === 'Mixed') fields.unshift('lane');
    const cell = v => '"' + v.replaceAll('"','""') + '"';
    const csv = [fields.join(','), ...rows.map(row => fields.map(f => cell(row[f])).join(','))].join('\n');
    return header + JSON.stringify({kind:'csv',lane,revision:rows[0].revision,
      test:rows[0].evidence_id === fixtures[rows[0].lane],payload:csv});
  }
  function chunks(rows) {
    const groups = new Map();
    for (const r of rows) {
      const group = r.revision + '/' + (r.evidence_id === fixtures[r.lane]);
      if (!groups.has(group)) groups.set(group,[[]]);
      const batches = groups.get(group);
      if (size(receiptBody([r])) > maxBytes) throw Error('One decision exceeds the submission limit. Shorten its note.');
      if (size(receiptBody([...batches.at(-1),r])) > maxBytes && batches.at(-1).length) batches.push([]);
      batches.at(-1).push(r);
    }
    return [...groups.values()].flat();
  }
  const sha256 = async text => [...new Uint8Array(await globalThis.crypto.subtle.digest('SHA-256', new TextEncoder().encode(text)))].map(x=>x.toString(16).padStart(2,'0')).join('');
  function metadata(body) {
    if (!body?.replaceAll('\r\n','\n').startsWith(reviewHeader+'\n')) return null;
    const found = [...body.replaceAll('\r\n','\n').matchAll(/<!-- ruralscan-review\n(.*?)\n-->/gs)];
    if (found.length !== 1) return null;
    try { return JSON.parse(found[0][1]); } catch { return null; }
  }
  const attachmentLinks = body => [...body.replace(/<!-- ruralscan-review\n.*?\n-->/gs,'').matchAll(/\[[^\]\n]+\]\((https:\/\/github\.com\/user-attachments\/files\/[0-9]+\/[^\s)]+\.csv)\)/g)].map(m=>m[1]);
  async function prepare(rows) {
    const entry = JSON.parse(receiptBody(rows).slice(header.length));
    const csv = entry.payload, hash = await sha256(csv);
    const meta = {kind:'csv',lane:entry.lane,revision:entry.revision,test:entry.test,sha256:hash,bytes:size(csv),count:rows.length};
    const filename = 'ruralscan-reviews-'+rows[0].reviewer+'-'+hash.slice(0,12)+'.csv';
    const title = (entry.test?'TEST · ':'')+'Review submission · '+rows.length+' decisions · '+rows[0].reviewer;
    const bodyFor = inline => reviewHeader+'\n\n'+rows.length+' review decisions for '+entry.lane+'.\n\n'
      +(inline?'Decisions are already included. Click **Create** to submit.':'Attach **'+filename+'** below, wait for upload to finish, then click **Create**. Do not edit the downloaded CSV.')
      +'\n\nSubmission records your votes; validation and register processing follow.\n\n'
      +'<!-- ruralscan-review\n'+JSON.stringify(inline?{...meta,payload:csv}:meta).replaceAll('<','\\u003c').replaceAll('>','\\u003e')+'\n-->\n';
    const urlFor = body => 'https://github.com/RuralScan/evidence/issues/new?'+new URLSearchParams({title,body});
    let body=bodyFor(true), url=urlFor(body), attachment=url.length>6000;
    if (attachment) { body=bodyFor(false); url=urlFor(body); }
    return {rows,meta,csv,filename,body,url,attachment,legacy:receiptBody(rows)};
  }
  function matches(issue, prepared) {
    if (issue.pull_request || issue.user?.login?.toLowerCase() !== prepared.rows[0].reviewer.toLowerCase()) return false;
    const body = issue.body?.replaceAll('\r\n','\n').trim();
    if (body === prepared.legacy) return true;
    const meta = metadata(body);
    if (!meta) return false;
    const expected = prepared.attachment?prepared.meta:{...prepared.meta,payload:prepared.csv};
    if (Object.keys(meta).length!==Object.keys(expected).length || Object.keys(expected).some(k=>meta[k]!==expected[k])) return false;
    const links=attachmentLinks(body);
    return prepared.attachment ? links.length===1 : links.length===0;
  }
  const historyPrefix = 'ruralscan.receipt.v1/';
  function history(storage, reviewer) {
    const prefix=historyPrefix+reviewer.toLowerCase()+'/';
    return Object.keys(storage).filter(k=>k.startsWith(prefix)).flatMap(k=>{
      try { const item=JSON.parse(storage.getItem(k)); return Array.isArray(item.rows)?[item]:[]; } catch { return []; }
    }).sort((a,b)=>b.number-a.number);
  }
  const pending = (rows, receipts) => rows.filter(row=>!receipts.some(r=>r.rows.some(old=>JSON.stringify(old)===JSON.stringify(row))));
  async function remember(storage, issue, prepared) {
    if (!matches(issue,prepared)) throw Error('Submission does not match these decisions. Your saved decisions are unchanged.');
    const item={number:issue.number,url:'https://github.com/RuralScan/evidence/issues/'+issue.number,
      reviewer:prepared.rows[0].reviewer,rows:prepared.rows,digest:await sha256(issue.body),state:'submitted'};
    storage.setItem(historyPrefix+item.reviewer.toLowerCase()+'/'+item.number,JSON.stringify(item));
    return item;
  }
  return {receiptBody, chunks, fixtures, header, reviewHeader, prepare, matches, metadata, sha256, maxBytes, history, pending, remember};
})();
if (typeof module !== 'undefined') module.exports = BatchReceipt;
