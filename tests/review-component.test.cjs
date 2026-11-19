const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');

const code = fs.readFileSync(path.join(__dirname, '../review/workspace.js'), 'utf8');
const release = JSON.parse(fs.readFileSync(path.join(__dirname, '../review/release.json'), 'utf8'));
function element(tag = 'div') {
  return { tag, children: [], hidden: false, textContent: '', writes: 0,
    append(...children) { this.children.push(...children); },
    appendChild(child) { this.append(child); },
    replaceChildren(...children) { this.children = children; this.writes++; }
  };
}
function text(node) { return node.textContent + node.children.map(text).join(''); }
function harness(revision = 'a'.repeat(40)) {
  const nodes = { 'review-build': element(), 'dashboard-build': element(),
    'review-component-release': {...element(), textContent: JSON.stringify(release)},
    'vf-sidebar-panel': element(), 'review-reference-guide': element(), 'historical-footer': element() };
  let listeners = 0;
  const context = { window: {}, document: {
    getElementById: id => nodes[id], querySelector: selector => selector === '.meta-timestamp' ? nodes['historical-footer'] : ({id:'tab-qaqc'}),
    createElement: element, createTextNode: value => ({...element('text'),textContent:value})
  }, reviewData: {registerRevision: revision},
    // Release display must not touch saved drafts or source-folder permissions.
    localStorage: new Proxy({}, {get(){throw Error('Storage touched by component mount');}})
  };
  context.window.matchMedia = () => ({ matches: true, addEventListener(){listeners++;} });
  vm.createContext(context);vm.runInContext(code, context);
  return {context, nodes, api:context.window.ReviewWorkspace, listeners:()=>listeners};
}

test('component mounts once, preserves drafts, and shows official evidence pin independently', () => {
  const h = harness();h.api.mount();h.api.mount();
  assert.equal(h.listeners(),1);
  assert.equal(h.nodes['vf-sidebar-panel'].open,true);
  assert.equal(h.nodes['dashboard-build'].hidden,false);
  assert.equal(h.nodes['historical-footer'].hidden,true);
  assert.equal(h.nodes['review-build'].hidden,false);
  assert.ok(text(h.nodes['review-build']).startsWith('Review v' + release.version + ' · Evidence aaaaaaaa'));
  assert.equal(h.nodes['review-build'].children[0].children[0].href,'https://github.com/RuralScan/evidence/tree/'+'a'.repeat(40));
  const writes=h.nodes['review-build'].writes;h.api.updateBuild();
  assert.equal(h.nodes['review-build'].writes,writes, 'unchanged label must not trigger observer/render loop');
  h.context.reviewData.registerRevision='b'.repeat(40);h.api.updateBuild();
  assert.ok(text(h.nodes['review-build']).startsWith('Review v' + release.version + ' · Evidence bbbbbbbb'));
  assert.equal(h.nodes['review-build'].writes,writes+1);
});

test('shared change history keeps dashboard and review versions visible across navigation', () => {
  const h=harness();h.api.mount();
  h.nodes['dashboard-build'].textContent='Historical dashboard version';
  h.api.onTab('tab-methods');
  assert.equal(h.nodes['review-build'].hidden,false);
  assert.equal(h.nodes['dashboard-build'].hidden,false);
  assert.equal(h.nodes['historical-footer'].hidden,false);
  assert.equal(h.nodes['dashboard-build'].textContent,'Historical dashboard version');
  h.api.onTab('tab-qaqc');
  assert.equal(h.nodes['review-build'].hidden,false);
  assert.match(text(h.nodes['review-build']), /Review changes/);
});

test('unavailable or invalid official revision never gets an invented evidence link', () => {
  for (const revision of ['', 'short-sha', 'javascript:alert(1)']) {
    const h=harness(revision);h.api.mount();
    assert.match(text(h.nodes['review-build']), /Evidence revision unavailable/);
    assert.equal(h.nodes['review-build'].children[0].children[0].tag,'text');
  }
});
