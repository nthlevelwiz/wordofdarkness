import { GameEngine } from './bell-317-engine.js';

const engine = new GameEngine();
const sceneEl = document.getElementById('sceneText');
const actionBar = document.getElementById('actionBar');
const playerPanel = document.getElementById('playerPanel');

const tokenPatterns = [
  { type: 'danger', re: /^!!([^!]+)!!/ },
  { type: 'investigation', re: /^\[\[([^\]]+)\]\]/ },
  { type: 'npc', re: /^\{\{([^}]+)\}\}/ },
  { type: 'action', re: /^\[Action:\s*([^\]]+)\]/ },
  { type: 'locked', re: /^--([^\-]+)--/ },
  { type: 'visited', re: /^~~([^~]+)~~/ },
  { type: 'exit', re: /^>>([^\n\s][^\n]*)/ },
];

function buildTokenButton(type, label) {
  const btn = document.createElement('button');
  btn.className = `link-btn ${type}`;
  btn.type = 'button';
  btn.textContent = label.trim();
  if (type === 'locked' || type === 'visited') btn.disabled = true;
  else btn.addEventListener('click', () => { engine.applyAction(type, label.trim()); renderState(engine.getState()); });
  return btn;
}

function parseAndRenderScene(text) {
  sceneEl.replaceChildren();
  const frag = document.createDocumentFragment();
  text.split('\n').forEach((line, idx, lines) => {
    let rest = line;
    while (rest.length) {
      let matched = false;
      for (const rule of tokenPatterns) {
        const m = rest.match(rule.re);
        if (m) { frag.appendChild(buildTokenButton(rule.type, m[1])); rest = rest.slice(m[0].length); matched = true; break; }
      }
      if (!matched) { frag.appendChild(document.createTextNode(rest[0])); rest = rest.slice(1); }
    }
    if (idx < lines.length - 1) frag.appendChild(document.createElement('br'));
  });
  sceneEl.appendChild(frag);
}

function fillList(id, values) {
  const el = document.getElementById(id);
  el.replaceChildren();
  values.forEach(v => { const li = document.createElement('li'); li.textContent = v; el.appendChild(li); });
}

function applyEffects(effects) {
  const app = document.getElementById('app');
  app.classList.toggle('glitch', !!effects.glitch);
  app.classList.toggle('flicker', !!effects.flicker);
  app.classList.toggle('scramble', !!effects.scramble);
}

function renderState(state) {
  parseAndRenderScene(state.scene.text);
  playerPanel.textContent = `${state.player.name} | HP ${state.player.health} | Stress ${state.player.stress} | ${state.player.location}`;
  fillList('alliesList', state.allies);
  fillList('inventoryList', state.inventory);
  fillList('cluesList', state.clues);
  fillList('historyList', state.history.slice().reverse());
  applyEffects(state.ui_effects);

  actionBar.replaceChildren();
  state.locations.forEach(loc => {
    const b = document.createElement('button');
    b.className = 'link-btn action';
    b.textContent = `go ${loc}`;
    b.addEventListener('click', () => { engine.applyAction('command', `go ${loc}`); renderState(engine.getState()); });
    actionBar.appendChild(b);
  });
}

document.getElementById('commandForm').addEventListener('submit', (e) => {
  e.preventDefault();
  const input = document.getElementById('commandInput');
  const cmd = input.value.trim();
  if (cmd) { engine.applyAction('command', cmd); renderState(engine.getState()); }
  input.value = '';
});

renderState(engine.getState());
