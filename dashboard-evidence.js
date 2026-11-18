/* Evidence section (tab 3): every retained finding, in plain words, from the official registers.
   Reads the registers the review queue already loads from RuralScan/evidence. Combines nothing:
   counts and ranges are descriptive, and each source is counted once per topic. */
(function () {
  'use strict';
  /* ---------- findings in plain words: built by fixed rules from the stored fields ---------- */
  const ROLE = {structural_suitability: 'w', nbs_effect: 'd', asset_vulnerability: 'h', operational_risk: 'o'};
  const DESIGN = {observational: 'Observational study', meta_analysis: 'Meta-analysis', quasi_experimental: 'Comparison study',
    model: 'Model result', review: 'Review', practitioner_rating: 'Practitioner rating', case_study: 'Case study',
    rct: 'Randomised trial', expert: 'Expert judgement'};
  const BASIS = {primary_measured: 'Measured by the study', primary_measurement: 'Measured by the study',
    expert_assertion: 'Stated by the authors', cited_secondary: 'Cited from another work', modelled: 'Model result',
    table: 'Taken from a table', figure_read: 'Read from a figure'};
  const UNIT = {percent: '%', degrees_celsius: '°C', degC: '°C', 'mm/year': 'mm a year', unitless: ''};
  // A finding answers the hazard-protection question when it states a hazard or measures one of these.
  const DIRECT_HAZARD = {drought_hazard: 'drought', flood_hazard: 'flood', fire_hazard: 'fire', wildfire_mitigation: 'fire',
    wind_cyclone_hazard: 'wind_cyclone', waterlogging_hazard: 'waterlogging', heat_stress_hazard: 'heat_stress'};
  const PRACTICE_LABEL = {water_harvesting_conservation: 'Water harvesting and conservation',
    wetland_management: 'Wetland management and restoration', riparian_buffer: 'Riparian buffers'};
  const SOURCE_KIND = {grey: 'report or guide, not peer reviewed', 'peer reviewed journal': 'peer-reviewed journal',
    stock: 'peer-reviewed journal', 'updated lit': 'peer-reviewed journal'};
  const COUNTRY = {"ABW":"Aruba","AFG":"Afghanistan","AGO":"Angola","AIA":"Anguilla","ALA":"Åland Islands","ALB":"Albania","AND":"Andorra","ARE":"United Arab Emirates","ARG":"Argentina","ARM":"Armenia","ASM":"American Samoa","ATA":"Antarctica","ATF":"French Southern Territories","ATG":"Antigua and Barbuda","AUS":"Australia","AUT":"Austria","AZE":"Azerbaijan","BDI":"Burundi","BEL":"Belgium","BEN":"Benin","BES":"Bonaire, Sint Eustatius and Saba","BFA":"Burkina Faso","BGD":"Bangladesh","BGR":"Bulgaria","BHR":"Bahrain","BHS":"Bahamas","BIH":"Bosnia and Herzegovina","BLM":"Saint Barthélemy","BLR":"Belarus","BLZ":"Belize","BMU":"Bermuda","BOL":"Bolivia","BRA":"Brazil","BRB":"Barbados","BRN":"Brunei Darussalam","BTN":"Bhutan","BVT":"Bouvet Island","BWA":"Botswana","CAF":"Central African Republic","CAN":"Canada","CCK":"Cocos (Keeling) Islands","CHE":"Switzerland","CHL":"Chile","CHN":"China","CIV":"Côte d'Ivoire","CMR":"Cameroon","COD":"Congo, The Democratic Republic of the","COG":"Congo","COK":"Cook Islands","COL":"Colombia","COM":"Comoros","CPV":"Cabo Verde","CRI":"Costa Rica","CUB":"Cuba","CUW":"Curaçao","CXR":"Christmas Island","CYM":"Cayman Islands","CYP":"Cyprus","CZE":"Czechia","DEU":"Germany","DJI":"Djibouti","DMA":"Dominica","DNK":"Denmark","DOM":"Dominican Republic","DZA":"Algeria","ECU":"Ecuador","EGY":"Egypt","ERI":"Eritrea","ESH":"Western Sahara","ESP":"Spain","EST":"Estonia","ETH":"Ethiopia","FIN":"Finland","FJI":"Fiji","FLK":"Falkland Islands (Malvinas)","FRA":"France","FRO":"Faroe Islands","FSM":"Micronesia, Federated States of","GAB":"Gabon","GBR":"United Kingdom","GEO":"Georgia","GGY":"Guernsey","GHA":"Ghana","GIB":"Gibraltar","GIN":"Guinea","GLP":"Guadeloupe","GMB":"Gambia","GNB":"Guinea-Bissau","GNQ":"Equatorial Guinea","GRC":"Greece","GRD":"Grenada","GRL":"Greenland","GTM":"Guatemala","GUF":"French Guiana","GUM":"Guam","GUY":"Guyana","HKG":"Hong Kong","HMD":"Heard Island and McDonald Islands","HND":"Honduras","HRV":"Croatia","HTI":"Haiti","HUN":"Hungary","IDN":"Indonesia","IMN":"Isle of Man","IND":"India","IOT":"British Indian Ocean Territory","IRL":"Ireland","IRN":"Iran","IRQ":"Iraq","ISL":"Iceland","ISR":"Israel","ITA":"Italy","JAM":"Jamaica","JEY":"Jersey","JOR":"Jordan","JPN":"Japan","KAZ":"Kazakhstan","KEN":"Kenya","KGZ":"Kyrgyzstan","KHM":"Cambodia","KIR":"Kiribati","KNA":"Saint Kitts and Nevis","KOR":"South Korea","KWT":"Kuwait","LAO":"Laos","LBN":"Lebanon","LBR":"Liberia","LBY":"Libya","LCA":"Saint Lucia","LIE":"Liechtenstein","LKA":"Sri Lanka","LSO":"Lesotho","LTU":"Lithuania","LUX":"Luxembourg","LVA":"Latvia","MAC":"Macao","MAF":"Saint Martin (French part)","MAR":"Morocco","MCO":"Monaco","MDA":"Moldova","MDG":"Madagascar","MDV":"Maldives","MEX":"Mexico","MHL":"Marshall Islands","MKD":"North Macedonia","MLI":"Mali","MLT":"Malta","MMR":"Myanmar","MNE":"Montenegro","MNG":"Mongolia","MNP":"Northern Mariana Islands","MOZ":"Mozambique","MRT":"Mauritania","MSR":"Montserrat","MTQ":"Martinique","MUS":"Mauritius","MWI":"Malawi","MYS":"Malaysia","MYT":"Mayotte","NAM":"Namibia","NCL":"New Caledonia","NER":"Niger","NFK":"Norfolk Island","NGA":"Nigeria","NIC":"Nicaragua","NIU":"Niue","NLD":"Netherlands","NOR":"Norway","NPL":"Nepal","NRU":"Nauru","NZL":"New Zealand","OMN":"Oman","PAK":"Pakistan","PAN":"Panama","PCN":"Pitcairn","PER":"Peru","PHL":"Philippines","PLW":"Palau","PNG":"Papua New Guinea","POL":"Poland","PRI":"Puerto Rico","PRK":"North Korea","PRT":"Portugal","PRY":"Paraguay","PSE":"Palestine, State of","PYF":"French Polynesia","QAT":"Qatar","REU":"Réunion","ROU":"Romania","RUS":"Russian Federation","RWA":"Rwanda","SAU":"Saudi Arabia","SDN":"Sudan","SEN":"Senegal","SGP":"Singapore","SGS":"South Georgia and the South Sandwich Islands","SHN":"Saint Helena, Ascension and Tristan da Cunha","SJM":"Svalbard and Jan Mayen","SLB":"Solomon Islands","SLE":"Sierra Leone","SLV":"El Salvador","SMR":"San Marino","SOM":"Somalia","SPM":"Saint Pierre and Miquelon","SRB":"Serbia","SSD":"South Sudan","STP":"Sao Tome and Principe","SUR":"Suriname","SVK":"Slovakia","SVN":"Slovenia","SWE":"Sweden","SWZ":"Eswatini","SXM":"Sint Maarten (Dutch part)","SYC":"Seychelles","SYR":"Syria","TCA":"Turks and Caicos Islands","TCD":"Chad","TGO":"Togo","THA":"Thailand","TJK":"Tajikistan","TKL":"Tokelau","TKM":"Turkmenistan","TLS":"Timor-Leste","TON":"Tonga","TTO":"Trinidad and Tobago","TUN":"Tunisia","TUR":"Turkey","TUV":"Tuvalu","TWN":"Taiwan","TZA":"Tanzania","UGA":"Uganda","UKR":"Ukraine","UMI":"United States Minor Outlying Islands","URY":"Uruguay","USA":"United States","UZB":"Uzbekistan","VAT":"Holy See (Vatican City State)","VCT":"Saint Vincent and the Grenadines","VEN":"Venezuela","VGB":"Virgin Islands, British","VIR":"Virgin Islands, U.S.","VNM":"Vietnam","VUT":"Vanuatu","WLF":"Wallis and Futuna","WSM":"Samoa","YEM":"Yemen","ZAF":"South Africa","ZMB":"Zambia","ZWE":"Zimbabwe"};

  const obj = v => {
    if (v && typeof v === 'object' && !Array.isArray(v)) return v;
    if (typeof v !== 'string' || !v) return {};
    try { const o = JSON.parse(v); return o && typeof o === 'object' && !Array.isArray(o) ? o : {note: String(o)}; }
    catch (e) { return {note: v}; }
  };
  const has = (o, k) => Object.prototype.hasOwnProperty.call(o, k);
  const pick = (o, ...keys) => { for (const k of keys) if (has(o, k)) return o[k]; };
  const num = x => {
    if (x === null || x === undefined || x === '' || typeof x === 'boolean') return null;
    const f = Number(x);
    return Number.isFinite(f) ? Math.round(f * 1000) / 1000 : null;
  };
  const fmt = x => { const n = num(x); return n === null ? String(x) : Math.abs(n) >= 10000 ? n.toLocaleString('en') : String(n); };
  const unit = u => {
    if (!u) return '';
    if (has(UNIT, u)) return UNIT[u];
    return String(u).replace(/usd/g, 'US$').replace(/eur/g, 'EUR').replace(/_per_/g, ' per ').replace(/_/g, ' ').replace(/ yr\b/g, ' year');
  };
  const span = (lo, hi, u) => {
    u = unit(u);
    const gap = u === '%' || u === '°C' || u === '' ? '' : ' ';
    const a = lo === null || lo === undefined ? null : fmt(lo), b = hi === null || hi === undefined ? null : fmt(hi);
    if (a && b && a !== b) return `${a} to ${b}${gap}${u}`;
    if (a && b) return `${a}${gap}${u}`;
    if (a) return `at least ${a}${gap}${u}`;
    if (b) return `up to ${b}${gap}${u}`;
    return '';
  };
  const cap = s => { s = String(s).trim(); return s.slice(0, 1).toUpperCase() + s.slice(1); };
  const low = s => (s.slice(0, 2).toUpperCase() !== s.slice(0, 2) ? s.slice(0, 1).toLowerCase() + s.slice(1) : s);
  const clip = (s, n) => {
    s = String(s === null || s === undefined ? '' : s).replace(/\s+/g, ' ').trim();
    if (s.length <= n) return s;
    const cut = s.slice(0, n - 1);
    return cut.slice(0, cut.lastIndexOf(' ') > 0 ? cut.lastIndexOf(' ') : cut.length) + ' …';
  };
  const stop = s => (String(s).trimEnd().endsWith('.') ? '' : '.');
  const pretty = id => cap(String(id || '').replace(/_/g, ' '));

  function whereSentence(lab, rel) {
    const u = rel.unit, classes = rel.observed_classes;
    if (rel.type === 'observed_presence' || (Array.isArray(classes) && classes.length) || num(rel.observed_min) !== null) {
      let range = span(num(rel.observed_min), num(rel.observed_max), u);
      if (!range && Array.isArray(classes) && classes.length) range = classes.slice(0, 4).map(String).join('; ');
      if (range) return [`One documented case: in use where ${lab} is ${range}.`, 'One case, not a limit'];
    }
    const lo = num(pick(rel, 'abs_min', 'lower')), hi = num(pick(rel, 'abs_max', 'upper'));
    const bestLo = num(rel.opt_low), bestHi = num(rel.opt_high);
    if (lo !== null || hi !== null) {
      let text = `Reported range: ${lab} ${span(lo, hi, u)}`;
      if (bestLo !== null || bestHi !== null) text += `; best at ${span(bestLo, bestHi, u)}`;
      return [text + '.', 'Range given by the source'];
    }
    if (bestLo !== null || bestHi !== null) return [`Reported as best where ${lab} is ${span(bestLo, bestHi, u)}.`, 'Best range given by the source'];
    for (const [key, lead] of [['included_classes', 'Classes named as suitable'], ['classes', 'Classes used by the source'], ['excluded_classes', 'Classes named as unsuitable']]) {
      const val = rel[key];
      if (Array.isArray(val) && val.length) {
        const names = val.slice(0, 5).map(c => String(c && typeof c === 'object' ? (has(c, 'class') ? c.class : JSON.stringify(c)) : c)).join('; ');
        return [`${lead} for ${lab}: ${clip(names, 150)}.`, 'Classes given by the source'];
      }
    }
    const weight = pick(rel, 'mcda_weight', 'weight');
    if (num(weight) !== null) return [`The source's own siting model gives ${lab} a weight of ${fmt(weight)}.`, "A weight in the source's model"];
    const d = String(rel.direction || rel.note || '');
    if (['increasing', 'decreasing', 'positive', 'negative'].includes(d)) {
      return [`The source reports that suitability ${d === 'increasing' || d === 'positive' ? 'rises' : 'falls'} as ${lab} increases. No limits are given.`, 'Direction only'];
    }
    if (d.length > 30) return [cap(clip(d, 230)) + stop(d), 'Condition described by the source'];
    return [`${cap(lab)}: no plain summary is recorded for this finding. Read the source's words.`, 'No summary'];
  }

  function sizeText(rel) {
    const m = rel.metric, u = rel.unit;
    const mag = num(rel.magnitude), lo = num(rel.magnitude_low), hi = num(rel.magnitude_high);
    if (m === 'pct_change' || u === 'percent') {
      if (lo !== null && hi !== null) return `by ${fmt(Math.abs(lo))} to ${fmt(Math.abs(hi))}%`;
      if (mag !== null) return `by ${fmt(Math.abs(mag))}%`;
    }
    if ((m === 'contrast' || m === 'complete_contrast') && num(rel.value_with) !== null) {
      return `${fmt(rel.value_with)} with the practice against ${fmt(rel.value_without)} without (${unit(u)})`.replace(' ()', '');
    }
    if (u === 'fold_change' && mag !== null) return `${fmt(mag)} times`;
    if (m === 'ordinal_rating' && rel.source_scale_value) {
      const val = String(rel.source_scale_value).replace(/_/g, ' ');
      return /^[+-]?\d$/.test(val) ? `practitioner rating ${val} on a scale of -3 to +3` : `practitioners say it copes “${val}”`;
    }
    if (m === 'absolute' && (mag !== null || lo !== null)) return 'reported value ' + span(mag !== null ? mag : lo, mag === null ? hi : mag, u);
    return '';
  }

  function effectSentence(lab, rel, sense) {
    const d = String(rel.direction || ''), size = sizeText(rel);
    if (rel.metric === 'absolute' && !sense) return [`${lab}: ${size || 'value reported'}.`, ''];
    if ((d === 'positive' || d === 'negative') && sense) {
      if (rel.metric === 'absolute' && size) return [`${lab}: ${size}.`, ''];
      const good = (sense.high_is === 'good') === (d === 'positive');
      const tag = sense.high_is === 'good' || sense.high_is === 'bad' ? (good ? 'Benefit' : 'Harm') : '';
      let text = cap(d === 'positive' ? sense.positive_means : sense.negative_means);
      if (size) text += (size.startsWith('practitioner') || size.startsWith('reported') || size.includes(' with the practice') ? ': ' : ' ') + size;
      return [text + '.', tag];
    }
    if (d === 'none') return [`No clear change in ${low(lab)}.`, 'No change'];
    if (d === 'positive' || d === 'negative') return [`${lab} went ${d === 'positive' ? 'up' : 'down'}${size ? ' ' + size : ''}.`, ''];
    const raw = String(rel.outcome_raw || d || '');
    return [raw ? cap(clip(raw, 200)) + stop(raw) : `${lab}: see the source's words.`, ''];
  }

  function buildModel(registers, lookups) {
    const srcRows = new Map((registers.SRC_source_register || []).map(r => [r.source_id, r]));
    const vont = new Map((lookups.vont || registers.VONT_variable_ontology || []).map(r => [r.canonical_variable_id, r]));
    const sense = new Map((lookups.sense || []).map(r => [r.variable, r]));
    const famRows = lookups.fam || registers.FAM_family_registry || [];
    const ev = (registers.EV_evidence_register || []).filter(r => (r.review_state || '') !== 'dropped' && ROLE[r.use_role] && srcRows.has(r.source_id));
    const label = v => ((vont.get(v) || {}).label || String(v || '').replace(/_/g, ' ')).trim();
    const hazardName = h => { h = String(h || '').replace(/_/g, ' '); return h === 'wind cyclone' ? 'wind or cyclone' : h; };
    const crossOf = {};
    ev.forEach(r => { if (/__cross_family$/.test(r.suitability_family_id || '')) crossOf[r.nbs_id] = r.suitability_family_id; });

    const sources = [], sourceIndex = new Map();
    const sourceOf = id => {
      if (sourceIndex.has(id)) return sourceIndex.get(id);
      const s = srcRows.get(id), cit = String(s.citation || id).replace(/\s+/g, ' ').trim();
      const m = cit.match(/^(.*?)\s*\((\d{4})[a-z]?\)/);
      let short = clip(cit, 40), year = '';
      if (m) {
        const first = m[1].split(/,|;| et al| and | & /)[0].trim();
        year = m[2];
        // A citation that opens with its year has no author to shorten to.
        if (first) short = `${first}${/et al|,.*,|;| and | & /.test(m[1]) ? ' et al.' : ''} (${m[2]})`;
      }
      const doi = String(s.doi || '');
      let kind = String(s.venue_type || s.source_category || s.method_type || '').replace(/_/g, ' ');
      kind = SOURCE_KIND[kind] || kind;
      sources.push({id, s: short, c: cit, y: year, l: s.url || (doi.startsWith('10.') ? 'https://doi.org/' + doi : ''), k: cap(kind), t: s.benchmark_tier || ''});
      sourceIndex.set(id, sources.length - 1);
      return sources.length - 1;
    };
    const countries = (ctx, s) => {
      const c = ctx.country || ctx.study_country || s.study_country || '';
      const out = [];
      (Array.isArray(c) ? c : String(c).split(/[|;,]/)).forEach(item => {
        item = String(item).trim();
        if (!item) return;
        if (/^[A-Z]{3}$/.test(item)) item = COUNTRY[item] || item;
        if (item === 'DRC') item = COUNTRY.COD || item;
        if (!out.includes(item)) out.push(item);
      });
      return out;
    };

    const findings = ev.map(r => {
      const rel = obj(r.relationship), ctx = obj(r.context), s = srcRows.get(r.source_id);
      let role = ROLE[r.use_role], text, tag = '';
      const lab = label(r.variable);
      if (role === 'w') [text, tag] = whereSentence(low(lab), rel);
      else if (role === 'd') [text, tag] = effectSentence(lab, rel, sense.get(r.variable));
      else if (role === 'h') {
        const raw = String(rel.outcome_raw || rel.direction || '').replace(/^WOCAT QT 6\.3:\s*/, '').replace('the Technology', 'the practice');
        text = `Under ${hazardName(ctx.hazard_type || 'hazard')}: ${clip(raw, 210)}${stop(raw)}`;
        const rating = String(rel.source_scale_value || ''), d = String(rel.direction), sn = sense.get(r.variable);
        if (rating === 'very well' || rating === 'well' || d === 'none') tag = 'Copes well';
        else if (rating === 'moderately') tag = 'Copes partly';
        else if (rating.startsWith('not well')) tag = 'Damage reported';
        else if ((d === 'positive' || d === 'negative') && sn && (sn.high_is === 'good' || sn.high_is === 'bad')) {
          tag = (sn.high_is === 'bad') === (d === 'positive') ? 'Damage reported' : 'Copes well';
        }
      } else {
        let raw = String(rel.outcome_raw || '');
        if (raw.length < 20) raw = String(rel.direction || rel.note || raw);
        if (raw.length < 20 || ['positive', 'negative', 'none'].includes(raw)) {
          text = `${lab}: no plain summary is recorded for this finding. Read the source's words.`;
          tag = 'No summary';
        } else text = cap(clip(raw, 230)) + stop(raw);
        if (String(rel.direction) === 'none') tag = 'No link found';
      }
      const page = r.page || r.locator || '';
      const stored = v => (typeof v === 'string' ? v : v === null || v === undefined ? '' : JSON.stringify(v));
      const item = {
        i: r.evidence_id, s: sourceOf(r.source_id), p: r.nbs_id, f: r.suitability_family_id || '', r: role, v: r.variable,
        t: text, g: tag, m: role === 'd' ? clip(rel.outcome_raw || '', 260) : '', q: String(r.quote || '').replace(/\s+/g, ' ').trim(),
        pg: r.locator_type === 'page' && page ? 'p. ' + page : clip(r.locator || page, 80), c: countries(ctx, s),
        d: DESIGN[rel.design] || BASIS[r.claim_basis] || '', k: r.reviewer_ok === true || r.reviewer_ok === 'true' ? 1 : 0,
        dir: {positive: 1, negative: -1, none: 0}[String(rel.direction)], x: stored(r.relationship), y: stored(r.context),
      };
      if (role === 'w' && rel.unit) {
        const lo = num(pick(rel, 'abs_min', 'lower', 'observed_min', 'opt_low')), hi = num(pick(rel, 'abs_max', 'upper', 'observed_max', 'opt_high'));
        if (lo !== null || hi !== null) { item.lo = lo; item.hi = hi; item.u = unit(rel.unit); }
      }
      if (role === 'w' && Array.isArray(rel.observed_classes)) item.cl = rel.observed_classes.slice(0, 4).map(c => clip(c, 40));
      if (role === 'h') item.v = 'hz:' + hazardName(ctx.hazard_type || 'hazard');
      if (role === 'd') {
        const hazard = hazardName(ctx.hazard_type || DIRECT_HAZARD[r.variable] || '');
        if (hazard) { item.r = 'p'; item.ov = r.variable; item.v = 'hz:' + hazard; }
        if (rel.metric === 'pct_change') {
          const mag = num(rel.magnitude), lo = num(rel.magnitude_low), hi = num(rel.magnitude_high);
          const val = mag !== null ? mag : lo !== null && hi !== null ? (lo + hi) / 2 : null;
          const sign = {positive: 1, negative: -1}[String(rel.direction)];
          if (val !== null) item.pc = Math.round((sign ? Math.abs(val) * sign : val) * 10) / 10;
        }
      }
      if (item.f === 'cross_family' && crossOf[r.nbs_id]) item.f = crossOf[r.nbs_id];
      if (ctx.practice_as_described) item.pa = clip(ctx.practice_as_described, 320);
      return item;
    });

    const families = {};
    famRows.forEach(f => {
      const d = families[f.suitability_family_id] || (families[f.suitability_family_id] = {p: f.nbs_id, n: []});
      d.n.push(f.name);
    });
    findings.forEach(f => { if (!families[f.f]) families[f.f] = {p: f.p, n: []}; });
    Object.entries(families).forEach(([id, d]) => {
      const tail = id ? id.split('__').slice(1).join('__') || id : 'not assigned';
      d.l = tail === 'cross_family' ? 'Across sub-practices' : pretty(tail);
    });
    const variables = {}, practices = {};
    findings.forEach(f => {
      [f.v, f.ov].forEach(v => { if (v && !variables[v]) variables[v] = v.startsWith('hz:') ? cap(v.slice(3)) : label(v); });
      if (!practices[f.p]) practices[f.p] = PRACTICE_LABEL[f.p] || pretty(f.p);
    });
    const ordered = {};
    Object.keys(practices).sort((a, b) => practices[a].localeCompare(practices[b])).forEach(k => { ordered[k] = practices[k]; });
    return {findings, sources, families, variables, practices: ordered};
  }
  /* ---------- small CSV reader and a zip writer (stored, no compression) ---------- */
  function parseCsv(text) {
    const rows = []; let row = [], cell = '', quoted = false;
    for (let i = 0; i < text.length; i++) {
      const ch = text[i];
      if (quoted) {
        if (ch === '"') { if (text[i + 1] === '"') { cell += '"'; i++; } else quoted = false; }
        else cell += ch;
      } else if (ch === '"') quoted = true;
      else if (ch === ',') { row.push(cell); cell = ''; }
      else if (ch === '\n' || ch === '\r') {
        if (ch === '\r' && text[i + 1] === '\n') i++;
        row.push(cell); cell = ''; rows.push(row); row = [];
      } else cell += ch;
    }
    if (cell !== '' || row.length) { row.push(cell); rows.push(row); }
    const header = rows.shift() || [];
    return rows.filter(r => r.length > 1 || r[0] !== '').map(r => Object.fromEntries(header.map((h, i) => [h, r[i] === undefined ? '' : r[i]])));
  }
  const toCsv = (header, rows) => [header, ...rows].map(r => r.map(v => '"' + String(v === null || v === undefined ? '' : v).replace(/"/g, '""') + '"').join(',')).join('\r\n') + '\r\n';
  let crcTable;
  function crc32(bytes) {
    if (!crcTable) { crcTable = new Uint32Array(256); for (let n = 0; n < 256; n++) { let c = n; for (let k = 0; k < 8; k++) c = c & 1 ? 0xEDB88320 ^ (c >>> 1) : c >>> 1; crcTable[n] = c >>> 0; } }
    let crc = 0xFFFFFFFF;
    for (let i = 0; i < bytes.length; i++) crc = crcTable[(crc ^ bytes[i]) & 0xFF] ^ (crc >>> 8);
    return (crc ^ 0xFFFFFFFF) >>> 0;
  }
  function zip(files) {
    const enc = new TextEncoder(), parts = [], central = []; let offset = 0;
    const u16 = n => [n & 255, (n >>> 8) & 255], u32 = n => [n & 255, (n >>> 8) & 255, (n >>> 16) & 255, (n >>> 24) & 255];
    files.forEach(([name, text]) => {
      const nameBytes = enc.encode(name), data = typeof text === 'string' ? enc.encode(text) : text, crc = crc32(data);
      const common = [...u16(20), ...u16(0x0800), ...u16(0), ...u16(0), ...u16(0x21), ...u32(crc), ...u32(data.length), ...u32(data.length), ...u16(nameBytes.length), ...u16(0)];
      const local = new Uint8Array([0x50, 0x4B, 3, 4, ...common]);
      parts.push(local, nameBytes, data);
      central.push(new Uint8Array([0x50, 0x4B, 1, 2, ...u16(20), ...common, ...u16(0), ...u16(0), ...u16(0), ...u32(0), ...u32(offset)]), nameBytes);
      offset += local.length + nameBytes.length + data.length;
    });
    const size = central.reduce((n, p) => n + p.length, 0);
    const end = new Uint8Array([0x50, 0x4B, 5, 6, ...u16(0), ...u16(0), ...u16(files.length), ...u16(files.length), ...u32(size), ...u32(offset), ...u16(0)]);
    return new Blob([...parts, ...central, end], {type: 'application/zip'});
  }

  const RAW = 'https://raw.githubusercontent.com/RuralScan/evidence/';
  const REGISTER_FILES = ['EV_evidence_register', 'SRC_source_register', 'SRCH_search_register', 'VONT_variable_ontology', 'FAM_family_registry'];
  const text = async url => { const r = await fetch(url); if (!r.ok) throw Error(url); return r.text(); };
  const MARKUP = "<div class=\"ev-top\"><p id=\"ev-how\">Choose a practice and a question. Each question can be shown two ways: <strong>how much evidence</strong> there is for each sub-practice and topic, or <strong>what the evidence says</strong>, topic by topic, down to the single finding.</p>\n<div class=\"tools\"><div class=\"tcol\"><button class=\"btn ghost\" id=\"ev-find\" aria-pressed=\"false\">Search all findings</button><a href=\"#evidence\" id=\"ev-b-back\" hidden>← Back to practice and question</a></div><button class=\"btn\" id=\"ev-zip\">Download all evidence <small>(.zip)</small></button></div></div>\n<p class=\"small\" id=\"ev-zip-note\" hidden></p>\n<section class=\"panel on\" id=\"ev-p-e\">\n<div class=\"steps\"><label class=\"f\"><span>Practice</span><select id=\"ev-e-p\"></select></label></div>\n<label class=\"f\" style=\"margin-top:18px\"><span>Question</span></label>\n<div class=\"qs\" id=\"ev-e-q\"></div>\n<p class=\"feeds\" id=\"ev-e-link\"></p>\n<div class=\"viewbar\">\n<div><span class=\"vl\">Show</span><div class=\"seg\" id=\"ev-e-view\" role=\"group\" aria-label=\"View\"><button data-view=\"map\">How much evidence</button><button data-view=\"says\">What the evidence says</button></div></div>\n<label class=\"f\" id=\"ev-e-fwrap\"><span>Sub-practice</span><select id=\"ev-e-f\"></select></label>\n</div>\n<p class=\"hint\" id=\"ev-e-hint\"></p>\n<div id=\"ev-e-map\"></div>\n<div id=\"ev-e-cell\"></div>\n<div id=\"ev-e-out\"></div>\n<div id=\"ev-e-about\"></div>\n</section>\n<section class=\"panel\" id=\"ev-p-b\">\n<div class=\"cols\">\n<aside id=\"ev-b-facets\"></aside>\n<div>\n<div class=\"bar\"><input type=\"search\" id=\"ev-b-text\" placeholder=\"Search findings, the sources' words and citations\" aria-label=\"Search the evidence\">\n<button class=\"btn ghost\" id=\"ev-b-csv\">Download these findings <small>(.csv)</small></button></div>\n<p class=\"count\" id=\"ev-b-count\"></p>\n<div id=\"ev-b-out\"></div>\n<div id=\"ev-b-about\"></div>\n</div>\n</div>\n</section>";
  let root, current = null, mounted = null;

  async function downloadAll(model, revision) {
    const note = document.getElementById('ev-zip-note'), Q = QUESTIONS;
    note.hidden = false; note.textContent = 'Preparing the download…';
    const files = [];
    files.push(['findings.csv', toCsv(
      ['finding_id', 'practice', 'sub_practice', 'question', 'topic', 'plain_sentence', 'label', 'source_words', 'page', 'source_id', 'citation', 'link', 'countries', 'study_type', 'reviewed'],
      model.findings.map(f => [f.i, model.practices[f.p], (model.families[f.f] || {}).l || f.f, Q[f.r], model.variables[f.ov || f.v], f.t, f.g, f.q, f.pg, model.sources[f.s].id, model.sources[f.s].c, model.sources[f.s].l, f.c.join('; '), f.d, f.k ? 'checked by a reviewer' : 'not yet checked']))]);
    let registers = 'The register files could not be added: the register revision was not available.';
    if (revision) {
      try {
        const loaded = await Promise.all(REGISTER_FILES.map(n => text(RAW + revision + '/registers/schema/registers/' + n + '.csv')));
        REGISTER_FILES.forEach((n, i) => files.push(['registers/' + n + '.csv', loaded[i]]));
        registers = 'registers/ holds the official registers exactly as stored at that revision, including findings that reviewers dropped (review_state = dropped).';
      } catch (e) { registers = 'The register files could not be fetched. Get them from https://github.com/RuralScan/evidence.'; }
    }
    files.push(['README.txt', [
      'Rural NbS Scan: evidence base', '',
      'Source: https://github.com/RuralScan/evidence' + (revision ? ' at revision ' + revision : ''),
      'Downloaded: ' + new Date().toISOString().slice(0, 10), '',
      'findings.csv holds one row for each retained finding (' + model.findings.length + ' rows from ' + model.sources.length + ' sources).',
      'plain_sentence is built by fixed rules from the stored fields. It is a reading aid, not the record.',
      'source_words is the quotation taken from the source, at the page given.',
      'reviewed says whether a reviewer has checked the finding against its source.',
      registers, '',
      'Field guide: https://ruralscan.github.io/method/reference/data-guide.html',
      'Reuse terms: see the evidence repository.', ''].join('\r\n')]);
    const a = document.createElement('a');
    a.href = URL.createObjectURL(zip(files));
    a.download = 'rural-nbs-scan-evidence-' + (revision ? revision.slice(0, 8) : new Date().toISOString().slice(0, 10)) + '.zip';
    a.click();
    setTimeout(() => URL.revokeObjectURL(a.href), 60000);
    note.textContent = 'Downloaded ' + files.length + ' files. ' + registers;
  }

  const QUESTIONS = {w: 'Where can it work?', p: 'Does it protect people from climate hazards?', d: 'What else does it deliver?', h: 'What can damage it?', o: 'What helps or hinders putting it in place?'};

  function mount(model, revision) {
    root.innerHTML = MARKUP;
    const F = model.findings, SRC = model.sources, FAM = model.families, VAR = model.variables, PR = model.practices;
    const Q={w:['Where can it work?','Site conditions the sources report'],p:['Does it protect people from climate hazards?','Effects under drought, flood, heat, fire, wind'],d:['What else does it deliver?','Yield, income, soil, water, carbon, nature, cost'],h:['What can damage it?','Hazards to the works themselves'],o:['What helps or hinders putting it in place?','Labour, tenure, finance, markets']};
    const REF='reference/';
    const FEED={w:['the suitability rules','table-T4.html','Suitability rules (T4)','ch-m1-suitability.html','Step 1, Suitability'],
      p:['the ratings of how far a practice protects livelihoods from each hazard','table-T3.html','Hazard responses (T3)','ch-m2-climate-risk.html','Step 2, Rural climate risk'],
      d:['the benefit ratings on the scorecard, and the cost profiles','table-T6.html','Scorecard effects (T6)','ch-m5-scorecard.html','Step 5, Scorecard'],
      h:['the ratings of how badly each hazard threatens the investment','table-T3.html','Hazard responses (T3)','ch-m2b-project-risk.html','Step 2b, Project risk screen'],
      o:['the checks on enabling conditions and the hand-off guidance. No rule table is built from them','','','ch-m2b-project-risk.html','Step 2b, Project risk screen']};
    const feeds=q=>{const f=FEED[q];return`<b>In the method:</b> these findings are the basis of ${f[0]}. ${f[1]?`<a href="${REF+f[1]}" target="_blank" rel="noopener">${f[2]} ↗</a> · `:''}<a href="${REF+f[3]}" target="_blank" rel="noopener">${f[4]} ↗</a>${q==='o'?` · <a href="${REF}ch-m6-handoff.html" target="_blank" rel="noopener">Step 6, Hand-off ↗</a>`:''}${q==='d'?` · <a href="${REF}table-T6E.html" target="_blank" rel="noopener">Cost profiles (T6E) ↗</a>`:''}`};
    const $=id=>document.getElementById('ev-'+id);
    const esc=s=>String(s??'').replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
    const nf=n=>n.toLocaleString('en');
    const uniq=(items,fn)=>new Set(items.map(fn)).size;
    const where=f=>f.c.length?f.c.slice(0,2).join(', ')+(f.c.length>2?` +${f.c.length-2}`:''):'';
    F.forEach(f=>{f._h=(f.t+' '+f.q+' '+SRC[f.s].c+' '+VAR[f.v]+' '+(f.ov?VAR[f.ov]:'')).toLowerCase()});
    const rank=f=>(f.k?0:2)+(f.g==='No summary'?4:0);
    const sorted=items=>[...items].sort((a,b)=>rank(a)-rank(b)||(SRC[b.s].y||0)-(SRC[a.s].y||0));
    const TC={Benefit:'b',Harm:'h','No change':'z','No summary':'ns','Copes well':'b','Copes partly':'z','Damage reported':'h',Helps:'b',Hinders:'h','No link found':'z'};
    function tag(f){if(!f.g)return'';const guess=f.r==='o'&&(f.g==='Helps'||f.g==='Hinders');return`<span class="tag ${TC[f.g]||''}${guess?' q':''}" ${guess?'title="Sorted by keyword for this mock-up. Not a recorded field."':''}>${guess?'≈ ':''}${esc(f.g)}</span>`}
    function detail(f){const s=SRC[f.s];return`<div class="det"><div>
    <h4>In the source's words</h4><blockquote>“${esc(f.q)}”</blockquote><p class="small">${esc(f.pg||'Page not recorded')}</p>
    ${f.m?`<h4>What was measured</h4><p>${esc(f.m)}</p>`:''}
    ${f.pa?`<h4>The practice, as the source describes it</h4><p>${esc(f.pa)}</p>`:''}</div><div>
    <h4>Source</h4><p>${esc(s.c)} ${s.l?`<a href="${esc(s.l)}" target="_blank" rel="noopener">Open the source ↗</a>`:''}</p>
    <h4>Where and how</h4><p>${esc([f.c.join(', ')||'Country not recorded',f.d,s.k].filter(Boolean).join(' · '))}</p>
    <h4>Review</h4><p>${f.k?'A reviewer has checked this finding against the source.':'Not yet checked by a reviewer. Treat as provisional.'} <a href="#review-evidence=${encodeURIComponent(f.i)}">Open in the review queue</a></p></div>
    <details class="raw"><summary>Show the record as stored</summary><pre>finding      ${esc(f.i)}
    topic        ${esc(f.v)}
    sub-practice ${esc(f.f)}
    relationship ${esc(f.x||'(empty)')}
    context      ${esc(f.y||'(empty)')}</pre></details></div>`}
    function table(el,items,opt={}){const cols=opt.topic===false?5:6;let n=opt.n||15;items=sorted(items);const per=new Map();items.forEach(f=>per.set(f.s,(per.get(f.s)||0)+1));
      if(opt.group){const first=new Map();items.forEach((f,i)=>first.has(f.s)||first.set(f.s,i));items=[...items].sort((a,b)=>first.get(a.s)-first.get(b.s))}
      const draw=()=>{el.innerHTML=`<table><thead><tr><th>Finding</th>${opt.topic===false?'':`<th>${opt.topicLabel||'Topic'}</th>`}<th>Source</th><th>Where</th><th>Study type</th><th>Reviewed</th></tr></thead><tbody>${items.slice(0,n).map((f,i)=>`${opt.group&&per.get(f.s)>1&&(i===0||items[i-1].s!==f.s)?`<tr class="grp"><td colspan="${cols}"><b>${esc(SRC[f.s].s)}</b> · ${per.get(f.s)} findings from this one source</td></tr>`:''}<tr class="row" data-i="${i}"><td><span class="sent">${esc(f.t)}</span>${tag(f)}</td>${opt.topic===false?'':`<td class="muted">${esc(VAR[opt.topicLabel?f.ov||f.v:f.v])}</td>`}<td class="muted" style="white-space:nowrap">${esc(SRC[f.s].s)}</td><td class="muted">${esc(where(f))}</td><td class="muted">${esc(f.d)}</td><td><span class="chk ${f.k?'ok':''}">${f.k?'✓ Checked':'Not yet'}</span></td></tr>`).join('')}</tbody></table>${items.length>n?`<button class="more">Show 15 more (${nf(items.length-n)} left)</button>`:''}`};
      draw();
      el.onclick=e=>{if(e.target.closest('.more')){n+=15;draw();return}const tr=e.target.closest('tr.row');if(!tr||e.target.closest('a'))return;
        if(tr.classList.toggle('open')){const x=document.createElement('tr');x.className='exp';x.innerHTML=`<td colspan="${cols}">${detail(items[+tr.dataset.i])}</td>`;tr.after(x)}else tr.nextElementSibling.remove()}}
    function about(el,items){const top=(fn,k=7)=>{const m=new Map();items.forEach(f=>[].concat(fn(f)).forEach(v=>v&&m.set(v,(m.get(v)||0)+1)));return[...m].sort((a,b)=>b[1]-a[1]).slice(0,k)};
      const t=(title,rows)=>{const mx=Math.max(1,...rows.map(r=>r[1]));return`<table><caption>${title}</caption><tbody>${rows.map(r=>`<tr><td>${esc(r[0])}</td><td class="n"><span class="m" style="width:${Math.round(90*r[1]/mx)}px"></span>${nf(r[1])}</td></tr>`).join('')}</tbody></table>`};
      const ok=items.filter(f=>f.k).length;
      el.innerHTML=`<details class="about"><summary>Where this evidence comes from <span class="small">· ${nf(items.length)} findings, ${nf(uniq(items,f=>f.s))} sources</span></summary><div class="g">${t('Findings by country (top 7)',top(f=>f.c))}${t('Findings by study type',top(f=>f.d))}${t('Findings by review status',[['Checked by a reviewer',ok],['Not yet checked',items.length-ok]])}</div></details>`}
    const qnum=(pre,k)=>`${pre}.${Object.keys(Q).indexOf(k)+1}`;
    function qbuttons(el,counts,cur,pre){el.innerHTML=Object.keys(Q).map(k=>`<button data-q="${k}" aria-pressed="${k===cur}"><b><span class="qn">${qnum(pre,k)}</span>${Q[k][0]}</b><span>${Q[k][1]} · ${nf(counts[k]||0)} findings</span></button>`).join('')}
    function popts(sel,cur){sel.innerHTML=Object.entries(PR).map(([k,v])=>`<option value="${k}"${k===cur?' selected':''}>${esc(v)}</option>`).join('')}
    const famLabel=id=>FAM[id]?FAM[id].l:(id||'Not assigned');

    /* ---------- 3.2 Read by question ---------- */
    const A={p:'water_harvesting_conservation',f:'water_harvesting__terracing',q:'w',open:null};
    const SETS={p:['Benefit','No change','Harm','benefit','no change','harm','give a value only'],d:['Benefit','No change','Harm','benefit','no change','harm','give a value only'],h:['Copes well','Copes partly','Damage reported','copes well','copes partly','damage reported','unclear'],o:['Helps','No link found','Hinders','helps','no link found','hinders','direction not recorded']};
    const med=a=>{a=[...a].sort((x,y)=>x-y);const m=a.length>>1;return a.length%2?a[m]:(a[m-1]+a[m])/2};
    const pct=v=>(v>0?'+':v<0?'−':'')+Math.abs(Math.round(v))+'%';
    const bySource=items=>{const m=new Map();items.forEach(f=>(m.get(f.s)||m.set(f.s,[]).get(f.s)).push(f));return m};
    function ranges(items){const xs=items.filter(f=>f.u&&(f.lo!=null||f.hi!=null));const um=new Map();xs.forEach(f=>um.set(f.u,(um.get(f.u)||0)+1));const u=xs.length?[...um].sort((a,b)=>b[1]-a[1])[0][0]:'';const ys=xs.filter(f=>f.u===u);
      if(ys.length<2){const cm=new Map();items.forEach(f=>(f.cl||[]).forEach(c=>(cm.get(c)||cm.set(c,new Set()).get(c)).add(f.s)));const top=[...cm].sort((a,b)=>b[1].size-a[1].size).slice(0,4);
        return top.length?`<span>${top.map(([c,s])=>`${esc(c)} <span class="small">(${s.size})</span>`).join(' · ')}</span><br><span class="small">Classes where the practice is in use, with the number of sources.</span>`:'<span class="small">Described in words. Open to read.</span>'}
      const vals=ys.flatMap(f=>[f.lo,f.hi]).filter(v=>v!=null);let lo=Math.min(...vals),hi=Math.max(...vals);if(lo===hi)hi=lo+1;const W=220,x=v=>4+(W-8)*(v-lo)/(hi-lo);
      return`<svg class="strip" width="${W}" height="34" role="img" aria-label="${ys.length} reported ranges from ${lo} to ${hi} ${esc(u)}"><line x1="4" x2="${W-4}" y1="14" y2="14" stroke="currentColor" stroke-opacity=".3"/>${ys.map(f=>{const a=x(f.lo??lo),b=x(f.hi??hi);return`<rect x="${a}" y="8" width="${Math.max(2,b-a)}" height="12" rx="2" fill="rgba(16,185,129,.13)"><title>${esc(SRC[f.s].s)}: ${f.lo??'…'} to ${f.hi??'…'} ${esc(u)}</title></rect>`}).join('')}<text x="4" y="32">${nf(lo)}</text><text x="${W-4}" y="32" text-anchor="end">${nf(hi)} ${esc(u)}</text></svg><span class="small">${ys.length} ranges as reported. Darker = more sources overlap.</span>`}
    function verdicts(items,q){const [g,z,b,lg,lz,lb,lo]=SETS[q];const c={b:0,x:0,z:0,h:0,o:0};bySource(items).forEach(fs=>{const t=new Set(fs.map(f=>f.g));c[t.has(g)&&t.has(b)?'x':t.has(g)?'b':t.has(b)?'h':t.has(z)?'z':'o']++});
      const seg=k=>c[k]?`<i class="${k}" style="flex:${c[k]}"></i>`:'';const parts=[c.b&&`▲ ${c.b} ${lg}`,c.x&&`◆ ${c.x} mixed`,c.z&&`● ${c.z} ${lz}`,c.h&&`▼ ${c.h} ${lb}`,c.o&&`${c.o} ${lo}`].filter(Boolean);
      return`<div class="split" role="img" aria-label="${parts.join(', ')}">${seg('b')+seg('x')+seg('z')+seg('h')+seg('o')}</div><span class="small">Sources: ${parts.join(' · ')}</span>`}
    function sizes(items){const mixed=uniq(items,f=>f.ov||f.v)>1;const bs=f=>f.g==='Benefit'?1:f.g==='Harm'?-1:0;const val=f=>mixed?Math.abs(f.pc)*bs(f):f.pc;
      const m=[];bySource(items.filter(f=>f.pc!=null&&(!mixed||f.g))).forEach((fs,s)=>m.push([s,med(fs.map(val)),fs.length]));if(!m.length)return'<span class="small">No size given as a percentage</span>';
      const hiGood=mixed||items.some(f=>(f.dir===1&&f.g==='Benefit')||(f.dir===-1&&f.g==='Harm'));const v=m.map(x=>x[1]);const what=mixed?' towards benefit':'';if(m.length===1)return`<span>${pct(v[0])}${what}</span><br><span class="small">One source gives a size</span>`;
      const lo=Math.max(-100,Math.min(0,...v)),hi=Math.min(300,Math.max(0,...v)),W=200,x=u=>6+(W-12)*(Math.min(hi,Math.max(lo,u))-lo)/((hi-lo)||1);
      return`<svg class="strip" width="${W}" height="34" role="img" aria-label="Change reported by ${m.length} sources, from ${pct(Math.min(...v))} to ${pct(Math.max(...v))}"><line x1="6" x2="${W-6}" y1="12" y2="12" stroke="currentColor" stroke-opacity=".3"/><line x1="${x(0)}" x2="${x(0)}" y1="4" y2="20" stroke="currentColor" stroke-opacity=".7"/>${m.map(([s,u,k])=>`<circle cx="${x(u)}" cy="12" r="4.5" style="fill:${u===0?'var(--flat)':(u>0)===hiGood?'var(--em)':'var(--rose)'}" style="stroke:var(--bg)" stroke-width="2"><title>${esc(SRC[s].s)}: ${pct(u)}${k>1?` (middle of ${k} findings)`:''}</title></circle>`).join('')}<text x="${x(0)}" y="32" text-anchor="middle">0</text><text x="6" y="32">${lo<0?pct(lo):''}</text><text x="${W-6}" y="32" text-anchor="end">${hi>0?pct(hi):''}</text></svg><span class="small">Middle ${pct(med(v))}${what} across ${m.length} sources (${pct(Math.min(...v))} to ${pct(Math.max(...v))})${mixed?'. Mixes several measures.':''}</span>`}
    const LC={b:'var(--em)',x:'var(--amber)',z:'var(--flat)',h:'var(--rose)',o:'var(--none)'};
    function legend(q,size){if(q==='w')return`<div class="lgd"><b>Key</b><span><i style="background:rgba(16,185,129,.3)"></i>One band = the range one source reports. Darker = more sources overlap.</span><span>Words with a number in brackets = a class and how many sources name it.</span></div>`;
      const s=SETS[q],cap=x=>x[0].toUpperCase()+x.slice(1);const sw=(k,sym,txt)=>`<span><i style="background:${LC[k]}"></i>${sym} ${txt}</span>`;
      return`<div class="lgd"><b>Bar: sources</b>${sw('b','▲',cap(s[3]))}${sw('x','◆','Mixed: one source, findings disagree')}${sw('z','●',cap(s[4]))}${sw('h','▼',cap(s[5]))}${sw('o','',cap(s[6]))}</div>${size?`<div class="lgd"><b>Dots: size of change</b><span><i class="dot" style="background:${LC.b}"></i>One source, change is a benefit</span><span><i class="dot" style="background:${LC.h}"></i>One source, change is a harm</span><span>Upright line = no change (0%)</span></div>`:''}`}
    /* ---------- the evidence section: one practice, one question, two views ---------- */
    const E={p:PR.water_harvesting_conservation?'water_harvesting_conservation':Object.keys(PR)[0],f:'',q:'w',view:'map',open:null,cell:null};
    const shade=n=>n>12?'s5':n>6?'s4':n>3?'s3':n>1?'s2':'s1';
    const cross=k=>/cross_family$/.test(k)?1:0;
    function drawE(){const inP=F.filter(f=>f.p===E.p);const counts={};inP.forEach(f=>counts[f.r]=(counts[f.r]||0)+1);qbuttons($('e-q'),counts,E.q,'3');
      $('e-p').value=E.p;$('e-link').innerHTML=feeds(E.q);
      $('e-view').querySelectorAll('button').forEach(b=>b.setAttribute('aria-pressed',b.dataset.view===E.view));
      const fams=[...new Set(inP.map(f=>f.f))].sort((a,b)=>cross(a)-cross(b)||famLabel(a).localeCompare(famLabel(b)));if(E.f&&!fams.includes(E.f))E.f='';
      $('e-f').innerHTML=`<option value="">All sub-practices</option>`+fams.map(k=>`<option value="${k}"${k===E.f?' selected':''}>${esc(famLabel(k))}</option>`).join('');
      const map=E.view==='map';$('e-fwrap').hidden=map;$('e-map').hidden=$('e-cell').hidden=!map;$('e-out').hidden=$('e-about').hidden=map;
      const fm=FAM[E.f];$('e-hint').textContent=!map&&fm&&fm.n.length?`${fm.l} covers: ${fm.n.join('; ')}.`:'';
      const items=inP.filter(f=>f.r===E.q);map?drawMap(items):drawSays(items.filter(f=>!E.f||f.f===E.f))}
    function drawMap(items){const hzq=E.q==='h'||E.q==='p';const vs=new Map();items.forEach(f=>(vs.get(f.v)||vs.set(f.v,new Set()).get(f.v)).add(f.s));const order=[...vs].sort((a,b)=>b[1].size-a[1].size).map(x=>x[0]);const cols=order.slice(0,9),rest=new Set(order.slice(9));
      const fams=[...new Set(items.map(f=>f.f))].sort((a,b)=>cross(a)-cross(b)||famLabel(a).localeCompare(famLabel(b)));
      const get=(fm,v)=>items.filter(f=>f.f===fm&&(v==='*'?rest.has(f.v):f.v===v));
      const cell=(fm,v)=>{const xs=get(fm,v),n=uniq(xs,f=>f.s);const sel=E.cell&&E.cell[0]===fm&&E.cell[1]===v?' sel':'';return`<td class="cell">${n?`<button class="${shade(n)}${sel}" data-f="${fm}" data-v="${esc(v)}" aria-pressed="${!!sel}" title="${n} sources, ${xs.length} findings. Select to read them below.">${n}</button>`:'<button class="gap" disabled title="No findings">–</button>'}</td>`};
      $('e-map').innerHTML=`<table class="map"><caption>Number of sources for each sub-practice and ${hzq?'hazard':'topic'}. A dash is a gap: nothing recorded. Select a cell to read its evidence below the table.</caption><thead><tr><th>Sub-practice</th>${cols.map(v=>`<th class="c">${esc(VAR[v])}</th>`).join('')}${rest.size?`<th class="c">${rest.size} other ${hzq?'hazards':'topics'}</th>`:''}<th class="n">All sources</th></tr></thead><tbody>${fams.map(fm=>`<tr><th class="r" title="${esc((FAM[fm]?.n||[]).join('; '))}">${esc(famLabel(fm))}</th>${cols.map(v=>cell(fm,v)).join('')}${rest.size?cell(fm,'*'):''}<td class="n muted">${uniq(items.filter(f=>f.f===fm),f=>f.s)}</td></tr>`).join('')}</tbody></table>
      <div class="legend">Sources: <i style="background:rgba(16,185,129,.13)"></i>1 <i style="background:rgba(16,185,129,.26)"></i>2–3 <i style="background:rgba(16,185,129,.42)"></i>4–6 <i style="background:rgba(16,185,129,.62)"></i>7–12 <i style="background:rgba(16,185,129,.86)"></i>13 or more</div>`;
      const box=$('e-cell');if(!E.cell||!get(...E.cell).length){E.cell=null;box.innerHTML='';return}
      const [fm,v]=E.cell,xs=get(fm,v),other=v==='*',size=E.q==='d'||E.q==='p';
      box.innerHTML=`<h3 class="qh">${esc(famLabel(fm))} · ${esc(other?`other ${hzq?'hazards':'topics'}`:VAR[v])}</h3><p class="muted" style="margin:2px 0 0">${uniq(xs,f=>f.s)} sources, ${xs.length} findings. <a href="#" id="ev-e-all">See every topic for ${esc(famLabel(fm))} →</a></p>${other?'':`${legend(E.q,size)}<table class="sum"><tbody><tr><th>What the sources report</th><td>${E.q==='w'?ranges(xs):verdicts(xs,E.q)}</td>${size?`<th>Size of change, as reported</th><td>${sizes(xs)}</td>`:''}</tr></tbody></table>`}<div></div>`;
      table(box.lastElementChild,xs,other?{n:10,group:true}:E.q==='p'?{topicLabel:'What was measured',n:10,group:true}:{topic:false,n:10,group:true});
      $('e-all').onclick=e=>{e.preventDefault();E.f=fm;E.view='says';E.open=other?null:v;drawE();$('e-q').scrollIntoView({block:'start'})}}
    function drawSays(items){const by=new Map();items.forEach(f=>(by.get(f.v)||by.set(f.v,[]).get(f.v)).push(f));const topics=[...by].sort((a,b)=>uniq(b[1],f=>f.s)-uniq(a[1],f=>f.s)||b[1].length-a[1].length);
      const hzq=E.q==='h'||E.q==='p';const first=hzq?'Hazard':'Topic';const size=E.q==='d'||E.q==='p';const cols=size?6:5;
      const note=E.q==='o'?'<p class="note">The evidence does not yet record whether a factor helps or hinders. Open a topic to read what each source says.</p>':'';
      $('e-out').innerHTML=`${note}${legend(E.q,size)}<table><caption>${nf(items.length)} findings from ${nf(uniq(items,f=>f.s))} sources. A source is counted once per ${first.toLowerCase()}, however many findings it gives. Not a combined result.</caption><thead><tr><th>${first}</th><th class="n">Sources</th><th class="n">Findings</th><th>What the sources report</th>${size?'<th>Size of change, as reported</th>':''}<th class="n">Checked</th></tr></thead><tbody>${topics.map(([v,xs])=>`<tr class="row topic" data-v="${esc(v)}"><td><span class="sent">${esc(VAR[v])}</span></td><td class="n">${uniq(xs,f=>f.s)}</td><td class="n muted">${xs.length}</td><td>${E.q==='w'?ranges(xs):verdicts(xs,E.q)}</td>${size?`<td>${sizes(xs)}</td>`:''}<td class="n muted">${xs.filter(f=>f.k).length} of ${xs.length}</td></tr>`).join('')}</tbody></table>`;
      const open=tr=>{if(tr.classList.toggle('open')){const x=document.createElement('tr');x.className='exp';x.innerHTML=`<td colspan="${cols}"><div></div></td>`;tr.after(x);table(x.querySelector('div'),by.get(tr.dataset.v),E.q==='p'?{topicLabel:'What was measured',n:10,group:true}:{topic:false,n:10,group:true})}else tr.nextElementSibling.remove()};
      $('e-out').onclick=e=>{const tr=e.target.closest('tr.topic');if(tr)open(tr)};
      if(E.open){const tr=[...$('e-out').querySelectorAll('tr.topic')].find(r=>r.dataset.v===E.open);E.open=null;if(tr){open(tr);setTimeout(()=>{tr.scrollIntoView({block:'start'});window.scrollBy(0,-60)},0)}}
      about($('e-about'),items)}
    popts($('e-p'),E.p);$('e-p').onchange=e=>{E.p=e.target.value;E.f='';E.cell=null;drawE()};$('e-f').onchange=e=>{E.f=e.target.value;drawE()};
    $('e-q').onclick=e=>{const b=e.target.closest('button');if(b){E.q=b.dataset.q;E.cell=null;drawE()}};
    $('e-view').onclick=e=>{const b=e.target.closest('button');if(b){E.view=b.dataset.view;drawE()}};
    $('e-map').onclick=e=>{const b=e.target.closest('button[data-f]');if(!b)return;const same=E.cell&&E.cell[0]===b.dataset.f&&E.cell[1]===b.dataset.v;E.cell=same?null:[b.dataset.f,b.dataset.v];drawE();if(!same)$('e-cell').scrollIntoView({behavior:'smooth',block:'nearest'})};

    /* ---------- Design B ---------- */
    const B={text:'',sel:{r:new Set(),p:new Set(),v:new Set(),c:new Set(),d:new Set(),k:new Set()}};
    const FAC=[['r','Question',f=>f.r,k=>Q[k][0]],['p','Practice',f=>f.p,k=>PR[k]],['v','Topic',f=>f.ov||f.v,k=>VAR[k]],['c','Country',f=>f.c,k=>k],['d','Study type',f=>f.d,k=>k||'Not recorded'],['k','Review',f=>f.k,k=>+k?'Checked by a reviewer':'Not yet checked']];
    function pass(f,skip){if(B.text&&!f._h.includes(B.text))return false;for(const[key,,fn]of FAC){if(key===skip||!B.sel[key].size)continue;const v=fn(f);if(Array.isArray(v)?!v.some(x=>B.sel[key].has(String(x))):!B.sel[key].has(String(v)))return false}return true}
    let Bitems=[];
    function drawB(){Bitems=F.filter(f=>pass(f));
      $('b-facets').innerHTML=FAC.map(([key,title,fn,lab])=>{const m=new Map();F.forEach(f=>{if(pass(f,key))[].concat(fn(f)).forEach(v=>m.set(String(v),(m.get(String(v))||0)+1))});
        const rows=[...m].sort((a,b)=>B.sel[key].has(b[0])-B.sel[key].has(a[0])||b[1]-a[1]).slice(0,key==='v'||key==='c'?9:8);
        return`<div class="facet"><h4>${title}</h4>${rows.map(([v,n])=>`<label><input type="checkbox" data-k="${key}" value="${esc(v)}"${B.sel[key].has(v)?' checked':''}>${esc(lab(v))}<span>${nf(n)}</span></label>`).join('')}${m.size>rows.length?`<p class="small">and ${m.size-rows.length} more</p>`:''}</div>`}).join('');
      $('b-count').innerHTML=`${nf(Bitems.length)} findings <span class="muted">from ${nf(uniq(Bitems,f=>f.s))} sources</span>`;
      table($('b-out'),Bitems);about($('b-about'),Bitems)}
    $('b-facets').onchange=e=>{const s=B.sel[e.target.dataset.k];e.target.checked?s.add(e.target.value):s.delete(e.target.value);drawB()};
    let tmr;$('b-text').oninput=e=>{clearTimeout(tmr);tmr=setTimeout(()=>{B.text=e.target.value.trim().toLowerCase();drawB()},180)};
    $('b-csv').onclick=()=>{const q=s=>`"${String(s??'').replace(/"/g,'""')}"`;const head=['finding_id','practice','sub_practice','question','topic','plain_sentence','source_words','page','source','link','countries','study_type','reviewed'];
      const rows=Bitems.map(f=>[f.i,PR[f.p],famLabel(f.f),Q[f.r][0],VAR[f.ov||f.v],f.t,f.q,f.pg,SRC[f.s].c,SRC[f.s].l,f.c.join('; '),f.d,f.k?'checked':'not yet'].map(q).join(','));
      const a=document.createElement('a');a.href=URL.createObjectURL(new Blob([head.join(',')+'\n'+rows.join('\n')],{type:'text/csv'}));a.download='rural-nbs-scan-findings.csv';a.click()};
    let searchDrawn = false;
    const show = view => {
      root.querySelectorAll('.panel').forEach(p => p.classList.toggle('on', p.id === 'ev-p-' + view));
      $('b-back').hidden = view !== 'b'; $('find').setAttribute('aria-pressed', String(view === 'b')); $('how').hidden = view === 'b';
      if (view === 'b' && !searchDrawn) { searchDrawn = true; drawB(); }
    };
    $('find').onclick = () => show('b');
    $('b-back').onclick = e => { e.preventDefault(); show('e'); };
    $('zip').onclick = () => downloadAll(model, revision);
    drawE();
  }

  async function lookups(revision) {
    if (!revision) return {};
    const get = async (path) => { try { return parseCsv(await text(RAW + revision + '/' + path)); } catch (e) { return undefined; } };
    const [vont, fam, sense] = await Promise.all([
      get('registers/schema/registers/VONT_variable_ontology.csv'), get('registers/schema/registers/FAM_family_registry.csv'),
      get('configuration/method-lookups/variable_direction_sense.csv')]);
    return {vont, fam, sense};
  }

  async function render() {
    root = document.getElementById('evidence-section-root');
    if (!root || !current || mounted === current) return;
    const data = current; mounted = data;
    root.innerHTML = '<p class="ev-status" role="status">Reading the evidence registers…</p>';
    try {
      const model = buildModel(data.registers || {}, await lookups(data.registerRevision));
      if (mounted !== data) return;
      if (!model.findings.length) { root.innerHTML = '<p class="ev-status">No findings are available in this snapshot.</p>'; return; }
      mount(model, data.registerRevision || '');
    } catch (error) {
      console.error(error);
      root.innerHTML = '<p class="ev-status">The evidence section could not be drawn. The review queue is not affected.</p>';
    }
  }
  const active = () => { const tab = document.getElementById('tab-interrogator'); return !tab || tab.classList.contains('active'); };
  function refresh(data) { current = data; if (active()) render(); }
  if (typeof document !== 'undefined') {
    document.addEventListener('click', e => { if (e.target.closest && e.target.closest('#btn-interrogator,[data-shell-open="btn-interrogator"]')) setTimeout(render, 0); });
    window.addEventListener('hashchange', () => setTimeout(() => { if (active()) render(); }, 0));
  }
  const api = {refresh, render, buildModel, parseCsv, zip, crc32};
  if (typeof window !== 'undefined') window.DashboardEvidence = api;
  if (typeof module !== 'undefined') module.exports = api;
})();
