/* Review controller. Classic-script callbacks preserve existing cards and integrations.
 * Host contract and release process: review/README.md. */
  async function loadReviewSnapshot(base) {
    const meta = document.querySelector('meta[name="ciat-review-snapshot"]');
    if (!meta) return base;
    const response = await fetch(meta.content);
    if (!response.ok) throw Error('Could not load the CIAT review snapshot.');
    const data = await response.json();
    const registers = {...base.registers};
    for (const [name, key] of [['EV_evidence_register', 'evidence_id'], ['SRC_source_register', 'source_id']]) {
      const rows = new Map(base.registers[name].map(row => [row[key], row]));
      const {removed, changed} = data.register_changes[name];
      for (const id of removed) rows.delete(id);
      for (const row of changed) rows.set(row[key], row);
      registers[name] = [...rows.values()];
    }
    // Resolve main once, then read every official record from that immutable revision.
    const revisionResponse = await fetch('https://api.github.com/repos/RuralScan/evidence/commits/main', {cache:'no-cache'});
    if (!revisionResponse.ok) throw Error('Could not resolve the RuralScan register revision.');
    const {sha} = await revisionResponse.json();
    if (!/^[0-9a-f]{40}$/.test(sha)) throw Error('Invalid RuralScan register revision.');
    const liveResponse = await fetch('https://raw.githubusercontent.com/RuralScan/evidence/'+sha+'/publication/review-queue.json');
    if (!liveResponse.ok) throw Error('Could not load official RuralScan review records.');
    const live = await liveResponse.json();
    // A legacy crop can be reused only while both its locator and source still match.
    const archivedUnits = new Map(registers.EV_evidence_register.map(r => [r.evidence_id,r]));
    const archivedSources = new Map(registers.SRC_source_register.map(r => [r.source_id,r]));
    const liveSources = new Map(live.registers.SRC_source_register.map(r => [r.source_id,r]));
    const same = (a,b,fields) => a && b && fields.every(k => (a[k] ?? '') === (b[k] ?? ''));
    const legacyPreviews = new Set(live.registers.EV_evidence_register.filter(r =>
      same(r,archivedUnits.get(r.evidence_id),['source_id','quote','page','locator','locator_type']) &&
      same(liveSources.get(r.source_id),archivedSources.get(r.source_id),['doi','url','library_path','access_status','license'])
    ).map(r => r.evidence_id));
    const priority = live.priority_requests ? [...live.priority_requests] : [...data.review_priorities];
    if (!live.priority_requests) for (const [batch_id, batch] of Object.entries(live.batches)) {
      for (const evidence_id of batch.ids) priority.push({batch_id, batch_label:batch.title, evidence_id, priority:'normal'});
    }
    return {...base, ...data, ...live, registers:{...registers,...live.registers}, review_priorities:priority, registerRevision:sha, legacyPreviews};
  }

  // VERIFY-FLAG worklist toggle & renderer
  window._vfVerdictFilter = 'all';
  window._vfWorklistOpen = false;

  function toggleVfWorklist() {
    window._vfWorklistOpen = !window._vfWorklistOpen;
    const panel = document.getElementById('ev-vf-worklist');
    const hint = document.getElementById('evq-worklist-toggle-hint');
    if (!panel) return;
    if (window._vfWorklistOpen) {
      panel.style.display = 'block';
      if (hint) hint.textContent = '▲ Hide VERIFY-FLAG worklist';
      renderVfWorklist();
    } else {
      panel.style.display = 'none';
      if (hint) hint.textContent = '▼ Show VERIFY-FLAG worklist';
    }
  }

  function vfEsc(v){ return (v==null?'':String(v)).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;'); }
  // library_path (e.g. D591_Rural-Scan_NBS/2_Technical_&_Data/library/.../x.pdf) -> SharePoint web URL.
  // Works for any team member with access to the Alliance-ClimateActionNetZero library — no local server.
  // soft-deleted (QA-dropped) EV rows are moved out of the analytical register into
  // data._evDropped so every count/synthesis view excludes them; QA views read _evDropped.
  // Live-server /api/crop failed to render (usually: PDF not synced to disk on this
  // reviewer's machine — the OneDrive folder is cloud-only). Don't dead-end at "crop
  // unavailable": fall back to the pre-rendered SharePoint crop (restricted sources) or
  // the SharePoint PDF, so the reviewer can still reach the source. Copyright-safe — both
  // are access-controlled library links, never inline public content.
  function vfCropOnErr(eid,img){
    var d=document.createElement('div');
    if((window._cropManifest||new Set()).has(eid) && !img.dataset.cropFallback){
      img.dataset.cropFallback='1';
      d.textContent='Full page unavailable locally. Showing saved crop; caption may be incomplete. Use source PDF link for context.';
      img.before(d); img.src='https://raw.githubusercontent.com/CIAT/nbs_ruralscan/'+(reviewData.revision || 'bec50bc0f9dc74b3d5ffafcf881571a8a8ec5c06')+'/docs/crops/'+encodeURIComponent(eid)+'.jpg'; return;
    }
    var spCrop=(window._cropSharePointMap||{})[eid];
    if(spCrop){ var u=vfSharePointUrl(spCrop); if(u){ d.style.cssText='font-size:10.5px; color:var(--text-secondary); padding:8px 4px;'; d.innerHTML='PDF not synced on this machine — <a href="'+u+'" target="_blank" rel="noopener noreferrer" style="color:var(--accent-sky);">open highlighted source region in SharePoint ↗</a><div style="font-size:9.5px; color:var(--text-muted); margin-top:4px;">needs CGIAR library access. To see crops inline, make the library available offline in OneDrive (see the <a href="https://github.com/CIAT/nbs_ruralscan/blob/main/docs/REVIEWER_GUIDE.md" target="_blank" rel="noopener noreferrer" style="color:var(--accent-sky);">reviewer guide</a>).</div>'; img.replaceWith(d); return; } }
    var evAll=((reviewData||{}).registers||{}).EV_evidence_register||[]; var ev=evAll.find(function(e){return e.evidence_id===eid;})||{};
    var srcAll=((reviewData||{}).registers||{}).SRC_source_register||[]; var src=srcAll.find(function(s){return s.source_id===ev.source_id;})||{};
    var pdf=vfSharePointUrl(src.library_path||''); if(pdf&&ev.page)pdf+='#page='+ev.page;
    d.style.cssText='font-size:10.5px; color:var(--text-muted); padding:8px 4px;';
    d.innerHTML=pdf?('PDF not synced on this machine — <a href="'+pdf+'" target="_blank" rel="noopener noreferrer" style="color:var(--accent-sky);">open in SharePoint'+(ev.page?(' p.'+ev.page):'')+' ↗</a> <span style="color:var(--text-muted);">(needs CGIAR access; or sync the library offline in OneDrive)</span>'):'crop unavailable — PDF not synced and no SharePoint copy for this source.';
    img.replaceWith(d);
  }
  // Task 3: click a card's source / page chip to subset the worklist to that paper / location.
  // Toggling the same value clears it. Applies via _inScope, so it works across flagged/passed.
  function vfSetSubset(kind,val){ if(window.DashboardPriority)DashboardPriority.leaveFocus(); if(!window._vfScope)window._vfScope={}; val=(val==null?'':String(val)); window._vfScope[kind]=(window._vfScope[kind]===val?'':val); renderVfWorklist(); }
  // Task (chips): clicking a card's OA / channel / NbS / sub-practice chip sets that scope
  // filter (single-value, like the sidebar pills) so the worklist narrows to matching cards.
  function vfScopeSet(key,val){ if(window.DashboardPriority)DashboardPriority.leaveFocus(); if(!window._vfScope)window._vfScope={}; window._vfScope[key]=val; if(key==='nbs'){ window._vfScope.family='all'; window._vfScope.round='all'; } if(key==='table')history.replaceState(null,'',DashboardPriority.route()); renderVfWorklist(); }
  // Uniform little pill for the card chip row — matches the OA / channel badge look so the
  // NbS / sub-practice / location / source chips all read as one consistent chip set.
  function _vfChip(label,color,title,onclick,noCaps){ return '<span '+(onclick?('onclick="'+onclick+'" '):'')+'title="'+vfEsc(title||'')+'" style="'+(onclick?'cursor:pointer; ':'')+'font-size:9.5px; font-weight:700; '+(noCaps?'':'text-transform:uppercase; ')+'letter-spacing:.03em; color:'+color+'; border:1px solid '+color+'; border-radius:3px; padding:1px 6px; white-space:nowrap;">'+label+'</span>'; }
  // Task D: report MISSING evidence (a variable/figure a reviewer expected but that was never
  // extracted). Writes a row to the in-repo gaps register via /api/gap; shown in the Gaps queue.
  function openGapModal(){ var m=document.getElementById('gap-modal'); if(!m)return;
    var dl=document.getElementById('gap-src-list'); if(dl){ var srcs=(((reviewData||{}).registers||{}).SRC_source_register||[]).map(function(s){return s.source_id;}).filter(Boolean).sort(); dl.innerHTML=srcs.map(function(s){return '<option value="'+vfEsc(s)+'"></option>';}).join(''); }
    var sc=window._vfScope||{}; var ctx=document.getElementById('gap-scope-ctx');
    if(ctx){ ctx.innerHTML='Filed against your current scope: <b>'+vfEsc(sc.nbs||'—')+'</b> · <b>'+vfEsc((sc.family&&sc.family!=='all')?familyDisplayName(sc.family):'all families and evidence scopes')+'</b> · <b>'+vfEsc(sc.table||'—')+'</b>'; }
    var msg=document.getElementById('gap-msg'); if(msg)msg.textContent='';
    if(!window._reviewApi){ if(msg)msg.innerHTML='<span style="color:var(--accent-amber);">No live review server — reporting a gap needs it running locally. It writes to pipeline/metrics/gaps.csv.</span>'; }
    m.style.display='block'; }
  function closeGapModal(){ var m=document.getElementById('gap-modal'); if(m)m.style.display='none'; }
  function submitGap(){ var msg=document.getElementById('gap-msg');
    if(!window._reviewApi){ if(msg)msg.innerHTML='<span style="color:var(--accent-rose);">No live review server — start it locally to log gaps.</span>'; return; }
    var sc=window._vfScope||{};
    var body={ reporter:(window._vfReviewer||'reviewer'), nbs_id:(sc.nbs&&sc.nbs!=='all'?sc.nbs:''), suitability_family_id:(sc.family&&sc.family!=='all'?sc.family:''), table:(sc.table||''), source_id:(document.getElementById('gap-source').value||'').trim(), location:(document.getElementById('gap-location').value||'').trim(), variable:(document.getElementById('gap-variable').value||'').trim(), note:(document.getElementById('gap-note').value||'').trim() };
    if(!body.variable && !body.note){ if(msg)msg.innerHTML='<span style="color:var(--accent-rose);">Enter at least a missing variable or a note.</span>'; return; }
    fetch('/api/gap',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(body)}).then(function(r){return r.json();}).then(function(res){
      if(res.error){ if(msg)msg.innerHTML='<span style="color:var(--accent-rose);">'+vfEsc(res.error)+'</span>'; return; }
      if(!reviewData.gaps)reviewData.gaps=[]; reviewData.gaps.push({gap_id:res.gap_id,date:'',reporter:body.reporter,nbs_id:body.nbs_id,suitability_family_id:body.suitability_family_id,table:body.table,source_id:body.source_id,location:body.location,variable:body.variable,note:body.note,status:'open'});
      ['gap-variable','gap-location','gap-note'].forEach(function(id){var el=document.getElementById(id); if(el)el.value='';});
      if(msg)msg.innerHTML='<span style="color:var(--accent-emerald);">Logged '+vfEsc(res.gap_id)+' — in pipeline/metrics/gaps.csv. Commit / submit to share it. See it in the ⚠ Gaps queue.</span>';
      if(typeof renderVfWorklist==='function')renderVfWorklist();
    }).catch(function(e){ if(msg)msg.innerHTML='<span style="color:var(--accent-rose);">Error: '+vfEsc(String(e))+'</span>'; }); }
  function renderVfGaps(host){ if(!host)return;
    var gaps=((reviewData||{}).gaps||[]).filter(_vfGapInScope).slice().reverse();
    var dc=document.getElementById('vf-decided-count'); if(dc)dc.innerHTML='<b>'+gaps.length+'</b> reported gap(s) — missing evidence flagged for a re-extraction sweep. <a href="#" onclick="openGapModal();return false;" style="color:var(--accent-amber);">+ report a gap</a>';
    host.innerHTML='';
    if(!gaps.length){ host.innerHTML='<div style="color:var(--text-muted); padding:14px; line-height:1.6;">No gaps reported yet. Use <b style="color:var(--accent-amber);">&#9888; Report missing evidence</b> (in the action bar above) to flag a variable / figure / table that should exist but isn\'t in the register — e.g. after checking every variable in Figure 7 has been extracted.</div>'; return; }
    gaps.forEach(function(g){ host.insertAdjacentHTML('beforeend',
      '<div style="border:1px solid var(--border-color); border-left:3px solid var(--accent-amber); border-radius:8px; padding:11px 14px; margin-bottom:9px; background:var(--bg-secondary);">'
      +'<div style="display:flex; align-items:center; gap:10px; flex-wrap:wrap;"><code style="color:var(--accent-amber); font-size:11.5px;">'+vfEsc(g.gap_id||'')+'</code>'
      +(g.variable?('<span style="font-size:11.5px; color:var(--text-primary); font-weight:600;">'+vfEsc(g.variable)+'</span>'):'')
      +(g.location?('<span style="font-size:10.5px; color:var(--text-secondary);">📍 '+vfEsc(g.location)+'</span>'):'')
      +(g.source_id?('<span style="font-size:10.5px; color:var(--text-muted);">'+vfEsc(g.source_id)+'</span>'):'')
      +'<span style="margin-left:auto; font-size:10px; color:var(--text-muted);">'+vfEsc(g.nbs_id||'')+(g.suitability_family_id?(' · '+vfEsc(familyDisplayName(g.suitability_family_id))):'')+(g.table?(' · '+vfEsc(g.table)):'')+'</span></div>'
      +(g.note?('<div style="font-size:11.5px; color:var(--text-secondary); margin-top:5px;">'+vfEsc(g.note)+'</div>'):'')
      +'<div style="font-size:10px; color:var(--text-muted); margin-top:6px;">'+vfEsc(g.reporter||'')+(g.date?(' · '+vfEsc(g.date)):'')+' · '+vfEsc(g.status||'open')+'</div>'
      +'</div>'); }); }
  // Task 2: how many of MY decisions are saved locally but NOT yet applied + submitted to main.
  // The store stamps each decision `applied:true` after Apply; pending = mine without it.
  function _vfPendingCount(){ var me=(window._vfReviewer||'').trim(); var all=window._vfAllReviews||{}; var n=0; Object.keys(all).forEach(function(eid){ var m=all[eid][me]; if(m&&m.decision&&m.applied!==true&&m.applied!=='true')n++; }); return n; }
  // Presentation only: with nothing pending, Apply reads as unavailable (muted + not-allowed).
  // Its show/hide (live vs offline) stays owned by updateVfMode, and we never touch .disabled,
  // so the in-flight "Applying…" state set by applyVfDecisions is never disturbed.
  function _vfStyleApply(n){ var b=document.getElementById('vf-apply-btn'); if(!b)return;
    b.style.opacity=(n>0?'1':'0.45'); b.style.cursor=(n>0?'pointer':'not-allowed'); }
  function _vfUpdatePending(){ if(reviewData.registerRevision && !window._reviewApi){ReviewBatch.refresh();return;} var el=document.getElementById('vf-pending-count'); if(!el)return; var me=(window._vfReviewer||'').trim();
    if(!me){ el.innerHTML='<span style="color:var(--text-muted); font-weight:400;">Pick your reviewer handle above the queue to start deciding.</span>'; _vfStyleApply(0); return; }
    // Apply ships EVERY pending decision, across all queues — so this total is scope- and mode-independent.
    // Break it into AI-flagged + AI-passed origin so the reviewer sees exactly what will be submitted.
    var all=window._vfAllReviews||{}; var byId={}; ((reviewData.registers.EV_evidence_register)||[]).forEach(function(e){byId[e.evidence_id]=e;}); ((reviewData._evDropped)||[]).forEach(function(e){byId[e.evidence_id]=e;});
    var nf=0,np=0; Object.keys(all).forEach(function(eid){ var m=all[eid][me]; if(m&&m.decision&&m.applied!==true&&m.applied!=='true'){ var e=byId[eid]; if(e&&/\[VERIFY-FLAG/.test(e.attribution||''))nf++; else np++; } });
    var n=nf+np;
    var nc=window._vfClarificationPending||0;
    el.innerHTML=n>0?n+' decision'+(n===1?'':'s')+' ready to submit':(nc?'Discussion updates ready to submit':'All decisions submitted');
    if(n||nc)el.innerHTML+='<details style="font-weight:400;font-size:11px"><summary>Submission details</summary>Your '+n+' decisions across all queues'+(nc?', plus '+nc+' saved discussion updates (all reviewers)':'')+'.</details>';
    _vfStyleApply(n+nc); }
  function _vfRenderSubsetBanner(){ var el=document.getElementById('vf-subset-banner'); if(!el)return; var sc=window._vfScope||{}; var chips=[]; if(sc.sourceId)chips.push(['sourceId','📄 source: '+sc.sourceId, sc.sourceId]); if(sc.section)chips.push(['section','📍 page '+sc.section, sc.section]); if(!chips.length){ el.style.display='none'; el.innerHTML=''; return; } el.style.display='block'; el.innerHTML='<div style="display:flex; align-items:center; gap:8px; flex-wrap:wrap; background:rgba(14,165,233,0.08); border:1px solid rgba(14,165,233,0.3); border-radius:6px; padding:6px 10px; font-size:11px;"><span style="color:var(--text-muted); font-weight:700; text-transform:uppercase; letter-spacing:.04em;">Subset</span>'+chips.map(function(c){return '<span style="background:var(--bg-secondary); border:1px solid var(--border-color); border-radius:12px; padding:2px 9px;">'+vfEsc(c[1])+' <a href="#" title="remove this subset" onclick="vfSetSubset(\''+c[0]+'\',\''+vfEsc(String(c[2]))+'\');return false;" style="color:var(--accent-rose); text-decoration:none; font-weight:700;">✕</a></span>';}).join('')+'<a href="#" onclick="if(window.DashboardPriority)DashboardPriority.leaveFocus();window._vfScope.sourceId=\'\';window._vfScope.section=\'\';renderVfWorklist();return false;" style="color:var(--accent-sky); margin-left:auto;">clear all</a></div>'; }
  function vfSourcePages(ev){
    var pages={},c=ev.context||{};
    if(typeof c==='string'){try{c=JSON.parse(c);}catch(e){c={};}}
    function add(value,label){String(value||'').split(',').forEach(function(v){v=v.trim();if(/^[1-9][0-9]*$/.test(v))pages[v]=label+' · PDF p'+v;});}
    add(ev.page,'Quoted evidence');
    add((c.model_use||{}).page,'Model / weights');
    add((c.model_use_provenance||{}).page,'Weight evidence');
    // Verified supporting pages belong to the source, not just the questioned card.
    var sourceIssues=(window._vfClarifications||[]).filter(function(g){return ev.source_id&&g.source===ev.source_id;});
    sourceIssues.concat(vfClarificationsFor(ev.evidence_id)).forEach(function(g){(g.answers||[]).forEach(function(a){var sc=a.source_check||{};(sc.pdf_pages||[]).forEach(function(n){if(!pages[n])add(n,'Supporting evidence');});Object.keys(sc.page_labels||{}).forEach(function(n){if(/^[1-9][0-9]*$/.test(n))pages[n]=sc.page_labels[n]+' · PDF p'+n;});});});
    return Object.keys(pages).sort(function(a,b){return Number(a)-Number(b);}).map(function(n){return {page:Number(n),label:pages[n]};});
  }
  function vfSelectSourcePage(eid,page,button){
    var box=button.closest('.vf-crop'),url='/api/crop?eid='+encodeURIComponent(eid)+'&full=1&page='+page;
    var img=box.querySelector('img');img.src=url;img.removeAttribute('data-src0');img.style.transform='';img.onerror=function(){this.alt='Page unavailable; use Open original PDF.';};box.dataset.rot='0';
    box.querySelectorAll('[data-source-page]').forEach(function(b){b.disabled=Number(b.dataset.sourcePage)===Number(page);});
    box.querySelectorAll('a').forEach(function(a){if(a.getAttribute('href').indexOf('/api/crop?')===0)a.href=url;if(a.getAttribute('href').indexOf('/api/pdf?')===0)a.href=a.href.split('#')[0]+'#page='+page;});
  }
  function vfToggleCrop(eid,btn){ var box=btn.nextElementSibling; if(!box)return; if(box.style.display==='none'){ if(!box.dataset.loaded){ box.dataset.rot='0'; var q=encodeURIComponent(eid);
      // CODE source (tool / GEE script): render the actual code lines from /api/code — NOT a PDF
      // crop. Needs the live server (it fetches + caches the file from GitHub at the pinned commit).
      var _evAllC=((reviewData||{}).registers||{}).EV_evidence_register||[]; var _evC=_evAllC.find(function(e){return e.evidence_id===eid;})||{};
      if((_evC.locator_type||'')==='file_line'){
        if(!window._reviewApi){ box.innerHTML='<div style="font-size:10.5px; color:var(--text-muted); padding:8px 4px;">Code source — start the local review server to render the file lines, or use the GitHub link above.</div>'; box.dataset.loaded='1'; box.style.display='block'; btn.textContent='💻 hide source code'; return; }
        box.innerHTML='<div style="font-size:10px; color:var(--text-muted); padding:6px 4px;">loading code…</div>';
        fetch('/api/code?eid='+q).then(function(r){return r.json();}).then(function(cj){
          if(!cj||!cj.ok||!cj.lines){ box.innerHTML='<div style="font-size:10.5px; color:var(--accent-rose); padding:8px 4px;">Could not load code'+((cj&&cj.error)?(': '+vfEsc(cj.error)):'')+'</div>'; return; }
          var rows=cj.lines.map(function(ln){ var hot=(ln.n>=cj.target_start&&ln.n<=cj.target_end); return '<div style="display:flex; '+(hot?'background:rgba(245,158,11,0.18);':'')+'"><span style="width:46px; flex:0 0 46px; text-align:right; padding-right:10px; color:var(--text-muted); user-select:none;">'+ln.n+'</span><span style="white-space:pre; color:var(--text-primary);">'+vfEsc(ln.text)+'</span></div>'; }).join('');
          box.innerHTML='<div style="font-size:10px; color:var(--text-muted); margin-bottom:5px;">'+vfEsc(cj.path)+' · lines '+cj.start+'–'+cj.end+' · commit '+vfEsc((cj.commit||'').slice(0,7))+' <span style="color:var(--accent-amber);">(highlighted = cited line)</span></div><div style="max-height:60vh; overflow:auto; border:1px solid var(--border-color); border-radius:4px; font-family:ui-monospace,monospace; font-size:11px; line-height:1.5; padding:8px;">'+rows+'</div>';
        }).catch(function(e){ box.innerHTML='<div style="font-size:10.5px; color:var(--accent-rose); padding:8px 4px;">Code load error: '+vfEsc(String(e))+'</div>'; });
        box.dataset.loaded='1'; box.style.display='block'; btn.textContent='💻 hide source code'; return;
      }
      var manifest=window._cropManifest||new Set();
      if(manifest.has(eid) && !window._reviewApi){
        // 1) committed crop (works on Pages + local, zero setup). Highlight baked in; client-side rotate for sideways tables.
        box.innerHTML='<div style="display:flex; gap:10px; align-items:center; margin-bottom:5px;"><button onclick="vfRotateCrop(\''+eid+'\',this)" title="rotate 90° — for sideways/landscape tables" style="font-size:10px; padding:2px 9px; border-radius:4px; background:transparent; color:var(--accent-sky); border:1px solid var(--border-color); cursor:pointer;">↻ rotate</button><a href="https://raw.githubusercontent.com/CIAT/nbs_ruralscan/'+(reviewData.revision || 'bec50bc0f9dc74b3d5ffafcf881571a8a8ec5c06')+'/docs/crops/'+q+'.jpg" target="_blank" rel="noopener noreferrer" style="font-size:10px; color:var(--accent-sky);">open crop ↗</a><span style="font-size:9.5px; color:var(--text-muted);">scroll to see the whole region</span></div><div style="max-height:72vh; overflow:auto; border:1px solid var(--border-color); border-radius:4px;"><img src="https://raw.githubusercontent.com/CIAT/nbs_ruralscan/'+(reviewData.revision || 'bec50bc0f9dc74b3d5ffafcf881571a8a8ec5c06')+'/docs/crops/'+q+'.jpg" style="max-width:100%; display:block;" alt="source region screengrab" onerror="this.replaceWith(document.createTextNode(\'crop unavailable\'));"></div>';
      } else if(window._reviewApi){
        // 2) Prefer the full page on the live server: old committed crops may omit captions.
        box.innerHTML='<div style="display:flex; gap:10px; align-items:center; margin-bottom:5px;"><button onclick="vfRotateCrop(\''+eid+'\',this)" title="rotate 90° (server re-renders crisp) — for sideways/landscape tables" style="font-size:10px; padding:2px 9px; border-radius:4px; background:transparent; color:var(--accent-sky); border:1px solid var(--border-color); cursor:pointer;">↻ rotate</button><a href="/api/crop?eid='+q+'&full=1" target="_blank" rel="noopener noreferrer" style="font-size:10px; color:var(--accent-sky);">open full page ↗</a><span style="font-size:9.5px; color:var(--text-muted);">scroll to see the whole region</span></div><div style="max-height:72vh; overflow:auto; border:1px solid var(--border-color); border-radius:4px;"><img src="/api/crop?eid='+q+'&full=1" style="max-width:100%; display:block;" alt="source region screengrab" onerror="vfCropOnErr(\''+eid+'\',this)"></div>';
      } else if(window._cropSharePointMap && window._cropSharePointMap[eid]){
        // 3) non-OA crop lives in the access-controlled library — link (can't embed an
        // auth'd SharePoint image). Copyright-safe: same access control as the PDF.
        var spCrop=vfSharePointUrl(window._cropSharePointMap[eid]);
        box.innerHTML=spCrop?('<div style="font-size:10.5px; color:var(--text-secondary); padding:8px 4px;"><b style="color:#fbbf24;">Restricted (copyright) source.</b> The crop can\'t be published on the public site, so it opens in the team library instead — <a href="'+spCrop+'" target="_blank" rel="noopener noreferrer" style="color:var(--accent-sky);">open highlighted source region in SharePoint ↗</a><div style="font-size:9.5px; color:var(--text-muted); margin-top:4px;">Needs CGIAR library access. To see restricted crops inline instead, make the library available offline in OneDrive + run the local server (see the <a href="https://github.com/CIAT/nbs_ruralscan/blob/main/docs/REVIEWER_GUIDE.md" target="_blank" rel="noopener noreferrer" style="color:var(--accent-sky);">reviewer guide</a>). If the link won\'t open, request access from the library maintainer.</div></div>'):('<div style="font-size:10.5px; color:var(--text-muted); padding:8px 4px;">Highlighted crop is in the library but its link could not be built.</div>');
      } else {
        // 4) no committed crop, no server, no library crop → SharePoint PDF link.
        var evAll=((reviewData||{}).registers||{}).EV_evidence_register||[]; var ev=evAll.find(function(e){return e.evidence_id===eid;})||{};
        var srcAll=((reviewData||{}).registers||{}).SRC_source_register||[]; var src=srcAll.find(function(s){return s.source_id===ev.source_id;})||{};
        var sp=vfSharePointUrl(src.library_path||''); if(sp&&ev.page)sp+='#page='+ev.page;
        box.innerHTML=sp?('<div style="font-size:10.5px; color:var(--text-secondary); padding:8px 4px;">No committed crop and no local review server — <a href="'+sp+'" target="_blank" rel="noopener noreferrer" style="color:var(--accent-sky);">open source region in SharePoint'+(ev.page?(' p.'+ev.page):'')+' ↗</a></div>'):('<div style="font-size:10.5px; color:var(--text-muted); padding:8px 4px;">No committed crop, no review server, and no SharePoint copy for this source.</div>');
      }
      if(window._reviewApi && _evC.source_id){
        var pdfLink=document.createElement('a');
        pdfLink.href='/api/pdf?sid='+encodeURIComponent(_evC.source_id)+'#page='+(parseInt(_evC.page,10)||1);
        pdfLink.target='_blank'; pdfLink.rel='noopener noreferrer';
        pdfLink.textContent='Open original PDF — adjacent pages and full table';
        box.prepend(pdfLink);
      }
      if(window._reviewApi){
        var pages=vfSourcePages(_evC);
        if(pages.length>1)box.innerHTML='<div style="display:flex;gap:8px;flex-wrap:wrap;margin:8px 0">'+pages.map(function(p){return '<button data-source-page="'+p.page+'" onclick="vfSelectSourcePage(\''+eid+'\','+p.page+',this)" style="padding:7px;cursor:pointer">'+vfEsc(p.label)+'</button>';}).join('')+'</div>'+box.innerHTML;
      }
      box.dataset.loaded='1'; } box.style.display='block'; btn.textContent='📷 hide source region'; } else { box.style.display='none'; btn.textContent='📷 show source region'; } }
  // Client-side rotate (canvas) — works for committed crops, live /api/crop, and on GitHub Pages
  // (no server round-trip). Right-angle raster rotation is pixel-exact; swaps dims for 90/270 so the
  // rotated image still fits the container width. Falls back to a CSS transform if the canvas is tainted.
  function vfRotateCrop(eid,b){ var box=b.closest('.vf-crop'); if(!box)return; var img=box.querySelector('img'); if(!img)return;
    if(!img.dataset.src0){ img.dataset.src0=img.getAttribute('src'); }
    var rot=((parseInt(box.dataset.rot||'0',10)+90)%360); box.dataset.rot=String(rot);
    if(rot===0){ img.src=img.dataset.src0; img.style.transform=''; return; }
    var base=new Image(); base.crossOrigin='anonymous';
    base.onload=function(){ try{ var w=base.naturalWidth,h=base.naturalHeight; var c=document.createElement('canvas'); if(rot===90||rot===270){ c.width=h; c.height=w; } else { c.width=w; c.height=h; } var ctx=c.getContext('2d'); ctx.translate(c.width/2,c.height/2); ctx.rotate(rot*Math.PI/180); ctx.drawImage(base,-w/2,-h/2); img.style.transform=''; img.src=c.toDataURL('image/jpeg',0.92); }catch(e){ img.style.transform='rotate('+rot+'deg)'; } };
    base.src=img.dataset.src0; }
  function toggleVfStats(){ if(window._vfMode==='stats'){ window._vfMode=window._vfLastReviewMode||'flagged'; } else { window._vfLastReviewMode=(window._vfMode&&window._vfMode!=='stats')?window._vfMode:'flagged'; window._vfMode='stats'; } renderVfWorklist(); }
  function vfShowReasonHelp(){ var d=document.getElementById('vf-reason-codes'); if(!d)return; d.open=true; d.scrollIntoView({behavior:'smooth',block:'center'}); d.style.transition='background .3s'; d.style.background='rgba(14,165,233,0.14)'; setTimeout(function(){ d.style.background=''; },1300); }
  function vfSharePointUrl(lp){ if(!lp)return ''; var base='https://cgiar.sharepoint.com/sites/Alliance-ClimateActionNetZero/'+encodeURIComponent('Shared Documents')+'/ClimateActionNetZero/1_Projects/'; return base+lp.split('/').map(encodeURIComponent).join('/'); }
  function vfLocHint(ev){
    var cb=(ev.claim_basis||'');
    if(cb==='table') return '\uD83D\uDCCA in a Table';
    if(cb==='figure_read') return '\uD83D\uDCC8 in a Figure';
    if((ev.locator_type||'')==='section' && ev.locator) return '\u00A7 '+ev.locator;
    var q=ev.quote||''; var nl=(q.match(/\n/g)||[]).length; var nums=(q.match(/[0-9]/g)||[]).length;
    if(nl>=3 && nums>=4) return '\uD83D\uDCCA likely a table (cells flattened)';
    return '\u00B6 main text';
  }
  function vfReviewingConflict(id){
    return ((reviewData.registers||{}).EV_evidence_register||[]).some(function(e){return e.evidence_id===id&&e._reviewConflict;});
  }
  function setVfDecision(id,d){
    window._vfSaveQueue=(window._vfSaveQueue||Promise.resolve()).then(async function(){
      var me=window._vfReviewer||'reviewer';var val=d; // Repeated clicks are idempotent, not undo.
      if(window._reviewApi){
        vfNotice('Saving decision…');
        var response=await fetch('/api/decision',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({evidence_id:id,decision:val,reviewed_conflict:vfReviewingConflict(id),answered_issue_ids:vfClarificationsFor(id).filter(function(g){return g.answers.length;}).map(function(g){return g.id;}),reason:((window._vfReasons||{})[id]||''),note:((window._vfNotes||{})[id]||''),reviewer:me})});
        var result=await response.json();if(!response.ok||result.error)throw Error(result.error||'Save failed');
      }
      window._vfDecisions=window._vfDecisions||{};window._vfDecisions[id]=val;
      window._vfAllReviews=window._vfAllReviews||{};window._vfAllReviews[id]=window._vfAllReviews[id]||{};
      window._vfAllReviews[id][me]={decision:val,applied:false,reviewed_conflict_at:vfReviewingConflict(id)?new Date().toISOString():null};localStorage.setItem('vfDecisions',JSON.stringify(window._vfDecisions));if(window._reviewApi)await vfLoadClarifications();renderVfWorklist();vfNotice('Decision saved locally. Apply & submit when finished.');
    }).catch(function(e){vfNotice('Decision NOT saved: '+e.message+' — click again to retry.',true);});
  }
  // A per-card DROP must carry a coded reason (mirrors the bulk-flag + query-note guards).
  // Before this, per-card drops could be reason-less — the source of the blank-reason drops
  // in the July QA batch (2026-07 sweep-retro #4). Toggling an existing drop OFF still works
  // Repeated decisions are idempotent; use Reset for pending changes.
  function vfTryDrop(id){
    var r=((window._vfReasons||{})[id]||''); var n=((window._vfNotes||{})[id]||'').trim();
    if(!r){ vfNotice('Pick a reason first — a drop needs a coded reason (use the Reason selector to the left).'); return; }
    if(r==='other'&&!n){ vfNotice('Reason "other" needs a note explaining it.'); return; }
    setVfDecision(id,'drop'); }
  // Reclassify species/crop-specific evidence (2026-07): KEEP + retag claim_scope + taxon —
  // never drop. On apply, review.apply_decisions retags the row; synthesis routes it out of the
  // practice T4 surface but retains it for reuse. Toggling again clears the decision.
  function vfReclassify(id){
    if((window._vfDecisions||{})[id]==='reclassify'){ setVfDecision(id,'reclassify'); return; } // toggle off
    var taxon=(prompt('Reclassify as species / crop-specific — KEEP & bank for reuse (not dropped).\n\nEnter the taxon (e.g. Faidherbia albida, Coffea arabica):','')||'').trim();
    if(!taxon)return;
    var isCrop=confirm('Is this an agricultural CROP?\n\nOK = crop-specific (e.g. coffee, maize — re-includable for F5 shaded systems)\nCancel = tree / plant species-specific');
    var scope=isCrop?'crop_specific':'species_specific';
    if(!window._vfDecisions)window._vfDecisions={}; if(!window._vfReasons)window._vfReasons={}; if(!window._vfTaxa)window._vfTaxa={};
    window._vfDecisions[id]='reclassify'; window._vfReasons[id]='species_envelope'; window._vfTaxa[id]=taxon;
    localStorage.setItem('vfDecisions',JSON.stringify(window._vfDecisions));
    { var me=(window._vfReviewer||'reviewer'); if(!window._vfAllReviews)window._vfAllReviews={}; window._vfAllReviews[id]=window._vfAllReviews[id]||{}; window._vfAllReviews[id][me]={decision:'reclassify',reason:'species_envelope',note:('→ '+scope+' · taxon: '+taxon)}; }
    if(window._reviewApi){ fetch('/api/decision',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({evidence_id:id,decision:'reclassify',reason:'species_envelope',claim_scope:scope,taxon:taxon,note:'',reviewer:(window._vfReviewer||'reviewer')})}).catch(function(){}); }
    renderVfWorklist(); }
  function setVfReason(id,reason){ if(!window._vfReasons)window._vfReasons={}; window._vfReasons[id]=reason; localStorage.setItem('vfReasons',JSON.stringify(window._vfReasons));
    if(window._reviewApi && (window._vfDecisions||{})[id]){ fetch('/api/decision',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({evidence_id:id,decision:window._vfDecisions[id],reason:reason,note:((window._vfNotes||{})[id]||''),reviewer:(window._vfReviewer||'reviewer')})}).catch(function(){}); } }
  function setVfNote(id,note){ if(!window._vfNotes)window._vfNotes={}; window._vfNotes[id]=note; localStorage.setItem('vfNotes',JSON.stringify(window._vfNotes));
    if(window._reviewApi && (window._vfDecisions||{})[id]){ fetch('/api/decision',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({evidence_id:id,decision:window._vfDecisions[id],reason:((window._vfReasons||{})[id]||''),note:note,reviewer:(window._vfReviewer||'reviewer')})}).catch(function(){}); } }
  function _vfToggleBanner(){ var b=document.getElementById('readonly-banner'); if(b)b.style.display=window._reviewApi?'none':'flex'; }
  // Red 'new version — pull' banner (#191): only for local reviewers (API present). Polls
  // /api/version; shows when the local clone is behind origin/main. Data/decisions are safe
  // across a pull (decisions.json is gitignored).
  function checkReadiness(){
    if(!window._reviewApi)return;
    let el=document.getElementById('vf-readiness');
    if(!el){el=document.createElement('div');el.id='vf-readiness';el.setAttribute('role','status');el.style.cssText='margin:10px 0;padding:10px;border:1px solid var(--border-color);font-size:12px;line-height:1.6';const anchor=document.getElementById('vf-mode-hint');if(anchor)anchor.parentNode.insertBefore(el,anchor);}
    fetch('/api/readiness').then(r=>r.ok?r.json():null).then(v=>{
      if(!v||!v.known){el.textContent='Source-cache readiness unavailable. Refresh after restarting the review server.';return;}
      el.innerHTML='<b>Source cache: '+v.cached+' / '+v.total+' present.</b> '+(v.ready?'Presence check passed; Apply still verifies source provenance.':'Missing '+v.missing.length+' source(s). Run <code>uv run python scripts/hydrate-corpus.py</code> from the repository, then recheck. On Windows, set <code>NBS_LIBRARY_ROOT</code> to your synced library folder. Decisions remain saved.')+' <button type="button" onclick="checkReadiness()">Recheck</button>';
      if(v.missing.length)el.innerHTML+='<details><summary>Missing source IDs</summary>'+v.missing.map(vfEsc).join(', ')+'</details>';
    }).catch(()=>{el.textContent='Source-cache check failed. Check the local review server; decisions remain saved.';});
  }
  function checkVersion(){
    if(!window._reviewApi)return;
    fetch('/api/version').then(function(r){return r.ok?r.json():null;}).then(function(v){
      var id='vf-version-banner'; var el=document.getElementById(id);
      if(v&&v.behind){
        if(!el){ el=document.createElement('div'); el.id=id;
          el.style.cssText='position:fixed; top:0; left:0; right:0; z-index:99999; background:#e11d48; color:#fff; font-size:12.5px; line-height:1.5; padding:8px 16px; text-align:center; box-shadow:0 2px 8px rgba(0,0,0,.35);';
          document.body.appendChild(el); document.body.style.paddingTop='40px'; }
        el.innerHTML='&#9888; <b>New version on main</b> — your local copy is behind (<code>'+vfEsc(v.local||'?')+'</code> vs <code>'+vfEsc(v.remote||'?')+'</code>). Finish &amp; <b>Apply</b> your current decisions, then <code>git pull</code> &#8594; <code>python3 scripts/hydrate-corpus.py</code> &#8594; <b>restart the server</b> &#8594; hard-reload. <span style="opacity:.85;">Pending decisions are safe (decisions.json is gitignored).</span>';
      } else if(el){ el.remove(); document.body.style.paddingTop=''; }
    }).catch(function(){});
  }
  async function vfFetchDecisions(){
    const response=await fetch('/api/state');
    const state=await response.json();
    function record(value){ return value!==null && typeof value==='object' && !Array.isArray(value); }
    if(!response.ok || (state && state.error)){
      throw Error((state && state.error) || 'Review server returned HTTP '+response.status);
    }
    const all=state && state.decisions;
    if(!record(all) || !Object.values(all).every(byReviewer=>record(byReviewer) && Object.values(byReviewer).every(record))){
      throw Error('The review server returned an invalid decision store.');
    }
    return all;
  }
  function vfUseDecisions(all){
    const me=window._vfReviewer || 'reviewer';
    const decisions={}, reasons={}, notes={};
    for(const [eid, byReviewer] of Object.entries(all)){
      const entry=byReviewer[me];
      if(entry && entry.decision){
        decisions[eid]=entry.decision;
        reasons[eid]=entry.reason || '';
        notes[eid]=entry.note || '';
      }
    }
    window._vfAllReviews=all;
    window._vfDecisions=decisions;
    window._vfReasons=reasons;
    window._vfNotes=notes;
    localStorage.setItem('vfDecisions',JSON.stringify(decisions));
  }
  async function probeReviewApi(){
    try{
      const response=await fetch('/api/health');
      window._reviewApi=!!(response.ok && (await response.json()).ok);
    }catch(e){ window._reviewApi=false; }
    updateVfMode();
    _vfToggleBanner();
    if(!window._reviewApi)return;
    vfLoadClarifications();
    checkVersion();
    checkReadiness();
    if(!window._vfVerPoll)window._vfVerPoll=setInterval(checkVersion,60000);
    if(window._vfReviewer===undefined)window._vfReviewer=localStorage.getItem('vfReviewer') || '';
    try{
      vfUseDecisions(await vfFetchDecisions());
      renderVfWorklist();
    }catch(e){
      vfNotice('Could not load saved reviews. Check the review server and reload to refresh your browser drafts.\n'+e.message,true);
    }
  }
  function updateVfMode(){ var ab=document.getElementById('vf-apply-btn'), db=document.getElementById('vf-download-btn'), h=document.getElementById('vf-mode-hint');
    if(window._reviewApi){ if(ab)ab.style.display='inline-block'; if(db)db.style.display='none'; if(h)h.innerHTML='Live review server connected — click ok/drop, then <b>Apply &amp; submit to main</b>: writes to the register, re-gates, and opens a PR including clarification replies. Required checks and approvals still apply.'; }
    else { if(ab)ab.style.display='none'; if(db)db.style.display='inline-block';
      // Offline branch was previously silent — the hint stayed blank on GitHub Pages, so a
      // reviewer had no idea why Apply was missing. Say what to run to get it back.
      if(h)h.innerHTML='<b style="color:var(--accent-amber);">Read-only</b> — decisions stay in this browser. Run the local review server (<code style="font-size:9.5px;">uv run python3 -m nbs_ruralscan.schema_tools.review_server</code>) to enable <b>Apply</b>, or use <b>Download CSV</b>.'; } }
  async function applyVfDecisions(){
    await (window._vfSaveQueue || Promise.resolve());
    if(!window._reviewApi){ vfNotice('Download your votes as CSV and submit it to RuralScan/evidence using the submission desk.'); return; }
    const btn=document.getElementById('vf-apply-btn');
    if(btn){btn.disabled=true; btn.textContent='Applying…';}
    const reviewer=window._vfReviewer || 'reviewer';
    const options={method:'POST', headers:{'Content-Type':'application/json'}};
    let summary='';
    try{
      const response=await fetch('/api/apply',{...options,body:JSON.stringify({reviewer})});
      const res=await response.json();
      if(!response.ok || res.error){
        vfNotice('Apply failed. If source files are missing, run uv run python scripts/hydrate-corpus.py (Windows: set NBS_LIBRARY_ROOT), then retry. Saved decisions remain local.\n'+(res.error || 'HTTP '+response.status),true);
        return;
      }
      const conflicts=res.conflicts || [];
      summary='Applied: '+(res.ok||0)+' ok, '+(res.dropped||0)+' dropped.'
        +(conflicts.length?'\n⚠ '+conflicts.length+' CONFLICT(s) pending — reviewers disagree: '+conflicts.map(c=>c.evidence_id).join(', '):' No conflicts.');
      let refreshFailed=false;
      try{
        vfUseDecisions(await vfFetchDecisions());
        const response=await fetch('data/bec50bc0f9dc/dashboard_data.json?t='+Date.now());
        if(!response.ok)throw Error('Dashboard data returned HTTP '+response.status);
        await setDashboardSnapshots(await response.json());
        renderVfWorklist();
        if(typeof triggerOverviewFilter==='function')triggerOverviewFilter();
        if(typeof renderDiscoveryAudit==='function')renderDiscoveryAudit();
      }catch(e){
        refreshFailed=true;
        summary+='\nThe review display could not refresh. Check the review server, then reload. '+e.message;
      }
      if(btn)btn.textContent='Submitting to main…';
      const title='qaqc: review '+new Date().toISOString().slice(0,10);
      const submitted=await fetch('/api/submit',{...options,body:JSON.stringify({reviewer,title})});
      const result=await submitted.json();
      if(!submitted.ok || !result.ok){
        vfNotice(summary+'\n\nSubmit failed. Retry submission after resolving the error.\n'+String(result.error || result.output || 'HTTP '+submitted.status).slice(-600),true);
        return;
      }
      vfLoadClarifications();
      vfNotice(summary+(result.pr_url?'\n\nSubmitted for main — '+result.pr_url+'\nSubject to checks and required approvals; clarification-history PRs require review.':'\n\nNo new agreed changes to submit. Saved decisions remain available.'),refreshFailed);
    }catch(e){
      vfNotice(summary?summary+'\n\nCould not confirm submission. Check the review server and submission status. '+e.message:'Could not confirm Apply. Check the review server and refresh. '+e.message,true);
    }finally{
      if(btn){btn.disabled=false;btn.textContent='Submit reviews';}
    }
  }
  function downloadVfDecisions(){ if(reviewData.registerRevision && !window._reviewApi){ReviewBatch.open();return;}
    var rows=window._vfFlagged||[]; var hdr=['evidence_id','source_id','variable','use_role','verdict','flag_reason','quote','relationship','decision','reason','reviewer','note'];
    function q(v){v=(v==null?'':String(v)); return '"'+v.replace(/"/g,'""')+'"';}
    var lines=[hdr.join(',')];
    rows.forEach(function(o){ var ev=o.ev; var rel=ev.relationship?(typeof ev.relationship==='string'?ev.relationship:JSON.stringify(ev.relationship)):'';
      lines.push([ev.evidence_id,ev.source_id,ev.variable,ev.use_role,o.verdict,o.reason,(ev.quote||'').replace(/\n/g,' '),rel,((window._vfDecisions||{})[ev.evidence_id]||''),((window._vfReasons||{})[ev.evidence_id]||''),'',((window._vfNotes||{})[ev.evidence_id]||'')].map(q).join(',')); });
    var blob=new Blob([lines.join('\n')],{type:'text/csv'}); var a=document.createElement('a'); a.href=URL.createObjectURL(blob); a.download='flag_worklist.csv'; a.click();
  }
  function syncVfReviewerPicker() {
    const picker = document.getElementById('vf-reviewer');
    const handle = window._vfReviewer || '';
    if (handle && !Array.from(picker.options).some(option => option.value === handle)) {
      picker.add(new Option(handle, handle), picker.querySelector('option[value="__other__"]'));
    }
    picker.value = handle;
  }

  function chooseVfReviewer(picker) {
    if (window._vfReviewer === undefined) window._vfReviewer = localStorage.getItem('vfReviewer') || '';
    let handle = picker.value;
    if (handle === '__other__') {
      handle = (prompt('Your GitHub handle') || '').trim();
      if (!handle || handle === '__other__') {
        syncVfReviewerPicker();
        return;
      }
      const known = Array.from(picker.options).find(option => option.value.toLowerCase() === handle.toLowerCase());
      if (known) handle = known.value;
    }
    if (handle === window._vfReviewer) {
      syncVfReviewerPicker();
      return;
    }
    setVfReviewer(handle);
  }

  function setVfReviewer(handle) {
    window._vfReviewer = handle;
    localStorage.setItem('vfReviewer', handle);
    syncVfReviewerPicker();
    vfUseDecisions(window._vfAllReviews || {});
    renderVfWorklist();
  }
  async function resetVfDecisions(){ if(reviewData.registerRevision && !window._reviewApi){ReviewBatch.open();return;} var me=(window._vfReviewer||'').trim(); if(!me){ alert('Set your reviewer handle first — reset only clears YOUR decisions.'); return; }
    // Reset = un-decide your PENDING (not-yet-applied) decisions only. Applied decisions are
    // the durable review record (register + review_log) and are never touched here — the old
    // version counted + cleared applied history too, so the dialog said "237" while Apply
    // said "24 pending" (confusing, 2026-09-18).
    var all=window._vfAllReviews||{}; var pend=[];
    Object.keys(all).forEach(function(eid){ var m=all[eid][me]; if(m&&m.decision&&m.applied!==true&&m.applied!=='true') pend.push(eid); });
    if(!window._reviewApi){ pend=Object.keys(window._vfDecisions||{}); } // offline: local decisions are all unapplied
    if(!pend.length){ alert('Nothing to reset — you have no pending (not-yet-applied) decisions.'); return; }
    if(!confirm('Reset your '+pend.length+' pending decision(s) back to to-review?\n\nPending = decided by you but not yet applied. Already-applied/committed decisions and other reviewers'+String.fromCharCode(39)+' work are untouched.'))return;
    if(window._reviewApi){
      try{
        const response=await fetch('/api/clear',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({reviewer:me})});
        const result=await response.json();
        if(!response.ok || !result || result.ok!==true || result.cleared_for!==me){
          throw Error((result && result.error) || 'The review server did not confirm this reset.');
        }
      }catch(e){
        vfNotice('Could not confirm the reset. Your browser drafts are still available. Check the review server and reload before retrying.\n'+e.message,true);
        return;
      }
    }
    const sameReviewer=(window._vfReviewer||'').trim()===me;
    for(const eid of pend){
      if(sameReviewer){
        if(window._vfDecisions)delete window._vfDecisions[eid];
        if(window._vfReasons)delete window._vfReasons[eid];
        if(window._vfNotes)delete window._vfNotes[eid];
      }
      if(all[eid]){
        delete all[eid][me];
        if(!Object.keys(all[eid]).length)delete all[eid];
      }
    }
    if(sameReviewer){
      localStorage.setItem('vfDecisions',JSON.stringify(window._vfDecisions||{}));
      localStorage.setItem('vfReasons',JSON.stringify(window._vfReasons||{}));
      localStorage.setItem('vfNotes',JSON.stringify(window._vfNotes||{}));
    }
    renderVfWorklist();
  }
  function renderQaqcStats(hostEl){
    var s=(reviewData&&reviewData.qaqc_stats)||{};
    var fe=s.flag_eval||{}, pe=s.pass_eval||{};
    var live=0; var allr=window._vfAllReviews||{}; Object.keys(allr).forEach(function(eid){ Object.keys(allr[eid]).forEach(function(rv){ if(allr[eid][rv].decision)live++; }); });
    function pct(v){ return (v===null||v===undefined)?'<span style="color:var(--text-muted);">n/a</span>':('<b>'+v+'%</b>'); }
    function cell(n,lbl,col){ return '<td style="padding:10px 14px; text-align:center; border:1px solid var(--border-color);"><div style="font-size:20px; font-weight:700; color:'+col+';">'+n+'</div><div style="font-size:10px; color:var(--text-muted);">'+lbl+'</div></td>'; }
    var matrix='<div style="margin:8px 0; font-size:11px;">'
      +'<div style="font-size:10.5px; color:var(--accent-amber); font-weight:700; text-transform:uppercase; letter-spacing:.03em; margin-bottom:4px;">When the AI flagged ('+(fe.n||0)+')</div>'
      +'<table style="border-collapse:collapse;"><tr>'+cell((fe.tp_removed||0),'caught → removed','var(--accent-emerald)')+cell((fe.tp_corrected||0),'caught → corrected (kept)','var(--accent-emerald)')+cell(fe.fp||0,'false alarm (kept)','var(--accent-rose)')+'</tr></table>'
      +'<div style="font-size:10px; color:var(--text-muted); margin:2px 0 10px;">first two = real catches (TP) · false alarm = AI was wrong (FP)</div>'
      +'<div style="font-size:10.5px; color:var(--accent-sky); font-weight:700; text-transform:uppercase; letter-spacing:.03em; margin-bottom:4px;">When the AI passed &amp; a human spot-checked ('+(pe.checked||0)+')</div>'
      +'<table style="border-collapse:collapse;"><tr>'+cell(pe.tn||0,'confirmed good (TN)','var(--accent-emerald)')+cell(pe.fn||0,'missed number/rel. error (FN)','var(--accent-rose)')+cell(pe.out_of_remit||0,'scope/quality drop (outside verify remit)','var(--accent-amber)')+'</tr></table>'
      +'<div style="font-size:10px; color:var(--text-muted); margin-top:2px;">'+((pe.checked||0)===0?'no passes spot-checked yet → miss rate unknown':'FN = verify pass let a <b>number/relationship</b> error through (its job) · the amber column is <b>scope/quality</b> (off-scope, wrong-practice, …) — a different failure caught by check_scope/check_quote, NOT the verify pass')+'</div>'
      +'</div>';
    function kv(k,v){ return '<div style="display:flex; justify-content:space-between; gap:18px; padding:3px 0; border-bottom:1px solid rgba(255,255,255,0.04);"><span style="color:var(--text-secondary);">'+k+'</span><span style="color:var(--text-primary); font-weight:600;">'+v+'</span></div>'; }
    function tally(obj){ obj=obj||{}; var ks=Object.keys(obj); if(!ks.length)return '<span style="color:var(--text-muted);">none yet</span>'; return ks.map(function(k){return '<div style="display:flex; justify-content:space-between; gap:14px; padding:2px 0;"><span style="color:var(--text-secondary);">'+k.replace(/_/g,' ')+'</span><span style="font-weight:600;">'+obj[k]+'</span></div>';}).join(''); }
    var h='<div style="font-size:11px; color:var(--text-muted); margin-bottom:12px;">Measured from <code>pipeline/metrics/review_log.csv</code> (applied/logged decisions only). The AI is <b>not</b> assumed correct — these numbers show how often its verify-flags were right and how many errors it let through.</div>'
      +'<div style="display:flex; gap:24px; flex-wrap:wrap;">'
      +'<div style="flex:1; min-width:340px;"><h3 style="font-size:12px; color:var(--text-secondary); margin:0 0 6px;">AI verify-flag confusion matrix</h3>'+matrix
      +'<div style="margin-top:10px;">'+kv('Flag precision (of flags, % real)',pct(fe.precision_pct)+' <span style="color:var(--text-muted); font-size:10px;">('+(fe.tp||0)+'/'+(fe.n||0)+')</span>')
      +kv('Recall — estimate only',pct(s.recall_est_pct)+' <span style="color:var(--text-muted); font-size:10px;">(FN from sampled passes)</span>')
      +kv('Pass FN-rate (number/rel. only)',pct(pe.fn_rate_pct)+' <span style="color:var(--text-muted); font-size:10px;">('+(pe.fn||0)+'/'+((pe.tn||0)+(pe.fn||0))+')</span>')
      +kv('Errors caught by AI',(s.errors_caught||0))
      +kv('Verify-remit errors AI missed (sample)',(s.errors_missed_in_sample||0))
      +kv('Scope/quality drops (outside verify remit)',(pe.out_of_remit||0))
      +kv('⚑ Queried (tentative + open question)',(s.queried||0))+'</div>'
      +'<div style="font-size:10px; color:var(--text-muted); margin-top:8px; line-height:1.5;">Recall/FN are <b>estimates</b>: false negatives only surface where someone spot-checked an AI-passed unit. Sample more passes to tighten them.</div></div>'
      +'<div style="flex:1; min-width:260px;"><h3 style="font-size:12px; color:var(--text-secondary); margin:0 0 6px;">Review effort</h3>'
      +kv('Distinct reviews',(s.total_reviews||0))+kv('⚑ Queried (tentative + open question)',(s.queried||0))+kv('Reviewers',(s.n_reviewers||0))+kv('Decisions in browser (not yet applied)',live)
      +'<h4 style="font-size:11px; color:var(--text-muted); margin:12px 0 4px;">By reviewer</h4>'+tally(s.by_reviewer)
      +'<h4 style="font-size:11px; color:var(--text-muted); margin:12px 0 4px;">By reason code</h4>'+tally(s.by_reason)
      +'<h4 style="font-size:11px; color:var(--text-muted); margin:12px 0 4px;">By decision</h4>'+tally(s.by_decision)+'</div></div>';
    hostEl.innerHTML=h;
  }

  function vfNotice(message, error){
    var el=document.getElementById('vf-action-status');
    if(!el){el=document.createElement('div');el.id='vf-action-status';el.setAttribute('role','status');var anchor=document.getElementById('vf-pending-count');if(anchor)anchor.parentNode.insertBefore(el,anchor);}
    el.style.cssText='padding:8px;margin:6px 0;white-space:pre-wrap;color:var('+(error?'--accent-rose':'--accent-sky')+')';el.textContent=message;
  }
  async function vfRefreshReview(){
    const [all, response]=await Promise.all([vfFetchDecisions(),fetch('data/bec50bc0f9dc/dashboard_data.json?t='+Date.now())]);
    if(!response.ok)throw Error('Could not refresh dashboard data');
    await setDashboardSnapshots(await response.json());
    vfUseDecisions(all);
    if(window._reviewApi)await vfLoadClarifications();
    renderVfWorklist();
  }
  async function reopenVf(eid){
    if(!window._reviewApi){vfNotice('Reopen needs the live review server.',true);return;}
    vfNotice('Reopening record and rebuilding review data…');
    try{
      var r=await fetch('/api/reopen',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({evidence_ids:[eid],reviewer:window._vfReviewer||'reviewer'})});var res=await r.json();if(!r.ok||res.error)throw Error(res.error||'Reopen failed');
      vfWriteFilters(vfShortcutFilters('todo'));
      await vfRefreshReview();vfNotice('Record reopened. Previous call cleared; ready for a new decision.');
      var card=document.querySelector('details[data-vfeid="'+eid+'"]');if(card){card.open=true;card.scrollIntoView({block:'center'});}
    }catch(e){vfNotice('Reopen failed: '+e.message,true);}
  }
  async function challengeVf(eid, dec){
    var rev=(window._vfReviewer||'').trim();if(!rev){vfNotice('Select your reviewer handle first.',true);return;}
    vfNotice('Saving revised decision…');
    try{var r=await fetch('/api/challenge',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({evidence_id:eid,decision:dec,reviewer:rev,reviewed_conflict:vfReviewingConflict(eid),reason:((window._vfReasons||{})[eid]||''),note:((window._vfNotes||{})[eid]||'')})});var res=await r.json();if(!r.ok||res.error)throw Error(res.error||'Save failed');await vfRefreshReview();vfNotice(res.conflict?'Decision saved; disagreement remains for resolution.':'Decision saved locally. Apply & submit when finished.');}
    catch(e){vfNotice('Decision not saved: '+e.message,true);}
  }

  // Units resolved by < 2 reviewers (need a 2nd opinion). If a reviewer handle is set,
  // exclude units that reviewer already reviewed (it's not THEIR 2nd opinion to give).
  // All reviews for one unit, MERGING committed review_log (other reviewers, from the register)
  // with the local decisions.json store (_vfAllReviews). decisions.json is per-machine, so on
  // its own it misses other people's committed reviews — the review_log fills that gap.
  function vfReviewCredits(name) {
    // CIAT review exports used all four spellings for the same account.
    const aliases = {'pete':'peetmate', 'peter':'peetmate', 'pete steward':'peetmate', 'peetmate':'peetmate', 'namita-j':'Namita-J'};
    return [...new Set(String(name || '?').split(',').map(s => s.trim()).filter(Boolean)
      .map(s => Object.hasOwn(aliases, s.toLowerCase()) ? aliases[s.toLowerCase()] : s))];
  }
  const vfEventCache = new WeakMap();
  function vfPersonalHistory() {
    const scope = window._vfScope || {};
    const who = window._vfReviewer;
    const query = (window._vfSearch || '').trim().toLowerCase();
    const inScope = row => who && row.table === scope.table &&
      (scope.nbs === 'all' || row.nbs_id === scope.nbs) && vfReviewCredits(row.reviewer).includes(who);
    const matchesSearch = row => [row.evidence_id, row.source_id, row.record_id, row.note, row.decision, row.date]
      .join(' ').toLowerCase().includes(query);
    const decisions = new Map();
    for (const row of reviewData.deferred_reviews || []) {
      if (!inScope(row)) continue;
      if (row.decision === 'reopen') decisions.delete(row.evidence_id);
      else decisions.set(row.evidence_id, row);
    }
    return {
      archived: [...decisions.values()].filter(matchesSearch),
      ratings: (reviewData.row_reviews || []).filter(row => inScope(row) && matchesSearch(row))
    };
  }
  function vfArchivedHistory(rows) {
    if (!rows.length) return '';
    const source = 'https://github.com/CIAT/nbs_ruralscan/blob/' + reviewData.revision + '/' + reviewData.deferred_register;
    return '<details id="vf-archived-history"><summary>Your archived ' + vfEsc(rows[0].table) + ' finding reviews (' +
      rows.length + ')</summary><p>CIAT archived these findings in September, before the current rating method.</p><ul>' +
      rows.map(r => '<li><code>' + vfEsc(r.evidence_id) + '</code> · ' + vfEsc(r.date) + ' · ' +
        vfEsc(r.decision === 'flag' ? 'query' : r.decision) + (r.note ? '<br>' + vfEsc(r.note) : '') + '</li>').join('') +
      '</ul><a href="' + source + '">Open the archived CIAT evidence register</a></details>';
  }
  function vfRatingHistory(rows) {
    if (!rows.length) return '';
    const source = 'https://github.com/RuralScan/evidence/blob/' + reviewData.registerRevision + '/registers/pipeline/metrics/row_review_log.csv';
    return '<details id="vf-rating-history"><summary>Your ' + vfEsc(rows[0].table) + ' rating reviews (' + rows.length +
      ')</summary><p>These decisions apply to compiled ratings.</p><ul>' +
      rows.map(r => '<li>' + vfEsc(r.record_id.replace(/__/g, ' · ').replace(/_/g, ' ')) + ' — ' +
        vfEsc(r.decision) + ' · ' + vfEsc(r.date.slice(0,10)) + (r.note ? '<br>' + vfEsc(r.note) : '') + '</li>').join('') +
      '</ul><a href="' + source + '">View RuralScan rating review log</a></details>';
  }
  function vfReviewerEvents() {
    const log = reviewData.review_log || [];
    if (!vfEventCache.has(log)) {
      vfEventCache.set(log, log.flatMap(row => vfReviewCredits(row.reviewer)
        .map(reviewer => ({...row, reviewer}))));
    }
    return vfEventCache.get(log);
  }
  function _vfMergedReviews(eid){ var out={};
    var rl=vfReviewerEvents();
    rl.forEach(function(r){ if(r.evidence_id!==eid)return; var d=(r.decision||'').toLowerCase(); if(d==='reopen')delete out[r.reviewer]; else if(d)out[r.reviewer]=d; });
    if(reviewData.registerRevision && !window._reviewApi) { var draft=ReviewBatch.get(eid); if(draft)out[draft.reviewer]=VoteDrafts.legacyDecision(draft.decision); return out; }
    var a=(window._vfAllReviews||{})[eid]||{};
    Object.keys(a).forEach(function(rv){ if(a[rv]&&a[rv].decision) out[rv]=a[rv].decision; });  // local pending/applied overrides
    return out; }
  // Module-level SCOPE predicate — the single source of truth for "is this row in the current
  // scope" (Practice · Sub-practice · Evidence-type · Source channel · Access · source/section
  // subset). Used by EVERY queue count so they all filter to the same scope + reconcile.
  // Combined review queue only: operational evidence keeps its M2b analytical role.
  // Including it here does not add it to the core suitability score.
  var _vfR2T={structural_suitability:'T4',operational_risk:'T4',nbs_effect:'T3/T6',asset_vulnerability:'T3/T6'};
  // Reconcile stored approval with current reviewer decisions; never infer approval.
  function vfLoadClarifications(){
    if(!window._reviewApi)return Promise.resolve();
    return fetch('/api/clarifications').then(function(r){if(!r.ok)throw Error('Could not load clarification history');return r.json();}).then(function(data){
      window._vfClarifications=data.issues||[];window._vfClarificationPending=data.pending||0;window._vfClarificationError='';
      renderVfWorklist();
    }).catch(function(e){window._vfClarificationError=e.message;renderVfWorklist();});
  }
  function vfClarificationQueue(status){
    vfShortcut(status==='needs_investigation'?'waiting':'answers'); // Legacy links retain their follow-up filter.
  }
  function vfClarificationsFor(eid){return (window._vfClarifications||[]).filter(function(g){return g.records.some(function(r){return r.evidence_id===eid;});});}
  function vfClarificationHtml(ev){
    return vfClarificationsFor(ev.evidence_id).map(function(g){
      var record=g.records.find(function(r){return r.evidence_id===ev.evidence_id;});
      var state=record.review_status||g.status;
      var answer=g.answers.filter(function(a){return !a.evidence_id||a.evidence_id===ev.evidence_id;});
      var body='<p><b>Your question — '+vfEsc(g.reviewer)+'</b><br>'+vfEsc(g.question)+'</p>'
        +answer.map(function(a){return '<p><b>Answer / what changed</b><br>'+vfEsc(a.response)+'</p>';}).join('')
        +(!answer.length?'<p>Answer still being investigated.</p>':'')
        +'<details><summary>Discussion history and linked records</summary>'+g.records.map(function(r){return '<p>'+vfEsc(r.evidence_id)+' · '+vfEsc(r.variable)+'</p>';}).join('')
        +g.history.map(function(h){return '<p>'+vfEsc(h.reviewer)+' · '+vfEsc(h.action)+' · '+vfEsc(h.date)+'<br>'+vfEsc(h.note)+'</p>';}).join('')+'</details>';
      if(state==='resolved')return '<details style="margin:12px 0"><summary>Previous question and answer</summary>'+body+'</details>';
      return '<section style="border-left:3px solid var(--accent-sky);padding:8px 12px;margin:12px 0;font-size:12px">'+body
        +'<p><b>Review this record below:</b> Keep if correct, Drop if unsuitable, or write a remaining question and choose Query.</p></section>';
    }).join('');
  }
  function vfHasAnswerForReview(eid){
    return vfClarificationsFor(eid).some(function(g){
      var r=g.records.find(function(r){return r.evidence_id===eid;});
      var status=r.review_status||g.status;
      return status==='answer_ready'||status==='needs_judgement';
    });
  }
  async function vfClarificationRespond(id,action,field){
    var g=(window._vfClarifications||[]).find(function(x){return x.id===id;});var reviewer=(window._vfReviewer||'').trim();
    if(!reviewer){vfNotice('Select your dashboard reviewer handle first.',true);return;}
    if(window._vfClarificationBusy)return;
    window._vfClarificationBusy=true;
    var input=document.getElementById(field);var note=input?input.value:'';
    vfNotice(action==='accept'?'Saving accepted answer…':'Saving follow-up…');
    try{var r=await fetch('/api/clarifications',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({issue_id:id,fingerprint:g.fingerprint,action:action,reviewer:reviewer,note:note})});var result=await r.json();if(!r.ok)throw Error(result.error);await vfLoadClarifications();vfNotice(action==='accept'?'Answer accepted and saved. Next answer below. Extraction approval unchanged.':'Follow-up saved; moved to team investigation.');}
    catch(e){vfNotice('Response NOT saved: '+e.message,true);}
    finally{window._vfClarificationBusy=false;}
  }
  function _vfReviewBucket(ev, decisions){
    if(ev.review_state==='dropped')return 'dropped';
    var ds=Object.values(decisions||{}).filter(Boolean).map(function(d){d=String(d).toLowerCase(); return d==='keep'?'ok':d;});
    var approved=String(ev.reviewer_ok).toLowerCase()==='true';
    if(ds.some(function(d){return d!=='ok';}))return 'unresolved';
    if(ds.length)return approved?'recorded':'unresolved';
    return approved?'approval_only':'first';
  }
  // Shortcuts and sidebar controls share these axes. There is no queue mode
  // that bypasses them; candidate counts use this same state and predicate.
  function vfFilterState(overrides){
    return Object.assign({status:window._vfAxStatus||'active',origin:window._vfAxOrigin||'any',
      me:window._vfAxMe||'no',other:window._vfAxOther||'any',call:window._vfMyCall||'all',
      followup:window._vfFollowUp||'all',verdict:window._vfVerdictFilter||'all',tables:!!window._vfTablesOnly,
      round:(window._vfScope||{}).round||'all'},overrides||{});
  }
  function vfShortcutFilters(key){
    var f={status:'active',origin:'any',me:'any',other:'any',call:'all',followup:'all',verdict:'all',tables:false};
    if(['todo','flagged','passed','second'].includes(key))f.me='no';
    if(key==='flagged'||key==='passed')f.origin=key;
    if(key==='second')f.other='yes';
    if(['kept','queried','dropped','mine'].includes(key))f.me='yes';
    if(key==='kept')f.call='ok';
    if(key==='queried')f.call='query';
    if(key==='dropped'){f.call='drop';f.status='any';}
    if(key==='mine'||key==='all')f.status='any';
    if(['answers','waiting','conflict','requested','unresolved','approval_only'].includes(key))f.followup=key;
    if(key==='requested')f.status='any';
    if(key==='history')f.status='dropped';
    return f;
  }
  function vfShortcutSelected(key){
    var f=vfFilterState(),preset=vfShortcutFilters(key);
    return Object.keys(preset).every(function(k){return f[k]===preset[k];});
  }
  function vfWriteFilters(f){
    var fields={status:'_vfAxStatus',origin:'_vfAxOrigin',me:'_vfAxMe',other:'_vfAxOther',
      call:'_vfMyCall',followup:'_vfFollowUp',verdict:'_vfVerdictFilter',tables:'_vfTablesOnly'};
    Object.keys(fields).forEach(function(k){if(Object.hasOwn(f,k))window[fields[k]]=f[k];});
    window._vfMode='review';
  }
  function vfShortcut(key){
    if(window.DashboardPriority)DashboardPriority.leaveFocus();
    vfWriteFilters(vfShortcutFilters(key));
    renderVfWorklist();
  }
  function vfSetFilter(key,value){
    if(window.DashboardPriority)DashboardPriority.leaveFocus();
    vfWriteFilters({[key]:value});
    renderVfWorklist();
  }
  function vfReviewQueue(key){
    vfShortcut(key==='dropped'?'history':key);
  }
  function vfSimpleQueue(view){
    // Compatibility for existing queue and finding links; no separate filter mode.
    vfWriteFilters(vfShortcutFilters(view==='advanced'?'all':view));
    renderVfWorklist();
  }
  function vfSearch(value){
    if(window.DashboardPriority)DashboardPriority.leaveFocus();window._vfSearch=value;var input=document.getElementById('vf-search');var position=input&&input.selectionStart;
    renderVfWorklist();input=document.getElementById('vf-search');if(input){input.focus();if(position!==null&&position!==undefined)input.setSelectionRange(position,position);}
  }
  function vfRepeatedConflicts(log,reviewer){
    var calls={},done={};
    log.forEach(function(r){
      var id=r.evidence_id,who=r.reviewer,d=(r.decision||'').toLowerCase();
      if(d==='keep')d='ok';
      var prev=calls[id]||(calls[id]={});
      if(d==='reopen'){delete prev[who];if(who===reviewer)delete done[id];return;}
      if(who===reviewer&&(d==='ok'||d==='drop')&&(prev[who]==='ok'||prev[who]==='drop')
        &&Object.keys(prev).some(function(other){return other!==who&&((prev[other]==='ok'&&prev[who]==='drop')||(prev[other]==='drop'&&prev[who]==='ok'));}))done[id]=true;
      if(d)prev[who]=d;
    });
    return done;
  }
  function vfFollowUpMatch(u,key){
    if(key==='all')return true;
    var answered=vfHasAnswerForReview(u.ev.evidence_id);
    if(key==='answers')return answered&&!(u.me&&!u.meApplied);
    if(key==='conflict')return !!u.ev._reviewConflict;
    if(key==='requested')return !!window.DashboardPriority?.needsAttention(u.ev)&&!(u.me&&!u.meApplied);
    if(key==='unresolved'||key==='approval_only')return u.ev._reviewQueue===key;
    if(key==='waiting'){
      var query=u.myDec==='flag'||u.myDec==='query';
      var waiting=vfClarificationsFor(u.ev.evidence_id).some(function(g){
        var r=g.records.find(function(r){return r.evidence_id===u.ev.evidence_id;});
        return g.reviewer!=='Status reconciliation'&&(r.review_status||g.status)==='needs_investigation';
      });
      return !(u.me&&!u.meApplied)&&(query||waiting)&&!answered&&!u.ev._reviewConflict;
    }
    return false;
  }
  function vfMatchesFilters(u, overrides){
    var f=vfFilterState(overrides);
    if(u.formerlyCited&&f.status==='active'&&f.followup!=='requested')return false;
    if(window.DashboardPriority&&!DashboardPriority.matches(u.ev,f.ignoreFocus))return false;
    if(f.round!=='all'&&_vfRoundKey(u.ev)!==f.round)return false;
    var search=(window._vfSearch||'').trim().toLowerCase();
    if(search&&![u.ev.source_id,u.ev.variable,u.ev.quote,u.ev.evidence_id].join(' ').toLowerCase().includes(search))return false;
    if(f.status==='active'&&u.dropped||f.status==='dropped'&&!u.dropped)return false;
    if(f.origin!=='any'&&u.origin!==f.origin)return false;
    if(f.me!=='any'&&u.me!==(f.me==='yes'))return false;
    if(f.other!=='any'&&u.other!==(f.other==='yes'))return false;
    if(f.me==='yes'&&f.call!=='all'){
      var call=u.myDec==='flag'?'query':u.myDec==='keep'?'ok':u.myDec;
      if(call!==f.call)return false;
    }
    if(!vfFollowUpMatch(u,f.followup))return false;
    if(f.verdict==='conflict'){if(!u.ev._reviewConflict)return false;}
    else if(f.verdict!=='all'&&(u.origin!=='flagged'||u.verdict!==f.verdict))return false;
    if(f.tables&&!_vfTabular(u.ev.quote))return false;
    return true;
  }
  function vfShowPersonalHistory(overrides){
    var f=vfFilterState(overrides),sc=window._vfScope||{},preset=vfShortcutFilters('mine');
    // Archived findings and rating events lack current EV filter fields. Show them
    // separately only in the unrefined personal-history view, never inflate filtered counts.
    return Object.keys(preset).every(function(k){return f[k]===preset[k];})&&f.round==='all'
      &&['family','source','access','claimScope'].every(function(k){return !sc[k]||sc[k]==='all'||k==='claimScope'&&sc[k]==='general';})
      &&!sc.sourceId&&!sc.section&&sc.observations!=='only'&&(!window._vfPriorityEvidence||f.ignoreFocus)
      &&(!window._vfPriority||window._vfPriority==='all');
  }
  // Site descriptions do not define suitability rules. Do not confuse these
  // with observational studies that estimate an effect or adoption relationship.
  function vfIsSiteObservation(ev){
    if(ev.use_role!=='structural_suitability')return false;
    var r=ev.relationship||{};
    if(typeof r==='string'){try{r=JSON.parse(r);}catch(e){return false;}}
    if(!r||typeof r!=='object')return false;
    if(r.type==='observed_presence'||r.type==='site_context')return true;
    if(r.type||r.shape||r.metric)return false;
    return r.note==='case_study_site_context'||r.direction==='observed_existing_tree_stock_where_FMNR_occurs'
      ||Object.keys(r).some(function(k){return k.indexOf('observed_')===0;});
  }
  function _vfInScope(ev,ignoreRound){ var sc=window._vfScope||{};
    var observations=sc.observations||'hide';var site=vfIsSiteObservation(ev);
    if(observations==='hide'&&site)return false;
    if(observations==='only'&&!site)return false;
    if(!sc.nbs)return true;
    if(sc.nbs!=='all'&&ev.nbs_id!==sc.nbs)return false;
    if(!DashboardTables.matches(ev, sc.table, true))return false;
    if(sc.family&&sc.family!=='all'&&ev.suitability_family_id!==sc.family)return false;
    if(sc.source&&sc.source!=='all'&&_vfChanKey(ev)!==sc.source)return false;
    if(!ignoreRound&&sc.round&&sc.round!=='all'&&_vfRoundKey(ev)!==sc.round)return false;
    if(sc.sourceId&&ev.source_id!==sc.sourceId)return false;
    if(sc.section&&String(ev.page||'')!==String(sc.section))return false;
    if(sc.access&&sc.access!=='all'){ var _oa=_vfIsOA(ev); if(sc.access==='oa'&&!_oa)return false; if(sc.access==='restricted'&&_oa)return false; }
    // claim_scope lane (2026-07): general = practice-level suitability (the everyday MCDA work);
    // species/crop = per-taxon evidence, KEPT + banked for reuse but filtered from practice MCDA.
    // Default 'general' hides the species/crop lane so it doesn't clutter suitability review.
    if(sc.claimScope&&sc.claimScope!=='all'){ var _cs=(ev.claim_scope||'practice_technology');
      if(sc.claimScope==='general'&&_cs!=='practice_technology')return false;
      if(sc.claimScope==='species'&&_cs!=='species_specific')return false;
      if(sc.claimScope==='crop'&&_cs!=='crop_specific')return false; }
    return true; }
  // Gap rows carry nbs_id / suitability_family_id / table directly (no use_role).
  function _vfGapInScope(g){ var sc=window._vfScope||{}; if(!sc.nbs)return true;
    if(sc.nbs!=='all'&&(g.nbs_id||'')!==sc.nbs)return false;
    if(sc.table&&sc.table!=='all'&&(g.table||'')!==sc.table)return false;
    if(sc.family&&sc.family!=='all'&&(g.suitability_family_id||'')!==sc.family)return false;
    return true; }
  function _vf2ndList(){
    var me=(window._vfReviewer||'').trim();
    var evAll=(reviewData.registers.EV_evidence_register)||[];
    var dropped=(reviewData._evDropped)||[];
    var rl=vfReviewerEvents();
    var revBy={}, prior={};
    rl.forEach(function(r){ var d=(r.decision||'').toLowerCase(); if(d==='ok'||d==='drop'){ (revBy[r.evidence_id]=revBy[r.evidence_id]||{})[r.reviewer||'?']=true; prior[r.evidence_id]=r; } });
    var resolved=evAll.filter(function(e){return e.reviewer_ok===true||e.reviewer_ok==='true';}).concat(dropped);
    var byId={}; evAll.concat(dropped).forEach(function(e){ byId[e.evidence_id]=e; });
    var store=(window._vfAllReviews||{});
    return resolved.filter(function(e){ var id=e.evidence_id;
      if(!_vfInScope(e)) return false;                           // 2nd-opinion respects the scope too
      var nrev=Object.keys(revBy[id]||{}).length;
      if(nrev<1) return false;                                   // nobody has reviewed it → not a 2nd-opinion candidate
      if(nrev>=2) return false;                                  // already has a 2nd opinion
      if(me){ var meRl=revBy[id]&&revBy[id][me]; var meSt=store[id]&&store[id][me]&&store[id][me].decision; if(meRl||meSt) return false; }
      return true;                                               // reviewed by exactly one OTHER person, not me
    }).map(function(e){ return {ev:e, prior:prior[e.evidence_id]||{}, dropped:((e.review_state||'')==='dropped')}; });
  }

  function renderVf2ndOpinion(host){
    var me=(window._vfReviewer||'').trim();
    var list=_vf2ndList();
    var dc=document.getElementById('vf-decided-count'); if(dc) dc.innerHTML='<b>'+list.length+'</b> unit(s) already reviewed by someone else'+(me?(' (not by '+vfEsc(me)+')'):'')+' <span style="color:var(--text-muted);">— give your independent 2nd opinion (ok / drop / query). Agreeing records consensus; disagreeing raises a conflict on Apply.'+(me?'':' Set your handle first.')+'</span>';
    host.innerHTML='';
    if(!list.length){ host.innerHTML='<div style="color:var(--text-muted); padding:14px;">'+(me?'Nothing awaiting your 2nd opinion.':'Set your reviewer handle to see units awaiting your 2nd opinion.')+'</div>'; return; }
    // Render the SAME full card as direct review (vfDetailHtml) — it already carries the existing
    // review(s) in its "Reviews:" line (supports multiple reviewers per unit). The normal
    // ok/drop/query buttons feed consensus on Apply (agree → consensus, disagree → conflict).
    list.forEach(function(o){ var ev=o.ev;
      var attr=ev.attribution||''; var idx=attr.indexOf('[VERIFY-FLAG ');
      var passed=(idx===-1); var verdict='pass', reason='AI accepted this extraction — spot-check: is the encoded value faithful to the quote?';
      if(!passed){ var raw=attr.slice(idx+13); var close=raw.indexOf(']'); var body=close!==-1?raw.slice(0,close):raw; var ci=body.indexOf(': '); verdict=(ci!==-1?body.slice(0,ci):body).trim().toLowerCase(); reason=ci!==-1?body.slice(ci+2).trim():''; }
      host.insertAdjacentHTML('beforeend', vfDetailHtml({ev:ev, verdict:verdict, reason:reason}, passed));
    });
  }

  function renderVfReviewed(host, rlAll, bucket){ rlAll=rlAll||[]; bucket=bucket||'kept';
    var me=(window._vfReviewer||'').trim();
    var rows=rlAll.slice().reverse();
    var touchedByMe={}; if(me) rlAll.forEach(function(r){ if((r.reviewer||'')===me) touchedByMe[r.evidence_id]=true; });
    var _myDecR={}; if(me) rlAll.forEach(function(r){ if((r.reviewer||'')===me && (r.decision||'')) _myDecR[r.evidence_id]=(r.decision||'').toLowerCase(); });
    var evAll=(reviewData.registers.EV_evidence_register)||[]; var present={};
    evAll.forEach(function(e){ present[e.evidence_id]=(e.reviewer_ok===true||e.reviewer_ok==='true'); });
    var dropped={}; ((reviewData._evDropped)||[]).forEach(function(e){ dropped[e.evidence_id]=true; });
    var _byId2={}; evAll.concat((reviewData._evDropped)||[]).forEach(function(e){ _byId2[e.evidence_id]=e; });
    // origin (AI-flagged vs AI-passed) from the EV attribution (active or quarantined row).
    var _flaggedMap={}; Object.keys(_byId2).forEach(function(id){ _flaggedMap[id]=/\[VERIFY-FLAG/.test((_byId2[id].attribution)||''); });
    var _origin=function(id){ return _flaggedMap[id]?'flagged':'passed'; };
    // one card per unit (latest action) — touched by me, IN the current scope, and in the
    // active/dropped bucket for this mode (My reviewed = kept/active; Dropped = quarantined).
    var seen={}, units=[];
    rows.forEach(function(r){ var id=r.evidence_id; if(me && !touchedByMe[id]) return; if(seen[id]) return; var e=_byId2[id]; if(!e||!_vfInScope(e)) return;
      var isDrop=!!dropped[id];
      if(bucket==='dropped'){ if(!isDrop) return; }
      else { if(isDrop) return; var _d=_myDecR[id]||''; var _isQ=(_d==='query'||_d==='flag'); if(bucket==='queried'){ if(!_isQ) return; } else { if(_isQ) return; } }
      seen[id]=1; units.push(r); });
    if(!window._vfReviewedFilter)window._vfReviewedFilter='all';
    var _rf=window._vfReviewedFilter;
    var _nFlag=units.filter(function(r){return _origin(r.evidence_id)==='flagged';}).length, _nPass=units.length-_nFlag;
    var shown=units.filter(function(r){ return _rf==='all'||_origin(r.evidence_id)===_rf; });
    var dc=document.getElementById('vf-decided-count'); if(dc) dc.innerHTML= (bucket==='dropped')
      ? ('<b>'+units.length+'</b> dropped (quarantined) record(s) '+(me?('by '+vfEsc(me)+' '):'')+'in scope — <span style="color:var(--text-muted);">removed from the analysis but kept &amp; reversible. Re-open any to send it back to the queue.</span>')
      : (bucket==='queried')
      ? ('<b>'+units.length+'</b> queried record(s) '+(me?('by '+vfEsc(me)+' '):'')+'in scope — <span style="color:var(--text-muted);">kept tentatively with an open question; awaiting follow-up / resolution. Write the question in the note; re-open to change the call.</span>')
      : ('<b>'+units.length+'</b> reviewed &amp; kept (ok) record(s) '+(me?('by '+vfEsc(me)+' '):'')+'in scope = <b style="color:var(--accent-rose);">'+_nFlag+'</b> AI-flagged + <b style="color:var(--accent-emerald);">'+_nPass+'</b> AI-passed. <span style="color:var(--text-muted);">Challenge any with ok/drop to raise a conflict; queried + dropped ones have their own queues.</span>');
    host.innerHTML='';
    if(!units.length){ host.innerHTML='<div style="color:var(--text-muted); padding:14px;">No applied reviews yet'+(me?(' by '+vfEsc(me)):'')+'. Decisions appear here once you <b>Apply</b> them.</div>'; return; }
    // filter: was the reviewed unit originally AI-flagged or AI-passed
    var _fp=function(k,lab,n){ var a=_rf===k?'active sky':''; return '<button class="pill-btn '+a+'" onclick="window._vfReviewedFilter=\''+k+'\'; renderVfWorklist();" style="font-size:11px; padding:3px 10px; border-radius:4px;">'+lab+' ('+n+')</button>'; };
    host.insertAdjacentHTML('beforeend','<div style="display:flex; gap:6px; margin-bottom:10px; flex-wrap:wrap; align-items:center;"><span style="font-size:9px; color:var(--text-muted); text-transform:uppercase; letter-spacing:.06em; font-weight:700; margin-right:2px;">Origin</span>'+_fp('all','All',units.length)+_fp('flagged','⚑ AI-flagged',_nFlag)+_fp('passed','✓ AI-passed',_nPass)+'</div>');
    if(!shown.length){ host.insertAdjacentHTML('beforeend','<div style="color:var(--text-muted); padding:8px;">None in this origin filter.</div>'); return; }
    shown.forEach(function(r){
      var id=r.evidence_id;
      var dec=(r.decision||'').toLowerCase();
      var col=dec==='ok'?'var(--accent-emerald)':dec==='drop'?'var(--accent-rose)':'var(--accent-amber)';
      var _org=_origin(id); var _orgCol=_org==='flagged'?'var(--accent-rose)':'var(--accent-emerald)';
      var _orgBadge='<span title="'+(_org==='flagged'?'AI flagged this extraction originally':'AI accepted this extraction originally')+'" style="font-size:9px; font-weight:700; text-transform:uppercase; letter-spacing:.03em; padding:1px 6px; border-radius:3px; border:1px solid '+_orgCol+'; color:'+_orgCol+';">'+(_org==='flagged'?'⚑ AI-flagged':'✓ AI-passed')+'</span>';
      // all reviewers' current decisions for this unit (from the persistent store)
      var allr=_vfMergedReviews(id); var rk=Object.keys(allr);
      var conf=(new Set(rk.map(function(k){return allr[k];}))).size>1;
      var reviewsLine=rk.length?('<div style="font-size:10.5px; margin-top:5px;">'+(conf?'<span style="color:var(--accent-rose); font-weight:700;">⚠ CONFLICT</span> ':'<span style="color:var(--text-muted);">Reviews:</span> ')+rk.map(function(k){return vfEsc(k)+'='+vfEsc(allr[k]);}).join(' · ')+'</div>'):'';
      var reopenBtn = (present[id]||dropped[id]) ? ('<button onclick="reopenVf(\''+id+'\')" title="clear the applied decision and send back to AI-flagged" style="cursor:pointer; font-size:11px; padding:3px 10px; border-radius:4px; border:1px solid var(--accent-amber); background:transparent; color:var(--accent-amber);">↩ re-open</button>') : '<span style="color:var(--text-muted); font-size:10.5px;">removed — re-extract</span>';
      var challenge='<span style="font-size:10.5px; color:var(--text-muted);">challenge:</span>'
        +'<button onclick="challengeVf(\''+id+'\',\'ok\')" title="record YOUR call = keep; disagreement raises a conflict" style="cursor:pointer; font-size:11px; padding:3px 11px; border-radius:4px; border:1px solid var(--accent-emerald); background:transparent; color:var(--accent-emerald);">ok</button>'
        +'<button onclick="challengeVf(\''+id+'\',\'drop\')" title="record YOUR call = drop; disagreement raises a conflict" style="cursor:pointer; font-size:11px; padding:3px 11px; border-radius:4px; border:1px solid var(--accent-rose); background:transparent; color:var(--accent-rose);">drop</button>';
      var card='<div style="border:1px solid var(--border-color); border-left:3px solid '+(conf?'var(--accent-rose)':col)+'; border-radius:8px; padding:10px 14px; margin-bottom:8px; background:var(--bg-secondary);">'
        +'<div style="display:flex; align-items:center; gap:10px; flex-wrap:wrap;">'
        +'<code style="color:var(--accent-sky); font-size:11.5px;">'+vfEsc(id||'')+'</code>'
        +_orgBadge
        +'<span style="font-weight:700; font-size:10px; color:'+col+'; text-transform:uppercase;">'+vfEsc(dec)+'</span>'
        +'<span style="font-size:11px; color:var(--text-secondary);">'+vfEsc(r.verdict||'')+(r.reason?(' · '+vfEsc((r.reason||'').replace(/_/g,' '))):'')+'</span>'
        +'<span style="margin-left:auto; font-size:10.5px; color:var(--text-muted);">'+vfEsc(r.reviewer||'')+' · '+vfEsc(r.date||'')+'</span></div>'
        +(r.note?('<div style="font-size:11px; margin-top:5px; color:var(--text-secondary);">'+vfEsc(r.note)+'</div>'):'')
        +reviewsLine
        +'<div style="margin-top:7px; display:flex; align-items:center; gap:8px; flex-wrap:wrap;"><span style="font-size:10.5px; color:var(--text-muted);">'+vfEsc(r.source_id||'')+'</span><span style="margin-left:auto; display:inline-flex; align-items:center; gap:8px;">'+challenge+reopenBtn+'</span></div>'
        +'</div>';
      host.insertAdjacentHTML('beforeend',card);
    });
  }

  function _vfFmtVal(v){ // human-readable nested relationship values (no raw JSON for reviewers)
    if(v===null||v===undefined) return '';
    if(Array.isArray(v)) return v.map(_vfFmtVal).join('  ·  ');
    if(typeof v==='object'){
      var lab=v.label!==undefined?v.label:(v.name!==undefined?v.name:(v.class!==undefined?v.class:v.level));
      var val=v.range!==undefined?v.range:(v.value!==undefined?v.value:(v.threshold!==undefined?v.threshold:undefined));
      if(lab!==undefined && val!==undefined) return lab+': '+val;
      return Object.keys(v).map(function(k){ return k.replace(/_/g,' ')+' '+_vfFmtVal(v[k]); }).join(', ');
    }
    return String(v);
  }
  function vfRelHtml(ev){ var r=ev.relationship; var o=null;
    if(r){ if(typeof r==='object')o=r; else { try{ o=JSON.parse(r); }catch(e){} } }
    if(o && typeof o==='object' && !Array.isArray(o)){
      var keys=Object.keys(o); if(!keys.length) return '<span style="color:var(--text-muted);">(none)</span>';
      return '<div style="display:flex; flex-wrap:wrap; gap:3px 16px; margin-top:4px;">'+keys.map(function(k){ var v=_vfFmtVal(o[k]); return '<span style="font-size:11.5px;"><span style="color:var(--text-muted);">'+vfEsc(k.replace(/_/g,' '))+':</span> <b style="color:var(--text-primary);">'+vfEsc(v)+'</b></span>'; }).join('')+'</div>';
    }
    if(r) return '<code style="font-size:10.5px;">'+vfEsc(typeof r==='string'?r:JSON.stringify(r))+'</code>';
    return '<span style="color:var(--text-muted);">(no encoded value — qualitative claim; judge the variable + quote)</span>';
  }
  function vfRelatedTableHtml(ev){
    function context(row){try{return typeof row.context==='object' ? row.context||{} : JSON.parse(row.context||'{}');}catch(e){return {};}}
    var rows=(reviewData.registers.EV_evidence_register)||[];
    var rootId=context(ev).table_continuation_of||ev.evidence_id;
    var root=rows.find(function(row){return row.evidence_id===rootId;});
    function compatible(row){return row.review_state!=='dropped' && ['source_id','nbs_id','variable','suitability_family_id','claim_scope'].every(function(k){return (row[k]||'')===(ev[k]||'');});}
    if(!root || !compatible(root))return '';
    var linked=rows.filter(function(row){return compatible(row) && (row.evidence_id===rootId || context(row).table_continuation_of===rootId);});
    if(linked.length<2 || !linked.some(function(row){return row.evidence_id===ev.evidence_id;}))return '';
    linked.sort(function(a,b){return Number(a.page)-Number(b.page)||a.evidence_id.localeCompare(b.evidence_id);});
    return '<div style="margin:10px 0;padding:12px;border:1px solid var(--border);border-radius:8px;"><b>Table continues across pages</b><p>All linked parts shown together. Your decision applies only to this record; linked parts keep their own review status.</p>'+linked.map(function(row){return '<div style="margin:8px 0;"><b>Page '+vfEsc(row.page)+' · '+(row.evidence_id===ev.evidence_id?'this record':'linked record')+'</b> · '+((row.reviewer_ok===true||row.reviewer_ok==='true')?'approved extraction':'awaiting review')+vfRelHtml(row)+'</div>';}).join('')+'</div>';
  }
  // Review the extracted claim and its intended use, not only relationship fields.
  function vfSourceAuditHtml(ev){
    var notes=typeof reviewData==='undefined'?{}:(reviewData.t4_review_notes||{});
    var note=notes[ev.evidence_id]; if(!note)return '';
    return '<section style="margin:10px 0;padding:10px;border:1px solid var(--accent-amber)"><b>Bounded source audit — approval unchanged</b><p>'+vfEsc(note.finding)+'</p><p><b>Intended use:</b> '+vfEsc(note.intended_use)+'</p><p><b>Remaining decision:</b> '+vfEsc(note.remaining_decision)+'</p><p>'+vfEsc(note.source_check)+'</p><p>Respond using this evidence card’s existing decision and note controls.</p></section>';
  }
  function vfReviewMeaning(ev){
    function obj(value){ if(value && typeof value==='object')return value; try{return JSON.parse(value||'{}')||{};}catch(e){return {};} }
    var c=obj(ev.context), r=obj(ev.relationship), m=c.model_use||{}, provenance=c.model_use_provenance||{};
    var values='', purpose='', question='', image='';
    if(r.type==='observed_presence'){
      values='Observed conditions at documented sites; not a tested suitability range.';
      purpose='Retained as site context. Does not vote for suitability thresholds or exclude places with different conditions.';
      if(ev.variable==='annual_precipitation' && Array.isArray(r.observed_classes) && r.observed_classes.length){
        question='Check the selected rainfall bands'+(ev.page?' on page '+ev.page:' in the source')+' against the extracted classes and any recorded bounds. Choose Keep if they match, or Query if a discrepancy remains.';
      } else {
        question='Check which boxes are selected in the Natural Environment panel, and distinguish topsoil from subsoil. Unselected options are not observations.';
      }
    } else if(Object.keys(m).length){
      var path=Array.isArray(m.weight_path_pct)?m.weight_path_pct:[];
      values=path.length ? 'Weight in this paper: '+path.map(function(w){return String(w)+'%';}).join(' × ') : 'Paper uses this variable; no numeric importance weight recorded.';
      if(path.length>1) values+=' (nested model branches; not necessarily the variable’s total weight).';
      purpose=m.scope==='species_selection' ? 'Documents an input used to choose species. Counted separately from practice-level suitability agreement.' : 'Counts one paper using this variable in its model. Records the paper’s importance weight separately from agreement on suitability thresholds.';
      purpose+=' Model-use information alone does not set a T4 cutoff, response score or default runtime weight.';
      question='Confirm variable use'+(path.length?' and the displayed weight':'')+' against '+(provenance.table||'the source')+' (PDF p'+(provenance.page||m.page||ev.page||'not recorded')+'). '+(Object.keys(r).length?'Also verify the extracted response values below; model use does not validate their thresholds.':'Keep approves this extraction, not a new suitability rule.');
      var img=provenance.image||'';
      if(/^docs\/review\/img\/[A-Za-z0-9_.-]+\.(png|jpg|jpeg)$/.test(img)) image='<details><summary>Inspect '+vfEsc(provenance.table||'source table')+' · PDF p'+vfEsc(provenance.page||'')+'</summary><img loading="lazy" src="'+vfEsc('https://raw.githubusercontent.com/CIAT/nbs_ruralscan/bec50bc0f9dc74b3d5ffafcf881571a8a8ec5c06/docs/'+img.slice(5))+'" alt="Original model-weight table" style="max-width:100%;background:white"></details>';
    } else {
      if(!Object.keys(r).length) values='No numeric threshold or class rule extracted. Review the qualitative claim and its scope.';
      if(ev.use_role==='operational_risk') purpose='Implementation feasibility evidence for M2b / next steps; does not set core biophysical suitability.';
      else if(ev.use_role==='dataset') purpose='Documents a dataset or selection method; does not itself define a suitability response.';
      else if(r.criterion_kind==='programme_eligibility') purpose='Eligibility condition for the named programme only. Not a universal agroforestry threshold.';
      else if(ev.use_role==='structural_suitability') purpose='Candidate suitability evidence. Extraction approval alone does not establish system applicability, dataset mapping or cross-paper combination.';
      else purpose='Evidence for its stated analytical role; review source meaning and applicability before synthesis.';
      question=c.review_needed||(c.recovery_review||{}).note||'Check extracted information against the source, including units and scope. Keep confirms the evidence; query records an unresolved interpretation.';
    }
    if(ev.review_state==='dropped') purpose='Quarantined record; excluded from synthesis. '+purpose;
    var note=(c.recovery_review||{}).note;
    var interpretation=(c.source_check||{}).resolution;
    return '<section style="margin:10px 0;padding:10px 12px;border:1px solid var(--border-color);border-radius:5px;font-size:12px;line-height:1.5">'+(values?'<div><b>Extracted information:</b> '+vfEsc(values)+'</div>':'')+'<div><b>How it will be used:</b> '+vfEsc(purpose)+'</div><div><b>What to review:</b> '+vfEsc(question)+'</div>'+(note&&note!==question?'<div><b>Source limitation:</b> '+vfEsc(note)+'</div>':'')+(interpretation?'<div><b>Source interpretation:</b> '+vfEsc(interpretation)+'</div>':'')+image+'</section>';
  }
  function _vfTabular(q){ q=q||''; return /\d+\s*[–-]\s*\d+/.test(q)||((q).match(/\d+(\.\d+)?/g)||[]).length>=3||q.indexOf('\n')>=0; }
  function _vfVerdictColor(v){ return v==='unsupported'?'var(--accent-rose)':v==='mismatch'?'var(--accent-amber)':v==='pass'?'var(--accent-sky)':v==='scope'?'var(--accent-amber)':'var(--text-secondary)'; }

  // --- Source channel (which discovery pipeline an EV row came from) ---
  // Authoritative from SRC.source_category; friendly labels for the QA/QC view.
  function _vfSrcCatMap(){ if(window.__vfSrcCat)return window.__vfSrcCat; var m={}; ((reviewData.registers.SRC_source_register)||[]).forEach(function(s){ m[s.source_id]=(s.source_category||'').trim(); }); window.__vfSrcCat=m; return m; }
  function _vfChanKey(ev){ var c=_vfSrcCatMap()[ev.source_id]||''; return c||'unknown'; }
  // --- Search round (which discovery ROUND a source came from) ---
  // Derived from SRC.extraction_run_id: 'round<N>_...' = round N; anything else = round 1
  // (the original sweeps, before the naming convention). No schema column needed.
  function _vfRoundMap(){ if(window.__vfRound)return window.__vfRound; var m={}; ((reviewData.registers.SRC_source_register)||[]).forEach(function(s){ var mm=/^round(\d+)_/.exec((s.extraction_run_id||'').trim()); m[s.source_id]=mm?('round'+mm[1]):'round1'; }); window.__vfRound=m; return m; }
  function _vfRoundKey(ev){ return _vfRoundMap()[ev.source_id]||'round1'; }
  function _vfRoundLabel(k){ var n=String(k).replace('round',''); return 'Round '+n+(n==='1'?' (original sweeps)':''); }
  // Open-access gate — same rule as scripts/render-crops.py (license cc-*/other-oa/cc0/
  // public-domain OR access_status open). Drives the Access filter chip + the OA/Restricted
  // card badge. Restricted = copyrighted, crop is team-only via SharePoint.
  function _vfSrcOAMap(){ if(window.__vfSrcOA)return window.__vfSrcOA; var m={}; ((reviewData.registers.SRC_source_register)||[]).forEach(function(s){ var lic=(s.license||'').toLowerCase(); var acc=(s.access_status||'').toLowerCase(); m[s.source_id]=(lic.indexOf('cc-')===0||lic==='other-oa'||lic==='cc0'||lic==='public-domain'||['open_access','open','gold','green','hybrid','oa'].indexOf(acc)>=0); }); window.__vfSrcOA=m; return m; }
  function _vfIsOA(ev){ return !!_vfSrcOAMap()[ev.source_id]; }
  function _vfChanMeta(key){ return ({
      stock:{label:'Stocktake', color:'#a78bfa'},
      updated_lit:{label:'Peer-reviewed · OpenAlex', color:'#38bdf8'},
      grey:{label:'Grey lit · CGSpace / project report', color:'#fbbf24'},
      tool:{label:'Tool / methodology', color:'#34d399'},
      unknown:{label:'Unspecified source', color:'var(--text-muted)'}
    })[key]||{label:key, color:'var(--text-muted)'}; }
  // Shared reason codes — single source of truth for BOTH the per-card reason selector and the
  // bulk-by-source selector, so they can't drift apart.
  var _VF_RC_PASSED=['confirmed_pass','missed_error','wrong_practice','species_envelope','off_scope','wrong_table','constrained_aoi','relationship_missed','insufficient_context','unusable_value','speculative_evidence','other'];
  var _VF_RC_FLAGGED=['smuggled_number','wrong_variable','wrong_practice','species_envelope','table_error','off_scope','wrong_table','constrained_aoi','quote_too_narrow','relationship_missed','insufficient_context','unusable_value','speculative_evidence','false_flag','accepted_correction','other'];
  var _VF_RC_DESC={smuggled_number:'number came from elsewhere in the paper, not this quote',wrong_variable:'labelled the wrong canonical variable (e.g. SOM != SOC, NDVI != canopy)',wrong_practice:'mapped to the wrong NbS / practice (reforestation, pure forestry, carbon-only)',species_envelope:'a per-species envelope, not a practice-level suitability rule',table_error:'mangled or mis-stitched table extraction — cells merged across rows, or garbled/misread values',off_scope:'not a suitability claim (study-site descriptors, methods, problem statement)',wrong_table:'real claim, wrong table — soft enabling-env (tenure / market / road / extension / finance / labour) belongs to T3 / M2b / next-steps, not T4 suitability',constrained_aoi:'source only covers part of the land (e.g. a "marginal / residual land" bucket) → understates where the NbS can actually go; never use to set the AOI / opportunity-space extent',quote_too_narrow:'quote too short / mid-sentence — does not carry the full claim',relationship_missed:'the suitability relationship / directionality / membership curve was present in the source but NOT captured (e.g. monotonic decline with distance, fine-texture = high suitability)',insufficient_context:'cannot review — no caption / surrounding context, or the table screengrab failed to render',unusable_value:'named a variable but gave no usable rule — a weight / score with no scale ("5 out of what?"), or land cover with no class list (which classes in / out?)',speculative_evidence:'speculation / assumption, not first- or second-hand evidence ("may deter", hand-wavy assumed causation)',false_flag:'verifier was wrong; the number IS supported -> keep (ok)',accepted_correction:'verifier auto-correction was right and accepted -> ok',confirmed_pass:'AI pass was correct (ok)',missed_error:'AI should have flagged this — false negative -> drop',other:'something else; explain in the note'};
  function vfDetailHtml(o, passed, opts){ opts=opts||{}; var _collap=!!opts.collapsible,_settledC=!!opts.settled,_openC=!!opts.open,_myDecC=(opts.myDec||'').toLowerCase(); var ev=o.ev, verdict=o.verdict, reason=o.reason; var srcAll=(reviewData.registers.SRC_source_register)||[]; var src=srcAll.find(function(s){return s.source_id===ev.source_id;})||{};
    var _chan=_vfChanMeta(_vfChanKey(ev)); var _chanBadge='<span onclick="vfScopeSet(\'source\',\''+vfEsc(_vfChanKey(ev))+'\')" title="Source channel: '+vfEsc(_chan.label)+' — click to filter the worklist to this channel" style="cursor:pointer; font-size:9.5px; font-weight:700; text-transform:uppercase; letter-spacing:.03em; color:'+_chan.color+'; border:1px solid '+_chan.color+'; border-radius:3px; padding:1px 6px;">'+vfEsc(_chan.label)+'</span>';
    var _rndK=_vfRoundKey(ev); var _roundBadge=(_rndK!=='round1')?('<span onclick="vfScopeSet(\'round\',\''+vfEsc(_rndK)+'\')" title="'+vfEsc(_vfRoundLabel(_rndK))+' — click to filter the worklist to this round" style="cursor:pointer; font-size:9.5px; font-weight:700; color:#fff; background:#f97316; border-radius:3px; padding:2px 6px; margin-left:4px;">'+vfEsc(_vfRoundLabel(_rndK))+'</span>'):'';
    var _oa=_vfIsOA(ev); var _oaCol=_oa?'#34d399':'#fbbf24'; var _oaBadge='<span onclick="vfScopeSet(\'access\',\''+(_oa?'oa':'restricted')+'\')" title="'+(_oa?'Open-access source — crop shown inline / publishable':'Copyrighted (non-open-access) — crop is team-only via SharePoint')+' — click to filter" style="cursor:pointer; font-size:9.5px; font-weight:700; text-transform:uppercase; letter-spacing:.03em; color:'+_oaCol+'; border:1px solid '+_oaCol+'; border-radius:3px; padding:1px 6px;">'+(_oa?'OA':'Restricted')+'</span>';
    var dec=(window._vfDecisions||{})[ev.evidence_id]||'';
    var page=ev.page?('p.'+ev.page):(ev.locator?ev.locator:'page n/a');
    var rel=ev.relationship?(typeof ev.relationship==='string'?ev.relationship:JSON.stringify(ev.relationship)):'';var relShown=rel?vfEsc(rel):'<span style="color:var(--text-muted);">(removed by the verify pass — disputed value is in the reason below)</span>';
    var vc=_vfVerdictColor(verdict);
    // AI's call on this record: passed = AI INCLUDED it (green); flagged = AI marked it for removal (red).
    var _aiInc=passed; var _aiCol=_aiInc?'var(--accent-emerald)':'var(--accent-rose)';
    var _aiBadge='<span style="font-size:10px; font-weight:700; text-transform:uppercase; letter-spacing:.03em; color:#fff; background:'+_aiCol+'; border-radius:3px; padding:2px 8px;">'+(_aiInc?'✓ AI included':'⚑ AI flagged')+'</span>';
    var _autoQD=((ev.review_state||'')==='dropped')&&/\[AUTO-QUARANTINE/.test(ev.attribution||'');
    var _dropBadgeD=((ev.review_state||'')==='dropped')?('<span title="'+(_autoQD?'Auto-quarantined by the guard — no human decision recorded.':'Quarantined — dropped from the analysis (kept &amp; reversible).')+'" style="font-size:9px; font-weight:700; text-transform:uppercase; letter-spacing:.03em; color:#fff; background:'+(_autoQD?'var(--accent-amber)':'var(--accent-rose)')+'; border-radius:3px; padding:2px 8px;">'+(_autoQD?'🤖 auto-quarantined':'🗑 dropped')+'</span>'):'';
    // (the ok / drop / query legend used to be repeated on EVERY card — it now lives once in the
    //  "ℹ How to review" details above the queue; the AI-included/flagged badge still says which.)
    var doi=(src.doi||'').trim();
    var doiHtml=doi?('<a href="'+(doi.indexOf('http')===0?doi:'https://doi.org/'+doi)+'" target="_blank" rel="noopener noreferrer" style="color:var(--accent-sky);">DOI ↗</a>'):(src.url?('<a href="'+src.url+'" target="_blank" rel="noopener noreferrer" style="color:var(--accent-sky);">source ↗</a>'):'');
    var spUrl=vfSharePointUrl(src.library_path||''); if(spUrl&&ev.page)spUrl+='#page='+ev.page;
    var spLink=spUrl?('<a href="'+spUrl+'" target="_blank" rel="noopener noreferrer" style="color:var(--accent-sky);" title="opens the source in SharePoint; no local folder connection needed">📄 Open source · SharePoint'+(ev.page?(' p.'+ev.page):'')+' ↗</a>'):'';
    // Task 1: CODE sources (tool / GEE script) link to the exact file+line on GitHub at the
    // pinned commit — never a "local PDF" (there is no PDF for code).
    var _isCodeSrc=((ev.locator_type||'')==='file_line');
    var _codeAnchor=''; if(_isCodeSrc){ var _clm=/:L(\d+)/.exec(ev.locator||''); if(_clm)_codeAnchor='#L'+_clm[1]; }
    var _codeLink=(_isCodeSrc&&src.url)?('<a href="'+src.url+_codeAnchor+'" target="_blank" rel="noopener noreferrer" style="color:var(--accent-sky);" title="opens the exact file + line on GitHub at the pinned commit '+vfEsc((ev.commit_sha||'').slice(0,7))+'">💻 GitHub '+vfEsc((ev.locator||'code').split('/').pop())+' ↗</a>'):'';
    var localLink=(!_isCodeSrc&&!spLink&&window._reviewApi)?('<a href="/api/pdf?sid='+encodeURIComponent(ev.source_id)+'#page='+(ev.page||1)+'" target="_blank" rel="noopener noreferrer" style="color:var(--accent-amber);">📄 local PDF '+vfEsc(page)+' ↗ (not in SharePoint)</a>'):'';
    var libTxt=(!_isCodeSrc&&!spLink&&!localLink)?'<span style="color:var(--text-muted);">📄 not uploaded</span>':'';
    var pdfLink=[_codeLink,spLink,localLink,libTxt].filter(Boolean).join(' &nbsp;·&nbsp; ');
    var okA=dec==='ok', dropA=dec==='drop', queryA=(dec==='flag'||dec==='query'), reclassA=dec==='reclassify';
    var _rc=passed?_VF_RC_PASSED:_VF_RC_FLAGGED;
    var _rcDesc=_VF_RC_DESC;
    var _rsel=(window._vfReasons||{})[ev.evidence_id]||'';
    var _nval=(window._vfNotes||{})[ev.evidence_id]||'';
    var noteInp='<textarea rows="2" placeholder="note (required for other)" onchange="setVfNote(\''+ev.evidence_id+'\',this.value)" style="font-size:10.5px; padding:5px 7px; border-radius:4px; background:var(--bg-secondary); color:var(--text-primary); border:1px solid var(--border-color); width:100%; resize:vertical; font-family:inherit; box-sizing:border-box;">'+vfEsc(_nval)+'</textarea>';
    var reasonSel='<select onchange="setVfReason(\''+ev.evidence_id+'\',this.value)" style="font-size:10.5px; padding:4px 7px; border-radius:4px; background:var(--bg-secondary); color:var(--text-primary); border:1px solid var(--border-color);"><option value="">reason…</option>'+_rc.map(function(rc){return '<option value="'+rc+'" title="'+vfEsc(_rcDesc[rc])+'"'+(_rsel===rc?' selected':'')+'>'+rc.replace(/_/g,' ')+'</option>';}).join('')+'</select>';
    var _allr=_vfMergedReviews(ev.evidence_id);
    var _rk=Object.keys(_allr);
    var _conf=(new Set(_rk.map(function(rv){return _allr[rv];}))).size>1;
    var reviewsLine=_rk.length?('<div style="font-size:10.5px; margin-top:8px;">'+(_conf?'<span style="color:var(--accent-rose); font-weight:700;">⚠ CONFLICT</span> ':'<span style="color:var(--text-muted);">Reviews:</span> ')+_rk.map(function(rv){return vfEsc(rv)+'='+vfEsc(_allr[rv]);}).join(' · ')+'</div>'):'';
    // Task 4: show what this evidence contributes to (NbS · sub-practice) + its geography, so a
    // reviewer can sanity-check the tagging without opening the source.
    var _nbsShort=(ev.nbs_id||'—').replace(/_/g,' ').replace(/\b\w/g,function(c){return c.toUpperCase();});
    var _famShort=ev.suitability_family_id?familyDisplayName(ev.suitability_family_id):'—';
    var _geoParts=[src.study_country,src.region,src.aez].filter(Boolean);
    var _ctxNote=''; try{ var _cx=ev.context?(typeof ev.context==='string'?JSON.parse(ev.context):ev.context):null; if(_cx&&_cx.note)_ctxNote=_cx.note; }catch(_ge){}
    var _geo=_geoParts.length?_geoParts.join(', '):(_ctxNote||'—');
    // Unified chip row (point 2+3): "contributes to" chips (NbS · sub-practice · location) on the
    // LEFT, source/access chips (OA · channel · source) pushed RIGHT — one line, all uniform pills.
    var _geoShort=(_geo&&_geo!=='—')?(_geo.length>44?_geo.slice(0,42)+'…':_geo):'';   // point 1: hide when empty
    var _nbsChip=_vfChip(vfEsc(_nbsShort),'var(--accent-sky)','Practice — click to filter the worklist to this NbS',"vfScopeSet('nbs','"+vfEsc(ev.nbs_id||'')+"')");
    var _famChip=ev.suitability_family_id?_vfChip(vfEsc(_famShort),'var(--accent-emerald)','Family / evidence scope — click to filter the worklist',"vfScopeSet('family','"+vfEsc(ev.suitability_family_id)+"')"):_vfChip(vfEsc(_famShort),'var(--text-muted)','No family / evidence scope tagged',null);
    // Taxon chip (2026-07): species/crop-specific evidence carries a taxon; the chip both
    // flags "this is banked-for-reuse, not practice suitability" and jumps to the Species lane.
    var _isSpeciesEv=(ev.claim_scope==='species_specific'||ev.claim_scope==='crop_specific');
    var _taxonChip=(_isSpeciesEv&&ev.taxon)?_vfChip('🧬 '+vfEsc(ev.taxon),'var(--accent-amber)','Species/crop-specific ('+vfEsc((ev.claim_scope||'').replace(/_/g,' '))+') — kept & banked for reuse, filtered from the practice MCDA. Click to see the Species lane.',"vfScopeSet('claimScope','"+(ev.claim_scope==='crop_specific'?'crop':'species')+"')",true):'';
    var _geoChip=_geoShort?_vfChip('📍 '+vfEsc(_geoShort),'var(--text-muted)',vfEsc('Study geography: '+_geo),null,true):'';
    var _srcChip=_vfChip(vfEsc(ev.source_id||''),'var(--text-muted)','Source — click to subset the worklist to this source',"vfSetSubset('sourceId','"+vfEsc(ev.source_id||'')+"')",true);
    var _pageChip=ev.page?_vfChip('p.'+vfEsc(String(ev.page)),'var(--text-muted)','Page — click to subset the worklist to page '+vfEsc(String(ev.page))+' of this source',"vfSetSubset('section','"+vfEsc(String(ev.page))+"')",true):'';
    // Recipe table this evidence feeds (T4 suitability), from use_role.
    var _R2Tc={structural_suitability:'T4',operational_risk:'M2b',nbs_effect:'T3/T6',asset_vulnerability:'T3/T6'}; var _tbl=_R2Tc[ev.use_role]||'';
    var _tblChip=_tbl?_vfChip(_tbl,'var(--accent-purple)','Recipe table (Evidence type) this evidence contributes to — click to filter the worklist to '+_tbl,"vfScopeSet('table','"+(_tbl==='T4'?'T4-suitability':_tbl)+"')"):'';
    var _chipRow='<div style="display:flex; align-items:center; gap:6px; flex-wrap:wrap; margin:2px 0 9px 0;"><span style="font-size:11px; color:var(--text-muted); margin-right:1px;" title="what this evidence contributes to">🧩</span>'+_nbsChip+_famChip+_taxonChip+_geoChip+'<span style="margin-left:auto; display:flex; align-items:center; gap:6px; flex-wrap:wrap;">'+_tblChip+_oaBadge+_chanBadge+_roundBadge+_srcChip+_pageChip+'</span></div>';
    var _hasCommittedCrop=(window._cropManifest&&window._cropManifest.has(ev.evidence_id));
    var _hasSharePointCrop=(window._cropSharePointMap && window._cropSharePointMap[ev.evidence_id]);
    // Task 1: server renders /api/crop for ANY passage and /api/code for code sources; the old
    // _vfTabular gate wrongly hid non-tabular OA PDFs + code. Offer whenever the server is up.
    var _showCrop=_hasCommittedCrop||window._reviewApi||_hasSharePointCrop;
    var cropImg=_showCrop?('<div style="margin-top:8px;"><button onclick="vfToggleCrop(\''+ev.evidence_id+'\',this)" style="font-size:10.5px; padding:3px 9px; border-radius:4px; background:transparent; color:var(--accent-sky); border:1px solid var(--border-color); cursor:pointer;">'+(_isCodeSrc?'💻 show source code':'📷 show source region')+'</button><div class="vf-crop" style="display:none; margin-top:6px;"></div></div>'):'';
    // Default-decode categorical class codes (issue #102): readable class names for any
    // class-coded EV (e.g. a CDL crop mask) so the reviewer never sees bare "61, 205…".
    var _dc=((reviewData||{}).decoded_classes||{})[ev.evidence_id];
    var _dcName=function(p){return vfEsc(p[1]||('#'+p[0]));};
    var decodedBlock=_dc?('<div style="margin-top:8px; font-size:10.5px; background:var(--bg-primary); border:1px solid var(--border-color); border-radius:4px; padding:7px 9px;"><b style="color:var(--accent-emerald);">&#128203; Decoded classes ('+_dc.n_included+' included &middot; scheme '+vfEsc(_dc.scheme)+')</b><div style="color:var(--text-secondary); margin-top:3px; line-height:1.5;">'+_dc.included.slice(0,25).map(_dcName).join(', ')+(_dc.included.length>25?(' <span style="color:var(--text-muted);">+'+(_dc.included.length-25)+' more</span>'):'')+'</div>'+((_dc.excluded&&_dc.excluded.length)?('<div style="margin-top:4px; color:var(--accent-rose);"><b>Excluded:</b> '+_dc.excluded.map(_dcName).join(', ')+'</div>'):'')+'</div>'):'';
    // Footer differs by state: pending/unreviewed -> decision buttons; my APPLIED decision -> challenge + re-open.
    var _footerPending='<div style="display:flex; align-items:center; gap:8px; flex-wrap:wrap; margin-top:10px;">'
      +'<a href="#" onclick="vfShowReasonHelp();return false;" title="reason-code definitions" style="font-size:11px; color:var(--accent-sky); text-decoration:underline dotted; cursor:pointer;">Reason ⌄</a>'+reasonSel+'<span style="font-size:11px; color:var(--text-muted); margin-left:auto; font-weight:700;">Your decision:</span>'
      +'<button title="keep this record in the evidence register" onclick="setVfDecision(\''+ev.evidence_id+'\',\'ok\')" style="cursor:pointer; font-size:12px; font-weight:600; padding:5px 16px; border-radius:4px; border:1px solid var(--accent-emerald); background:'+(okA?'var(--accent-emerald)':'transparent')+'; color:'+(okA?'#fff':'var(--accent-emerald)')+';">✓ ok — keep</button>'
      +'<button title="remove this record from the evidence register (soft-delete / quarantine) — pick a reason first" onclick="vfTryDrop(\''+ev.evidence_id+'\')" style="cursor:pointer; font-size:12px; font-weight:600; padding:5px 16px; border-radius:4px; border:1px solid var(--accent-rose); background:'+(dropA?'var(--accent-rose)':'transparent')+'; color:'+(dropA?'#fff':'var(--accent-rose)')+';">✕ drop — remove</button>'
      +'<button title="tentatively keep, but raise an open question for further review — write the question in the note below" onclick="if(!((window._vfNotes||{})[\''+ev.evidence_id+'\']||\'\').trim()){vfNotice(\'Write your question in the note box first — a query needs a note.\',true);return;} setVfDecision(\''+ev.evidence_id+'\',\'flag\')" style="cursor:pointer; font-size:12px; font-weight:600; padding:5px 16px; border-radius:4px; border:1px solid var(--accent-amber); background:'+(queryA?'var(--accent-amber)':'transparent')+'; color:'+(queryA?'#fff':'var(--accent-amber)')+';">⚑ query</button>'
      +'<button title="species/crop-specific evidence → reclassify + KEEP (banked for reuse, filtered from the practice MCDA) — do NOT drop it" onclick="vfReclassify(\''+ev.evidence_id+'\')" style="cursor:pointer; font-size:12px; font-weight:600; padding:5px 12px; border-radius:4px; border:1px solid var(--accent-sky); background:'+(reclassA?'var(--accent-sky)':'transparent')+'; color:'+(reclassA?'#fff':'var(--accent-sky)')+';">🧬 species/crop'+(reclassA&&(window._vfTaxa||{})[ev.evidence_id]?(' · '+vfEsc(window._vfTaxa[ev.evidence_id])):'')+'</button></div>'
      +'<div style="margin-top:8px;">'+noteInp+'</div>';
    var _footerSettled='<div style="display:flex; align-items:center; gap:8px; flex-wrap:wrap; margin-top:12px; border-top:1px solid var(--border-color); padding-top:10px;"><span style="font-size:10.5px; color:var(--text-muted);">You applied this — <b>challenge</b> (a differing call raises a conflict) or <b>re-open</b> to redo:</span><span style="margin-left:auto; display:inline-flex; gap:8px; align-items:center;"><button onclick="challengeVf(\''+ev.evidence_id+'\',\'ok\')" title="record YOUR call = keep" style="cursor:pointer; font-size:12px; font-weight:600; padding:5px 14px; border-radius:4px; border:1px solid var(--accent-emerald); background:transparent; color:var(--accent-emerald);">✓ ok</button><button onclick="challengeVf(\''+ev.evidence_id+'\',\'drop\')" title="record YOUR call = drop" style="cursor:pointer; font-size:12px; font-weight:600; padding:5px 14px; border-radius:4px; border:1px solid var(--accent-rose); background:transparent; color:var(--accent-rose);">✕ drop</button><button onclick="reopenVf(\''+ev.evidence_id+'\')" title="clear the applied decision and send it back to the queue" style="cursor:pointer; font-size:11px; padding:5px 12px; border-radius:4px; border:1px solid var(--accent-amber); background:transparent; color:var(--accent-amber);">↩ re-open</button></span></div>';
    var _footerHtml=window._vfFollowUp==='waiting'?'<p>Waiting for an answer. Your question is saved; no repeat review needed.</p>':(_settledC&&!vfHasAnswerForReview(ev.evidence_id))?_footerSettled:_footerPending;
    var _decChipS=_myDecC?('<span style="font-size:9px; font-weight:700; text-transform:uppercase; padding:1px 7px; border-radius:3px; color:#fff; background:'+(_myDecC==='ok'?'var(--accent-emerald)':(_myDecC==='drop'?'var(--accent-rose)':'var(--accent-amber)'))+';">you: '+vfEsc(_myDecC==='flag'?'query':_myDecC)+'</span>'):'';
    var _revChipS=_rk.length?('<span style="font-size:10px; color:var(--text-muted);">'+_rk.map(function(rv){return vfEsc(rv)+'='+vfEsc(_allr[rv]);}).join(' · ')+'</span>'):'';
    var _summaryHtml='<summary style="cursor:pointer; display:flex; align-items:center; gap:9px; flex-wrap:wrap; padding:9px 14px; border-left:4px solid '+_aiCol+'; border-radius:8px; background:var(--bg-secondary);">'+_aiBadge+_dropBadgeD+(window.DashboardPriority?DashboardPriority.badge(ev):'')+'<code style="color:var(--accent-sky); font-size:11.5px;">'+vfEsc(ev.evidence_id||'')+'</code><span style="font-size:11px; color:var(--text-secondary);">'+vfEsc(ev.variable||'')+' · '+vfEsc((ev.use_role||'').replace(/_/g,' '))+'</span>'+_decChipS+'<span style="margin-left:auto; display:inline-flex; gap:8px; align-items:center;">'+_revChipS+'</span></summary>';
    const intakeLane = ev.use_role === 'operational_risk' ? 'M2b' : ev.use_role === 'structural_suitability' ? 'T4' :
      (DashboardTables.matches(ev, 'T3') || DashboardTables.matches(ev, 'T6') ? 'T3/T6' : '');
    const inlineControls = intakeLane && reviewData.registerRevision && !window._reviewApi ? InlineReview.html(ev.evidence_id, intakeLane, reviewData.registerRevision) : '';
    var _card='<div data-vfeid="'+vfEsc(ev.evidence_id||'')+'" style="border:1px solid '+(dec?'var(--accent-emerald)':'var(--border-color)')+'; border-left:4px solid '+_aiCol+'; border-radius:8px; padding:14px 16px; margin-bottom:10px; background:var(--bg-secondary);">'
      +(_collap?'':('<div style="display:flex; align-items:center; gap:10px; flex-wrap:wrap; margin-bottom:8px;">'
      +_aiBadge+_dropBadgeD+(window.DashboardPriority?DashboardPriority.badge(ev):'')
      +'<code style="color:var(--accent-sky); font-size:12px;">'+vfEsc(ev.evidence_id||'')+'</code>'
      +'<span style="font-weight:700; font-size:10px; color:'+vc+'; text-transform:uppercase;" title="AI verify verdict">'+vfEsc(verdict)+'</span>'
      +'<span style="font-size:11px; color:var(--text-secondary);">'+vfEsc(ev.variable||'')+' · '+vfEsc((ev.use_role||'').replace(/_/g,' '))+' · '+(ev.page?('<a href="#" onclick="vfSetSubset(\'section\',\''+vfEsc(String(ev.page))+'\');return false;" title="subset the worklist to page '+vfEsc(String(ev.page))+' of this source" style="color:var(--accent-sky); text-decoration:none; border-bottom:1px dotted var(--accent-sky);">'+vfEsc(page)+'</a>'):vfEsc(page))+' · '+vfEsc(vfLocHint(ev))+'</span>'
      +'</div>'))
      +(_collap && opts.formerlyCited?'<p>Previously cited in this table. <a href="https://github.com/CIAT/nbs_ruralscan/blob/'+vfEsc(reviewData.formerly_cited[window._vfScope.table][ev.evidence_id])+'">View the earlier CIAT table</a>.</p>':'')
      +(opts.myEvent?'<p><strong>Your recorded decision</strong> · '+vfEsc(opts.myEvent.date)+' · '+vfEsc(opts.myEvent.decision)+(opts.myEvent.reason?' · '+vfEsc(opts.myEvent.reason.replace(/_/g,' ')):'')+(opts.myEvent.note?'<br>'+vfEsc(opts.myEvent.note):'')+'</p>':'')
      +_chipRow
      +'<details class="review-history-link"><summary>Earlier source record</summary><a class="finding-ciat" href="'+vfEsc(DashboardTables.ciatUrl(ev.evidence_id))+'">CIAT source record</a></details>'
      +(ev._reviewConflict?'<p style="border-left:3px solid var(--accent-amber);padding:8px"><b>Reviewers disagree:</b> this record has both Keep and Drop decisions. Check the reviewer notes below and give your judgement.</p>':'')
      +vfClarificationHtml(ev)
      +(window.DashboardPriority?DashboardPriority.card(ev):'')
      +'<details class="review-extraction-details"><summary>Extraction context and checks</summary>'+vfReviewMeaning(ev)+vfSourceAuditHtml(ev)+'</details>'
      +'<div class="review-source-pair"><div class="review-extracted">'
      +(ev.relationship && JSON.stringify(ev.relationship)!=='{}' && ev.relationship!=='{}' ? '<div style="font-size:11.5px;margin:5px 0;"><b>Extracted rule / values:</b> '+vfRelHtml(ev)+'</div>' : '')
      +vfRelatedTableHtml(ev)
      +(!passed?'<div style="font-size:11.5px;margin:5px 0;color:'+vc+';"><b>AI review flag:</b> '+vfEsc(reason)+'</div>':'')
      +'<div style="font-size:11.5px; margin:8px 0; color:var(--text-secondary); background:rgba(255,255,255,0.02); padding:9px 11px; border-radius:4px;"><b style="color:var(--text-muted);">Verbatim quote ('+vfEsc(page)+', '+vfEsc(vfLocHint(ev))+'):</b> '+vfEsc(ev.quote||'')+'</div>'
      +inlineControls+'</div><div class="review-original">'+(reviewData.registerRevision && !window._reviewApi ? SourcePreviews.card(ev.evidence_id) : cropImg)+'</div></div>'
      +decodedBlock
      +reviewsLine
      +'<div style="display:flex; align-items:center; gap:10px; flex-wrap:wrap; margin-top:12px; font-size:10.5px; border-top:1px solid var(--border-color); padding-top:10px;">'+doiHtml+((doiHtml&&pdfLink)?' &nbsp; ':'')+pdfLink+'</div>'
      +(reviewData.registerRevision && !window._reviewApi ? '' : _footerHtml)+'</div>';
    if(_collap){ return '<details data-vfeid="'+vfEsc(ev.evidence_id||'')+'" '+(_openC?'open':'')+' style="margin-bottom:10px;">'+_summaryHtml+_card+'</details>'; }
    return _card;
  }

  // ===== Keyboard-driven review (j/↓ next · ↑ prev · k ok · d drop · q query) =====
  // Operates on the rendered cards in #vf-cards. A "focused" card is tracked by index in
  // window._vfFocusIdx and outlined; the index resets on every re-render (the list reorders).
  // The action keys route through the SAME guarded entry points as the buttons — vfTryDrop for
  // drop (a drop needs a coded reason) and the note-required rule for query — never around them.
  function _vfCardEls(){ var h=document.getElementById('vf-cards'); if(!h)return [];
    return Array.prototype.filter.call(h.children,function(el){return el.hasAttribute('data-vfeid');}); }
  function _vfSetFocus(i){ var cards=_vfCardEls(); if(!cards.length){ window._vfFocusIdx=-1; return; }
    if(i<0)i=0; if(i>cards.length-1)i=cards.length-1; window._vfFocusIdx=i;
    cards.forEach(function(el,k){ if(k===i){ el.style.outline='2px solid var(--accent-sky)'; el.style.outlineOffset='2px'; el.style.borderRadius='8px'; } else { el.style.outline=''; el.style.outlineOffset=''; } });
    try{ cards[i].scrollIntoView({block:'nearest'}); }catch(_e){} }
  // click anywhere in a card → that card becomes the focused one (walk up to the direct child
  // of #vf-cards, so a click on a nested button/chip still resolves to its card).
  function _vfFocusFromNode(n){ var host=document.getElementById('vf-cards'); if(!host)return;
    while(n&&n!==host&&n.parentNode!==host)n=n.parentNode;
    if(!n||n===host)return; var i=_vfCardEls().indexOf(n); if(i>=0)_vfSetFocus(i); }
  function _vfInstallKeys(){ if(window._vfKeysInstalled)return; window._vfKeysInstalled=true;
    window.addEventListener('resize',function(){ try{_vfSyncStickyBars();}catch(_e){} });
    document.addEventListener('click',function(e){ var host=document.getElementById('vf-cards'); if(!host||!host.contains(e.target))return; _vfFocusFromNode(e.target); });
    document.addEventListener('keydown',function(e){
      if(e.ctrlKey||e.metaKey||e.altKey)return;
      var t=e.target||{}; var tn=((t.tagName||'')+'').toUpperCase();
      if(document.querySelector('dialog[open]') || t.closest?.('.source-preview, #vf-sidebar'))return;
      if(tn==='INPUT'||tn==='TEXTAREA'||tn==='SELECT'||t.isContentEditable)return;   // never steal typing
      var tab=document.getElementById('tab-qaqc'); if(!tab||!tab.classList.contains('active'))return;
      var cards=_vfCardEls(); if(!cards.length)return;
      var k=e.key, cur=window._vfFocusIdx; if(cur===undefined||cur===null||cur<0)cur=-1;
      if(k==='j'||k==='ArrowDown'){ e.preventDefault(); _vfSetFocus(cur<0?0:cur+1); return; }
      if(k==='ArrowUp'){ e.preventDefault(); _vfSetFocus(cur<0?0:cur-1); return; }
      if(cur<0||cur>=cards.length)return;
      var el=cards[cur]; var eid=el.getAttribute('data-vfeid'); if(!eid)return;        // gap cards etc. carry none
      if(reviewData.registerRevision && !window._reviewApi && ['k','d','q'].includes(k)){
        e.preventDefault(); InlineReview.key(el,k); return;
      }
      if(k==='k'){ e.preventDefault(); setVfDecision(eid,'ok'); return; }
      if(k==='d'){ e.preventDefault();
        if(!((window._vfReasons||{})[eid]||'')){ var sel=el.querySelector('select'); if(sel){ try{sel.scrollIntoView({block:'nearest'});}catch(_e){} try{sel.focus();}catch(_e2){} } return; }
        vfTryDrop(eid); return; }
      if(k==='q'){ e.preventDefault(); var ta=el.querySelector('textarea'); if(ta){ try{ta.scrollIntoView({block:'nearest'});}catch(_e){} try{ta.focus();}catch(_e3){} } return; }
    });
  }
  // Keep batch actions at the bottom; filters now live in their own sidebar.
  function _vfSyncStickyBars(){ var fb=document.getElementById('vf-filterbar'), ab=document.getElementById('vf-actionbar');
    if(!fb||!ab)return; ab.style.top='auto'; ab.style.bottom='0'; }

  function renderVfWorklist() {
    if (!reviewData) return;
    document.getElementById('tab-qaqc').toggleAttribute('data-public-review', Boolean(reviewData.registerRevision && !window._reviewApi));
    if (!window._vfDecisions){ try{ window._vfDecisions=JSON.parse(localStorage.getItem('vfDecisions')||'{}'); }catch(e){ window._vfDecisions={}; } }
    if (!window._vfReasons){ try{ window._vfReasons=JSON.parse(localStorage.getItem('vfReasons')||'{}'); }catch(e){ window._vfReasons={}; } }
    if (!window._vfNotes){ try{ window._vfNotes=JSON.parse(localStorage.getItem('vfNotes')||'{}'); }catch(e){ window._vfNotes={}; } }
    if (window._vfReviewer===undefined){ window._vfReviewer=localStorage.getItem('vfReviewer')||''; }
    _vfInstallKeys();                       // idempotent — one document-level listener, ever
    window._vfFocusIdx=-1;                  // the card list is about to be rebuilt; drop the focus
    syncVfReviewerPicker();
    window.ReviewBatch?.refresh();
    var evAll=reviewData.registers.EV_evidence_register||[]; var srcAll=reviewData.registers.SRC_source_register||[];
    var mode=window._vfMode||'flagged';
    var flaggedRows=[];
    evAll.forEach(function(ev){ var attr=ev.attribution||''; var idx=attr.indexOf('[VERIFY-FLAG '); if(idx===-1)return;
      var raw=attr.slice(idx+13); var close=raw.indexOf(']'); var body=close!==-1?raw.slice(0,close):raw;
      var ci=body.indexOf(': '); var verdict=(ci!==-1?body.slice(0,ci):body).trim().toLowerCase(); var reason=ci!==-1?body.slice(ci+2).trim():'';
      flaggedRows.push({ev:ev,verdict:verdict,reason:reason}); });
    window._vfFlagged=flaggedRows;
    var flaggedIds={}; flaggedRows.forEach(function(r){flaggedIds[r.ev.evidence_id]=1;});
    var passedAll=evAll.filter(function(ev){ return !flaggedIds[ev.evidence_id] && (ev.use_role!=='dataset'); });
    // scope filter — pills derived from the data model; NbS controls table + family options
    var _nbsOpts=Array.from(new Set(evAll.map(function(e){return e.nbs_id;}).filter(Boolean))).sort();
    if(!window._vfScope)window._vfScope={nbs:(_nbsOpts.indexOf('agroforestry')>=0?'agroforestry':(_nbsOpts[0]||'all')),table:'T4',family:'all',source:'all',access:'all',claimScope:'general',sourceId:'',section:''};
    if(window._vfScope.observations===undefined)window._vfScope.observations='hide';
    if(window._vfScope.source===undefined)window._vfScope.source='all';
    if(window._vfScope.round===undefined)window._vfScope.round='all';
    if(window._vfScope.access===undefined)window._vfScope.access='all';
    if(window._vfScope.claimScope===undefined)window._vfScope.claimScope='general';
    if(window._vfScope.sourceId===undefined)window._vfScope.sourceId='';
    if(window._vfScope.section===undefined)window._vfScope.section='';
    // T4 remains the default; explicit all-scope is available for review batches.
    if(!window._vfScope.table)window._vfScope.table='T4';
    // Explicit all-practice scope supports priority batches spanning practices.
    DashboardTables.describe(window._vfScope.table);
    _vfUpdatePending(); _vfRenderSubsetBanner();
    // Task 3: sourceId subsets to one paper/tool; section subsets to one page within it.
    function _inScope(ev){ return _vfInScope(ev,true); }
    var scEl=document.getElementById('vf-scope');
    if(scEl){ var _inNbs=function(e){ return window._vfScope.nbs==='all'||e.nbs_id===window._vfScope.nbs; };
      var _famOpts=Array.from(new Set(evAll.filter(_inNbs).map(function(e){return e.suitability_family_id;}).filter(Boolean))).sort();
      // Always show the 4 canonical channels (Tool is its own chip, distinct from Grey)
      // even when a channel has no evidence yet; append 'unknown' only if data has it.
      var _srcPresent=new Set(evAll.filter(_inNbs).map(_vfChanKey));
      var _srcOpts=['stock','updated_lit','grey','tool'].concat(_srcPresent.has('unknown')?['unknown']:[]);
      // noAll=true → single-select mandatory (no "All" pill): used for Practice + Evidence-type.
      var _mkPills=function(key,label,opts,fmt,cls,noAll,tip){ var cur=window._vfScope[key]; var list=(noAll?[]:['all']).concat(opts); var btns=list.map(function(o){ var a=(cur===o)?(' active '+cls):''; var lab=(o==='all'?'All':fmt(o)); return '<button class="pill-btn'+a+'" onclick="if(window.DashboardPriority)DashboardPriority.leaveFocus();window._vfScope.'+key+'=\''+o+'\'; if(\''+key+'\'===\'nbs\'){window._vfScope.family=\'all\';window._vfScope.round=\'all\';} renderVfWorklist();" style="font-size:11px; padding:4px 10px; border-radius:6px;">'+vfEsc(lab)+'</button>'; }).join(''); return '<div style="display:flex; align-items:center; gap:6px; flex-wrap:wrap;"'+(tip?(' title="'+vfEsc(tip)+'"'):'')+'><span style="font-size:10px; color:var(--text-muted); text-transform:uppercase; letter-spacing:.04em; margin-right:2px; min-width:84px;">'+label+'</span>'+btns+'</div>'; };
      // Evidence type: T4 (suitability) or T3/T6 (effect + asset-vulnerability units behind the
      // generated hazard / scorecard rows; QA items from the prose reviews land here, 2026-10).
      var _tblDesc={T4:'<b>T4 analysis · Suitability + operational feasibility</b> — review establishment conditions and M2b implementation evidence together. Operational evidence remains separate from the core suitability score.','T3/T6':'<b>T3/T6 · Effects</b> — what the NbS does to hazards and priorities (effect units) and what hazards do to the works (asset vulnerability). Generated rows; review = these units.'};
      var _tblLegend='<div style="font-size:9.5px; color:var(--text-muted); margin:2px 0 4px 0; line-height:1.4;">'+(_tblDesc[window._vfScope.table]||'')+'</div>';
      var _capNbs=function(o){return o.replace(/_/g,' ').replace(/\b\w/g,function(c){return c.toUpperCase();});};
      var _capFam=familyDisplayName;
      // claim_scope lane (2026-07): count rows per lane within the current Practice so the
      // pills show "🧬 Species (N awaiting)". General = practice-level (default); species/crop
      // are kept + banked for reuse but filtered from the practice MCDA.
      var _csOf=function(e){return e.claim_scope||'practice_technology';};
      var _csCount=function(v){ return evAll.filter(_inNbs).filter(function(e){ var c=_csOf(e); return v==='general'?c==='practice_technology':(v==='species'?c==='species_specific':(v==='crop'?c==='crop_specific':true)); }).length; };
      var _csFmt=function(o){ var m={general:'General (practice)',species:'🧬 Species',crop:'🌾 Crop'}; var lab=m[o]||o; var n=_csCount(o); return n?(lab+' ('+n+')'):lab; };
      var _csHint=(window._vfScope.claimScope&&window._vfScope.claimScope!=='general'&&window._vfScope.claimScope!=='all')?'<div style="font-size:9.5px; color:var(--text-muted); margin:2px 0 4px 0; line-height:1.4;">🧬 <b>Species / crop lane</b> — per-taxon evidence, <b>kept &amp; banked for reuse</b> but filtered out of the practice-level MCDA. Fix a mis-tagged row by re-classifying it (keep), not dropping it.</div>':'';
      var select=function(key,label,options){return '<label>'+label+' <select'+(key==='table'?' aria-describedby="review-table-description"':'')+' onchange="vfScopeSet(\''+key+'\',this.value)" style="padding:7px;background:var(--bg-secondary);color:var(--text-primary);border:1px solid var(--border-color);border-radius:5px">'+options.map(function(o){return '<option value="'+vfEsc(o[0])+'"'+(window._vfScope[key]===o[0]?' selected':'')+'>'+vfEsc(o[1])+'</option>';}).join('')+'</select></label>';};
      scEl.innerHTML=select('nbs','Practice',[['all','All practices']].concat(_nbsOpts.map(function(n){return [n,_capNbs(n)];})))
        +select('family','Family / evidence scope',[['all','All families']].concat(_famOpts.map(function(f){return [f,_capFam(f)];})))
        +select('table','Evidence type',[['all','All evidence types'],['T3','T3 hazard findings'],['T4-suitability','T4 suitability findings'],['T6','T6 scorecard findings'],['M2b','M2b operational feasibility'],['T4','T4 + operational feasibility'],['T3/T6','T3/T6 effects']])
        +'<label>Search <input id="vf-search" type="search" placeholder="Paper, variable or text" value="'+vfEsc(window._vfSearch||'')+'" oninput="vfSearch(this.value)" style="padding:7px;background:var(--bg-secondary);color:var(--text-primary);border:1px solid var(--border-color);border-radius:5px"></label>';
      window._vfAdvancedScopeHtml=_mkPills('observations','Site observations',['hide','show','only'],function(o){return {hide:'Hide (default)',show:'Include',only:'Only observations'}[o];},'sky',true,'Site descriptions and observed presence are deferred; tested relationships remain in review.')
        +_mkPills('claimScope','Scope',['general','species','crop'],_csFmt,'sky',false)
        +_mkPills('source','Source channel',_srcOpts,function(o){return _vfChanMeta(o).label;},'amber',false)
        +_mkPills('access','Access',['oa','restricted'],function(o){return o==='oa'?'Open-access':'Restricted';},'emerald',false);
    }
    var _vfPreScope=flaggedRows.map(function(r){return r.ev;}).concat(passedAll, (reviewData._evDropped||[]).filter(function(e){return e.use_role!=='dataset';})); window._vfPreScope=_vfPreScope;
    flaggedRows=flaggedRows.filter(function(r){return _inScope(r.ev);}); window._vfFlagged=flaggedRows;
    passedAll=passedAll.filter(_inScope);
    var rlAll=vfReviewerEvents();
    var _gapsCount=((reviewData.gaps)||[]).filter(_vfGapInScope).length;
    // ===== Orthogonal review-status axes: origin × reviewed-by-me × reviewed-by-others =====
    // Replaces the mode-encodes-status split. Every permutation is a toggle combo,
    // composed with scope + verdict + tables. Universe includes ACTIVE (flagged∪passed) AND DROPPED
    // units. Active is the default; dropped evidence is available through the explicit history filter.
    if(window._vfAxStatus===undefined)window._vfAxStatus='active';
    if(window._vfAxOrigin===undefined)window._vfAxOrigin='any';
    if(window._vfAxMe===undefined)window._vfAxMe='no';
    if(window._vfAxOther===undefined)window._vfAxOther='any';
    if(window._vfMyCall===undefined)window._vfMyCall='all';
    if(window._vfFollowUp===undefined)window._vfFollowUp='all';
    if(window._vfVerdictFilter===undefined)window._vfVerdictFilter='all';
    // reviewed-by predicates: pending (this session) + persistent store (all reviewers) + committed log.
    var publicQueue=reviewData.registerRevision && !window._reviewApi;
    var _store=publicQueue ? {} : (window._vfAllReviews||{}), _pend=publicQueue ? ReviewBatch.pending(reviewData.registerRevision) : (window._vfDecisions||{});
    var _meH=(window._vfReviewer||'').trim();
    var _repeatConflicts=vfRepeatedConflicts(rlAll,_meH);
    // committed decisions per (id,reviewer). A 'reopen' row CLEARS that reviewer's prior decision —
    // the unit is back in play awaiting a fresh call, so it must NOT count as reviewed-by-them, and
    // (for me) it overrides any now-stale store decision so the unit resurfaces in To review / AI-flagged.
    var _rlByRev={}, _reopMe={}, myEvents={};
    rlAll.forEach(function(r){ var d=(r.decision||'').toLowerCase(); if(!d)return; var id=r.evidence_id, who=r.reviewer||'?'; _rlByRev[id]=_rlByRev[id]||{};
      if(d==='reopen'){ delete _rlByRev[id][who]; if(who===_meH){_reopMe[id]=true; delete myEvents[id];} }
      else { _rlByRev[id][who]=d; if(who===_meH){delete _reopMe[id]; myEvents[id]=r;} } });
    var _uMe=function(id){ if(_pend[id])return true; if(_reopMe[id])return false; var s=_store[id]||{}; if(_meH&&s[_meH]&&s[_meH].decision)return true; return !!(_meH&&(_rlByRev[id]||{})[_meH]); };
    var _uOther=function(id){ var s=_store[id]||{}; if(Object.keys(s).some(function(k){return k!==_meH&&s[k]&&s[k].decision;}))return true; return Object.keys(_rlByRev[id]||{}).some(function(k){return k!==_meH;}); };
    var _uMyDec=function(id){ if(_pend[id])return (_pend[id]||'').toLowerCase(); if(_reopMe[id])return ''; var s=_store[id]||{}; if(_meH&&s[_meH]&&s[_meH].decision)return (s[_meH].decision||'').toLowerCase(); return _meH?((_rlByRev[id]||{})[_meH]||''):''; };
    // Has MY decision been APPLIED (committed to the review_log, or stamped applied in the store)?
    // This — not the register's reviewer_ok/dropped state — decides settled (compact card) vs
    // in-progress (full editable card), so an applied *query* reads as settled like an ok/drop does.
    var _meApplied=function(id){ if(_pend[id]||_reopMe[id])return false; if((_rlByRev[id]||{})[_meH])return true; var s=_store[id]||{}; return !!(_meH&&s[_meH]&&(s[_meH].applied===true||s[_meH].applied==='true')); };
    // Build the annotated universe (deduped by evidence_id). flaggedRows/passedAll are already scoped.
    var _uni=[], _useen={};
    var _pushU=function(ev,origin,verdict,reason){ var id=ev.evidence_id; if(_useen[id])return; _useen[id]=1;
      var isDrop=((ev.review_state||'')==='dropped');
      var decisions=Object.assign({},_rlByRev[id]||{});
      Object.keys(_store[id]||{}).forEach(function(who){var d=_store[id][who]; if(d&&d.decision)decisions[who]=d.decision;});
      if(_reopMe[id])delete decisions[_meH];
      if(_pend[id])decisions[_meH]=_pend[id];
      ev._reviewQueue=_vfReviewBucket(ev,decisions);
      var calls=Object.values(decisions).map(function(d){return d==='keep'?'ok':d;});ev._reviewConflict=calls.indexOf('ok')>=0&&calls.indexOf('drop')>=0;
      if(!isDrop&&vfHasAnswerForReview(id))ev._reviewQueue='first';
      _uni.push({myEvent:myEvents[id],formerlyCited:!DashboardTables.matches(ev,window._vfScope.table),ev:ev,origin:origin,verdict:verdict,reason:reason,me:_uMe(id),other:_uOther(id),myDec:_uMyDec(id),conflictReviewed:!!_repeatConflicts[id]||!!((_store[id]||{})[_meH]||{}).reviewed_conflict_at,meApplied:_meApplied(id),dropped:isDrop}); };
    flaggedRows.forEach(function(r){ _pushU(r.ev,'flagged',r.verdict,r.reason); });
    passedAll.forEach(function(ev){ _pushU(ev,'passed','pass','AI accepted this extraction — spot-check: is the encoded value faithful to the quote?'); });
    ((reviewData._evDropped)||[]).forEach(function(ev){ if(ev.use_role==='dataset')return; if(!_inScope(ev))return; var o=/\[VERIFY-FLAG/.test(ev.attribution||'')?'flagged':'passed'; _pushU(ev,o,o==='flagged'?'flagged':'pass',''); });
    // Counts use exactly the view and candidate value that the button will select.
    var _axN=function(which,val){var candidate={ignoreFocus:true};candidate[which]=val;
      return _uni.filter(function(u){return vfMatchesFilters(u,candidate);}).length;};
    // ---- sidebar presets (set the toggles; keep familiar labels + counts) ----
    var _gb=document.getElementById('vf-gaps-btn'); if(_gb){ var _gon=(mode==='gaps'); _gb.style.background=_gon?'var(--accent-amber)':'transparent'; _gb.style.color=_gon?'#0b0b0b':'var(--accent-amber)'; _gb.textContent=(_gon?'← Back to review':'⚠ Gaps ('+_gapsCount+')'); }
    var _sb=document.getElementById('vf-stats-btn'); if(_sb){ var _on=(mode==='stats'); _sb.style.background=_on?'var(--accent-emerald)':'transparent'; _sb.style.color=_on?'#fff':'var(--accent-emerald)'; _sb.textContent=_on?'← Back to review':'📊 Stats'; }
    const personal = vfPersonalHistory();
    const extraReviews = personal.archived.length + personal.ratings.length;
    const isMyHistory = vfShowPersonalHistory();
    document.getElementById('public-review-history').hidden = !isMyHistory;
    var fd=document.getElementById('vf-verdict-filters'); var host=document.getElementById('vf-cards'); var statsHost=document.getElementById('vf-stats');
    document.getElementById('vf-sidebar-filters').hidden = mode==='stats'||mode==='gaps';
    if(mode==='stats'){ if(fd)fd.style.display='none'; if(host)host.style.display='none'; var dcs=document.getElementById('vf-decided-count'); if(dcs)dcs.innerHTML=''; if(statsHost){statsHost.style.display='block'; renderQaqcStats(statsHost);} _vfSyncStickyBars(); return; }
    if(mode==='gaps'){ if(fd)fd.style.display='none'; if(statsHost)statsHost.style.display='none'; if(host){host.style.display='block'; renderVfGaps(host);} _vfSyncStickyBars(); return; }
    if(statsHost)statsHost.style.display='none'; if(host)host.style.display='block';
    var _tblPill='<button class="pill-btn '+(window._vfTablesOnly?'active sky':'')+'" aria-pressed="'+!!window._vfTablesOnly+'" onclick="vfSetFilter(\'tables\',!window._vfTablesOnly)" style="font-size:11px; padding:3px 10px; border-radius:4px;" title="only units whose quote is tabular (📷)">📷 tables</button>';
    // ---- filter bar: 3 orthogonal toggles (+ My-call when me=Yes) + verdict + tables ----
    if(fd){ fd.style.display='block'; fd.style.gap=''; fd.style.flexWrap=''; fd.style.alignItems='';
      // One row per axis: a fixed-width label column keeps the pill columns aligned down the bar.
      var _seg=function(which,label,opts,sv,tip){ return '<div style="display:flex; align-items:center; gap:4px; flex-wrap:wrap; margin:1px 0;"'+(tip?(' title="'+vfEsc(tip)+'"'):'')+'><span style="font-size:9px; color:var(--text-muted); text-transform:uppercase; letter-spacing:.05em; font-weight:700; min-width:118px; flex:0 0 118px;">'+label+'</span>'+opts.map(function(o){ var active=(window[sv]===o[0])?'active sky':''; var cnt=which?(' ('+_axN(which,o[0])+')'):''; return '<button class="pill-btn '+active+'" aria-pressed="'+(window[sv]===o[0])+'" onclick="vfSetFilter(\''+which+'\',\''+o[0]+'\')" style="font-size:11px; padding:3px 10px; border-radius:4px;">'+o[1]+cnt+'</button>'; }).join('')+'</div>'; };
      var _bar=_seg('status','Record status',[['active','Active'],['dropped','Dropped history'],['any','All']],'_vfAxStatus','Dropped records stay excluded from the normal review queue. Show history to inspect, challenge or reopen them.')
        +_seg('origin','Origin',[['any','Any'],['flagged','⚑ AI-flagged'],['passed','✓ AI-passed']],'_vfAxOrigin','Did the AI verify pass flag this extraction, or accept it?')
        +_seg('me','Reviewed by me',[['any','Any'],['no','No'],['yes','Yes']],'_vfAxMe','Does the selected reviewer have a current decision? Reopened decisions do not count. Shortcuts above set these same filters.')
        +_seg('other','Reviewed by others',[['any','Any'],['no','No'],['yes','Yes']],'_vfAxOther','Has anyone else made a call? Not-me + others-Yes = the 2nd-opinion queue.');
      // Search round: which discovery round the source came from (SRC.extraction_run_id prefix).
      // Counts retain the current queue, reviewer axes, search and task; only round changes.
      var _rdAll=Array.from(new Set(((window._vfPreScope)||[]).map(_vfRoundKey))).sort();
      var _rdN=function(k){return _uni.filter(function(u){return vfMatchesFilters(u,{round:k,ignoreFocus:true});}).length;};
      var _rdCur=(window._vfScope&&window._vfScope.round)||'all';
      _bar+='<div style="display:flex; align-items:center; gap:4px; flex-wrap:wrap; margin:1px 0;" title="Which discovery round the source was found in. Round 1 = the original sweeps; Round 2 = grey literature + WOCAT practice database (2026-09)."><span style="font-size:9px; color:var(--text-muted); text-transform:uppercase; letter-spacing:.05em; font-weight:700; min-width:118px; flex:0 0 118px;">Search round</span>'
        +['all'].concat(_rdAll).map(function(k){ var active=(_rdCur===k)?'active sky':''; var lab=(k==='all')?'Any':('Round '+String(k).replace('round','')); return '<button class="pill-btn '+active+'" onclick="if(window.DashboardPriority)DashboardPriority.leaveFocus();window._vfScope.round=\''+k+'\'; renderVfWorklist();" style="font-size:11px; padding:3px 10px; border-radius:4px;">'+lab+' ('+_rdN(k)+')</button>'; }).join('')+'</div>';
      if(window._vfAxMe==='yes'){ _bar+=_seg('call','My call',[['all','All'],['ok','✓ Kept'],['query','⚑ Queried'],['drop','🗑 Dropped']],'_vfMyCall','Narrow your own reviewed units by the call you made.'); }
      // Keep every active filter visible, including an empty origin/verdict combination.
      var _extra='';
      { var verdicts=['all'].concat(Array.from(new Set(_uni.filter(function(u){return u.origin==='flagged';}).map(function(u){return u.verdict;})))).filter(function(v){return v!=='conflict';});
        _extra=verdicts.map(function(v){ var active=window._vfVerdictFilter===v?'active rose':''; var n=(v==='all')?0:_axN('verdict',v); return '<button class="pill-btn '+active+'" aria-pressed="'+(window._vfVerdictFilter===v)+'" onclick="vfSetFilter(\'verdict\',\''+v+'\')" style="font-size:11px; padding:3px 10px; border-radius:4px; text-transform:capitalize;">'+(v==='all'?'All':(v+' ('+n+')'))+'</button>'; }).join('')+'<span style="width:1px; height:16px; background:var(--border-color); margin:0 5px;"></span>'; }
      _bar+='<div style="display:flex; align-items:center; gap:4px; flex-wrap:wrap; margin:3px 0 0; padding-top:4px; border-top:1px solid var(--border-color);" title="Filter by AI verification result. Tables limits the queue to tabular quotes."><span style="font-size:9px; color:var(--text-muted); text-transform:uppercase; letter-spacing:.05em; font-weight:700; min-width:118px; flex:0 0 118px;">Verdict</span>'+_extra+_tblPill+'</div>';
      var followups=[['all','All findings'],['answers','Answers ready'],['waiting','Waiting for answers'],['conflict','Conflicts'],['requested','Requested rechecks'],['unresolved','Decision / status checks'],['approval_only','Missing review history']];
      _bar+='<div><label for="vf-followup">Follow-up</label><select id="vf-followup" onchange="vfSetFilter(\'followup\',this.value)">'+followups.map(function(q){return '<option value="'+q[0]+'"'+((window._vfFollowUp||'all')===q[0]?' selected':'')+'>'+q[1]+' ('+_axN('followup',q[0])+')</option>';}).join('')+'</select></div>';
      var shortcuts=[['todo','To review','Active findings not reviewed by you.'],['flagged','AI-flagged','AI-flagged findings not reviewed by you.'],['passed','AI-passed','AI-passed findings not reviewed by you.'],['second','2nd opinion','Active findings reviewed by others, not by you.'],['kept','Kept','Your Keep decisions on active findings.'],['queried','Queried','Your Query decisions on active findings.'],['dropped','Dropped','Your Drop decisions, including saved drafts. Record status may still be active.'],['mine','My reviewed','All your current finding decisions, plus separate archived and rating history.'],['answers','Answers ready','Returned answers, including findings you previously queried.'],['conflict','Conflicts','Findings with opposing Keep and Drop decisions.']];
      const summary='<nav class="vf-shortcuts" aria-label="Review shortcuts">'+shortcuts.map(function(q){
        var filters=vfShortcutFilters(q[0]);filters.ignoreFocus=true;
        var count=_uni.filter(function(u){return vfMatchesFilters(u,filters);}).length+(vfShowPersonalHistory(filters)?extraReviews:0);
        var active=vfShortcutSelected(q[0]);
        return '<button type="button" data-review-shortcut="'+q[0]+'" aria-pressed="'+active+'" class="pill-btn '+(active?'active sky':'')+'" title="'+q[2]+'" onclick="vfShortcut(\''+q[0]+'\')">'+q[1]+' ('+count+')</button>';
      }).join('')+'</nav><p class="vf-filter-help">Shortcuts set the sidebar filters. Refine them there. <b>To review = not reviewed by you.</b> <button type="button" class="pill-btn" onclick="vfShortcut(\'all\')">All records</button></p>';
      var cl=window._vfClarificationError?'<p>'+vfEsc(window._vfClarificationError)+'</p>':'';
      fd.innerHTML=summary+(window.DashboardPriority?DashboardPriority.controls():'')+(isMyHistory?vfArchivedHistory(personal.archived)+vfRatingHistory(personal.ratings):'')+cl;
      document.getElementById('vf-sidebar-filters').innerHTML='<div class="vf-custom-view">Filters apply together. Counts show results after selection.</div><div class="vf-filter-groups">'+(window._vfAdvancedScopeHtml||'')+_bar+'</div><details data-local-review-only><summary>Review a whole source</summary><div id="vf-bulk"></div></details>'; }

    var _list=_uni.filter(function(u){return vfMatchesFilters(u);});
    // stable seeded order (hash) so cards don't jump between renders.
    if(window._vfPassSeed===undefined)window._vfPassSeed=Math.floor(Math.random()*1e9); var _seed=window._vfPassSeed;
    _list=_list.map(function(u){ var h=0,s=u.ev.evidence_id+'|'+_seed; for(var i=0;i<s.length;i++){h=((h<<5)-h+s.charCodeAt(i))|0;} return {u:u,h:h>>>0}; }).sort(function(a,b){return Number(vfHasAnswerForReview(b.u.ev.evidence_id))-Number(vfHasAnswerForReview(a.u.ev.evidence_id))||a.h-b.h;}).map(function(x){return x.u;});
    if(window._vfAxMe==='yes'){
      _list.sort((a,b)=>String(b.myEvent?.date || '').localeCompare(String(a.myEvent?.date || '')) || a.ev.evidence_id.localeCompare(b.ev.evidence_id));
    }
    // decided-count line — reflects the current toggle combo.
    const countLine = document.getElementById('vf-decided-count');
    if (countLine) {
      if (isMyHistory) {
        const groups = [[_list.length, 'finding card'], [personal.archived.length, 'archived finding review'],
          [personal.ratings.length, 'rating decision']];
        countLine.textContent = groups.filter(([count]) => count).map(([count, label]) =>
          count + ' ' + label + (count === 1 ? '' : 's')).join(' · ');
        if (_list.some(u => u.formerlyCited)) countLine.textContent += '. Includes findings cited in earlier CIAT ratings.';
      } else {
        countLine.textContent = _list.length + ' records' + (window._vfFollowUp === 'waiting' ?
          ' — no action needed until answers arrive.' : window._vfAxMe==='no' ? ' — not reviewed by you; check each source before choosing Keep, Drop or Query.' : ' — check each passage before choosing Keep, Drop or Query.');
      }
    }
    _vfRenderBulk(evAll);
    if(!host)return; host.innerHTML='';
    if(!_list.length){
      if (isMyHistory) {
        if (!extraReviews) {
          host.textContent = window._vfReviewer ? 'No review history for ' + window._vfReviewer + ' matches this queue and its filters.' :
            'Choose your reviewer handle to see your review history.';
        }
        _vfSyncStickyBars();
        return;
      }
      if((window._vfScope||{}).source==='tool'&&!_uni.length){
        var _nTool=((reviewData.registers||{}).TOOL_tool_registry||[]).length;
        host.innerHTML='<div style="color:var(--text-muted); padding:14px; line-height:1.5;"><b style="color:var(--accent-amber);">No tool-derived evidence extracted yet.</b><br>Tools / methods / codebases <b>are evidence-reviewable like any source</b> — their thresholds, weights and criteria become EV rows (provenance via <code>locator=file_line</code>+<code>commit_sha</code> for code, or section/anchor for docs) and are reviewed here under this channel. This is empty only because no tool has been extracted yet. <b>'+_nTool+'</b> tool(s) are catalogued in <code>TOOL_tool_registry</code> — browse them under <b>Bibliography</b>; extracting their criteria populates this channel.</div>';
        return;
      }
      host.innerHTML='<div style="color:var(--text-muted); padding:14px; line-height:1.6;">No records match these filters. Change sidebar filters or choose another shortcut.</div>'; _vfSyncStickyBars(); return; }
    // One collapsible card per unit. Furled (closed) when I've already applied a decision — the
    // summary row shows my call; expand for the full evidence + challenge / re-open. Unfurled (open)
    // for anything I still need to act on (to-review, 2nd opinion, or my pending unapplied decision).
    // Render long queues a page at a time. Counts and filters use the full list.
    let rendered = 0;
    function showNextCards() {
      const batch = _list.slice(rendered, rendered + 20);
      host.insertAdjacentHTML('beforeend', batch.map(function(u){
        return vfDetailHtml({ev:u.ev, verdict:u.verdict, reason:u.reason}, u.origin==='passed',
          {collapsible:true, myEvent:window._vfAxMe==='yes'?u.myEvent:null, formerlyCited:u.formerlyCited, open:!u.meApplied||vfHasAnswerForReview(u.ev.evidence_id), settled:u.meApplied, myDec:u.myDec});
      }).join(''));
      rendered += batch.length;
      if (rendered < _list.length) {
        const more = document.createElement('button');
        more.type = 'button'; more.className = 'pill-btn';
        more.textContent = 'Show more findings (' + rendered + ' of ' + _list.length + ')';
        more.onclick = function() { more.remove(); showNextCards(); };
        host.appendChild(more);
      }
    }
    showNextCards();
    _vfSyncStickyBars();
  }

  // Active EV rows (not dropped/dataset/reviewer_ok) for a single source_id, scoped to the
  // current NbS, narrowed by scope: whole source | a single page | tabular-only quotes.
  // Paper-table number parsed from an evidence_id suffix (e.g. ev_texture_affan24_table4 -> "4").
  // Matches only "table"/"tbl" — NOT bare "t4" (that collides with the T4 recipe-table id).
  function _vfTableNo(eid){ var m=/(?:table|tbl)[ _]?(\d+)/i.exec(eid||''); return m?m[1]:''; }
  function _vfBulkRows(evAll, sid, scope){
    var nbs=(window._vfScope||{}).nbs||'all';
    return (evAll||[]).filter(function(e){
      if(e.source_id!==sid)return false;
      if(nbs!=='all'&&e.nbs_id!==nbs)return false;
      if(e.use_role==='dataset')return false;
      if(e.reviewer_ok===true||e.reviewer_ok==='true')return false;
      if(scope==='tabular')return _vfTabular(e.quote);
      if(scope==='page'){ var p=(window._vfBulkPage||'').trim(); return p!==''&&String(e.page||'')===p; }
      if(scope==='table'){ var t=(window._vfBulkTable||'').trim(); return t!==''&&_vfTableNo(e.evidence_id)===t; }
      return true;
    });
  }
  // "Flag a whole source at once" sidebar panel — flag every active record from one source
  // (so a bad source need not be reviewed entry-by-entry). Searchable source picker + chips
  // for the actual locations (pages / tables) present in that source. Sets your decisions;
  // Apply commits.
  function _vfRenderBulk(evAll){
    var box=document.getElementById('vf-bulk'); if(!box)return;
    var nbs=(window._vfScope||{}).nbs||'all';
    var bySrc={}; (evAll||[]).forEach(function(e){ if(nbs!=='all'&&e.nbs_id!==nbs)return; if(e.use_role==='dataset')return; if(e.reviewer_ok===true||e.reviewer_ok==='true')return; var s=e.source_id||'(none)'; bySrc[s]=(bySrc[s]||0)+1; });
    var srcs=Object.keys(bySrc).sort();
    if(!srcs.length){ box.innerHTML='<div style="font-size:10px; color:var(--text-muted);">No active source to flag in this scope.</div>'; return; }
    var cur=(window._vfBulkSrc&&bySrc[window._vfBulkSrc])?window._vfBulkSrc:srcs[0]; window._vfBulkSrc=cur;
    // Locations present in THIS source (structured): distinct pages + whether any tabular rows.
    var _rowsAll=_vfBulkRows(evAll,cur,'whole');
    var _pageCount={}; _rowsAll.forEach(function(r){ var p=String(r.page||''); if(p)_pageCount[p]=(_pageCount[p]||0)+1; });
    var _pages=Object.keys(_pageCount).sort(function(a,b){return (parseInt(a)||0)-(parseInt(b)||0);});
    var _tabCount=_rowsAll.filter(function(r){return _vfTabular(r.quote);}).length;
    // specific paper-tables present (from evidence_id) — lets you target Table 4 without also
    // catching other content on the same page.
    var _tblCount={}; _rowsAll.forEach(function(r){ var t=_vfTableNo(r.evidence_id); if(t)_tblCount[t]=(_tblCount[t]||0)+1; });
    var _tbls=Object.keys(_tblCount).sort(function(a,b){return (parseInt(a)||0)-(parseInt(b)||0);});
    var scope=window._vfBulkScope||'whole';
    if(scope==='page'&&_pages.indexOf(String(window._vfBulkPage||''))<0){ scope='whole'; window._vfBulkScope='whole'; window._vfBulkPage=''; }
    if(scope==='tabular'&&!_tabCount){ scope='whole'; window._vfBulkScope='whole'; }
    if(scope==='table'&&_tbls.indexOf(String(window._vfBulkTable||''))<0){ scope='whole'; window._vfBulkScope='whole'; window._vfBulkTable=''; }
    var n=_vfBulkRows(evAll,cur,scope).length;
    var dlopts=srcs.map(function(s){ return '<option value="'+vfEsc(s)+'">'+bySrc[s]+' record(s)</option>'; }).join('');
    var _chip=function(label,active,onclick){ return '<button class="pill-btn '+(active?'active sky':'')+'" onclick="'+onclick+'" style="font-size:10px; padding:3px 8px; border-radius:10px;">'+label+'</button>'; };
    var locChips=_chip('whole source ('+_rowsAll.length+')', scope==='whole', "window._vfBulkScope='whole'; window._vfBulkPage=''; window._vfBulkTable=''; renderVfWorklist();");
    if(_tabCount) locChips+=_chip('tables only ('+_tabCount+')', scope==='tabular', "window._vfBulkScope='tabular'; renderVfWorklist();");
    locChips+=_tbls.map(function(t){ return _chip('Table '+vfEsc(t)+' ('+_tblCount[t]+')', scope==='table'&&String(window._vfBulkTable)===t, "window._vfBulkScope='table'; window._vfBulkTable='"+vfEsc(t)+"'; renderVfWorklist();"); }).join('');
    locChips+=_pages.map(function(p){ return _chip('p.'+vfEsc(p)+' ('+_pageCount[p]+')', scope==='page'&&String(window._vfBulkPage)===p, "window._vfBulkScope='page'; window._vfBulkPage='"+vfEsc(p)+"'; renderVfWorklist();"); }).join('');
    box.innerHTML=''
      +'<div style="font-size:10px; color:var(--text-muted); text-transform:uppercase; letter-spacing:.04em; margin-bottom:2px;">&#9873; Flag a whole source at once</div>'
      +'<div style="font-size:9.5px; color:var(--text-muted); margin-bottom:6px; line-height:1.4;">Flag every active record from one paper (or one page / its tables) without reviewing each. Sets your decisions; Apply commits.</div>'
      +'<input list="vf-bulk-datalist" value="'+vfEsc(cur)+'" placeholder="type to search sources…" onchange="window._vfBulkSrc=this.value; window._vfBulkScope=\'whole\'; window._vfBulkPage=\'\'; window._vfBulkTable=\'\'; renderVfWorklist();" style="width:100%; box-sizing:border-box; font-size:11px; padding:5px; border-radius:4px; margin-bottom:6px; background:var(--bg-secondary); color:var(--text-primary); border:1px solid var(--border-color);">'
      +'<datalist id="vf-bulk-datalist">'+dlopts+'</datalist>'
      +'<div style="font-size:9px; color:var(--text-muted); margin-bottom:3px;">Location in this source:</div>'
      +'<div style="display:flex; gap:4px; flex-wrap:wrap; margin-bottom:6px;">'+locChips+'</div>'
      +'<select onchange="window._vfBulkReason=this.value;" title="coded reason — same set as the per-card reason selector" style="width:100%; box-sizing:border-box; font-size:11px; padding:5px 7px; border-radius:4px; margin-bottom:6px; background:var(--bg-secondary); color:var(--text-primary); border:1px solid var(--border-color);"><option value="">reason…</option>'+_VF_RC_FLAGGED.map(function(rc){return '<option value="'+rc+'" title="'+vfEsc(_VF_RC_DESC[rc]||'')+'"'+((window._vfBulkReason||'')===rc?' selected':'')+'>'+rc.replace(/_/g,' ')+'</option>';}).join('')+'</select>'
      +'<textarea rows="2" placeholder="note (required for &quot;other&quot;)" oninput="window._vfBulkNote=this.value;" style="width:100%; box-sizing:border-box; font-size:11px; padding:5px 7px; border-radius:4px; margin-bottom:6px; background:var(--bg-secondary); color:var(--text-primary); border:1px solid var(--border-color); resize:vertical; font-family:inherit;">'+vfEsc(window._vfBulkNote||'')+'</textarea>'
      +'<div style="font-size:10px; color:var(--text-secondary); margin-bottom:6px;">will flag <b id="vf-bulk-n">'+n+'</b> active record(s)</div>'
      +'<div style="display:flex; gap:6px;">'
        +'<button onclick="vfBulkFlag(\'drop\')" title="remove all matching records (soft-delete on Apply)" style="flex:1; font-size:11px; padding:6px; border-radius:4px; border:1px solid var(--accent-rose); background:transparent; color:var(--accent-rose); cursor:pointer;">&#9873; drop all</button>'
        +'<button onclick="vfBulkFlag(\'flag\')" title="tentatively keep all + raise for reconsideration" style="flex:1; font-size:11px; padding:6px; border-radius:4px; border:1px solid var(--accent-amber); background:transparent; color:var(--accent-amber); cursor:pointer;">&#9873; query all</button>'
      +'</div>';
  }
  function vfBulkFlag(decision){
    var sid=window._vfBulkSrc; var scope=window._vfBulkScope||'whole';
    var reason=(window._vfBulkReason||'').trim();
    var note=(window._vfBulkNote||'').trim();
    if(!reason){ alert('Pick a reason first — a bulk flag needs a coded reason (same set as the cards).'); return; }
    if(reason==='other'&&!note){ alert('Reason "other" needs a note explaining it.'); return; }
    var rows=_vfBulkRows(reviewData.registers.EV_evidence_register||[],sid,scope);
    if(!rows.length){ alert('No active records match that source/scope.'); return; }
    var verb=decision==='drop'?'DROP':'QUERY (tentatively keep + flag for reconsideration)';
    var where=scope==='page'?(' on page '+(window._vfBulkPage||'')):(scope==='tabular'?' (tabular records only)':(scope==='table'?(' from Table '+(window._vfBulkTable||'')):''));
    if(!confirm(verb+' all '+rows.length+' active record(s) from "'+sid+'"'+where+'?\n\nThis sets YOUR decision on each — review the queue, then Apply to commit.'))return;
    var me=(window._vfReviewer||'reviewer');
    if(!window._vfDecisions)window._vfDecisions={}; if(!window._vfReasons)window._vfReasons={}; if(!window._vfNotes)window._vfNotes={}; if(!window._vfAllReviews)window._vfAllReviews={};
    rows.forEach(function(e){ var id=e.evidence_id; window._vfDecisions[id]=decision; window._vfReasons[id]=reason; window._vfNotes[id]=note;
      window._vfAllReviews[id]=window._vfAllReviews[id]||{}; window._vfAllReviews[id][me]={decision:decision,reason:reason,note:note};
      if(window._reviewApi){ fetch('/api/decision',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({evidence_id:id,decision:decision,reason:reason,note:note,reviewer:me})}).catch(function(){}); }
    });
    localStorage.setItem('vfDecisions',JSON.stringify(window._vfDecisions));
    localStorage.setItem('vfReasons',JSON.stringify(window._vfReasons));
    localStorage.setItem('vfNotes',JSON.stringify(window._vfNotes));
    renderVfWorklist();
    alert('Flagged '+rows.length+' record(s) from "'+sid+'" as '+decision+'. Now Apply (action bar, top of the queue) to commit.');
  }


function startReviewWorkspace() {
    probeReviewApi();
    // Best-effort: load the committed-crop manifest so crops render for everyone (incl.
    // GitHub Pages) with zero setup. Falls back silently to an empty set if absent/offline.
    if(window._cropManifest===undefined){ window._cropManifest=new Set(); }
    if(window._cropSharePoint===undefined){ window._cropSharePoint=new Set(); }
    if(window._cropSharePointMap===undefined){ window._cropSharePointMap={}; }
    fetch('https://raw.githubusercontent.com/CIAT/nbs_ruralscan/'+(reviewData.revision || 'bec50bc0f9dc74b3d5ffafcf881571a8a8ec5c06')+'/docs/crops/manifest.json').then(function(r){return r.ok?r.json():null;}).then(function(j){ if(j&&Array.isArray(j.eids)){ window._cropManifest=new Set(j.eids); } if(j&&j.sharepoint&&typeof j.sharepoint==='object'){ window._cropSharePointMap=j.sharepoint; window._cropSharePoint=new Set(Object.keys(j.sharepoint)); } if(j&&(Array.isArray(j.eids)||j.sharepoint)){ if(typeof renderVfWorklist==='function' && window._vfMode){ try{renderVfWorklist();}catch(e){} } } }).catch(function(){});
}

function mountReviewWorkspace() {
    // The same controls stay in the sidebar on desktop and a disclosure on small screens.
    var filterPanel = document.getElementById('vf-sidebar-panel');
    var wideReview = window.matchMedia('(min-width: 1000px)');
    function sizeReviewFilters() { if (filterPanel) filterPanel.open = wideReview.matches; }
    sizeReviewFilters();
    wideReview.addEventListener('change', sizeReviewFilters);
    var guide = document.getElementById('review-reference-guide');
    ['vf-howto', 'vf-reason-codes'].forEach(function (id) { var item = document.getElementById(id); if (item) guide.appendChild(item); });
}

// Public lifecycle. Legacy card callbacks above remain global during this extraction.
window.ReviewWorkspace = (function () {
  let mounted = false;
  let buildKey = '';
  function updateBuild() {
    const host = document.getElementById('review-build');
    const manifest = document.getElementById('review-component-release');
    if (!host || !manifest) return;
    const release = JSON.parse(manifest.textContent);
    const revision = (typeof reviewData !== 'undefined' && reviewData && reviewData.registerRevision) || '';
    const key = release.content_sha256 + ':' + revision;
    if (buildKey === key) return;
    buildKey = key;
    const label = document.createElement('span');
    label.textContent = 'Review v' + release.version + ' · Evidence ';
    if (/^[0-9a-f]{40}$/.test(revision)) {
      const link = document.createElement('a');
      link.href = 'https://github.com/RuralScan/evidence/tree/' + revision;
      link.textContent = revision.slice(0, 8);
      link.title = 'Official evidence registers at ' + revision;
      label.append(link);
    } else {
      label.append(document.createTextNode('revision unavailable'));
    }
    const details = document.createElement('details');
    const summary = document.createElement('summary');
    summary.textContent = 'Review changes';
    details.append(summary);
    for (const item of [release, ...(release.history || [])]) {
      const entry = document.createElement('div');
      const title = document.createElement('b');
      title.textContent = 'v' + item.version + ' · ' + item.date;
      entry.append(title);
      const notes = document.createElement('p');
      notes.textContent = item.notes.join(' ');
      entry.append(notes);
      details.append(entry);
    }
    host.replaceChildren(label, details);
  }
  function onTab(tab) {
    const active = tab === 'tab-qaqc';
    const historicalFooter = document.querySelector('.meta-timestamp');
    if (historicalFooter) historicalFooter.hidden = active;
    updateBuild();
  }
  function mount() {
    if (mounted) return;
    mounted = true;
    mountReviewWorkspace();
    onTab(document.querySelector('.tab-content.active')?.id);
  }
  return { mount, onTab, updateBuild, start: startReviewWorkspace };
})();
