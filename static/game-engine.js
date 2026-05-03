export class GameEngine {
  constructor() {
    this.state = this.buildDemoState();
    this.history = ['Case file initialized.'];
    this.visitedTargets = new Set();
  }

  buildDemoState() {
    return {
      player: {
        name: 'Mara Vey', health: 10, stress: 0, current_location: 'downtown', current_scene: 'downtown_street',
        traits: [
          'Paper Trail: once per scene, reroll Archive or Pattern on institutional records.',
          'Not a Fighter: -2 on direct Force attacks unless prepared.',
          'Claims Logic: +2 Pattern after observing rule-bound behavior once.'
        ],
        inventory: ['Cheap flashlight', 'Municipal badge', 'Broken voice recorder', 'Carbon-copy incident forms', 'Box cutter', 'Lighter'],
        allies: []
      },
      flags: new Set(),
      discovered_clues: new Set(),
      locations: {
        downtown: { key: 'downtown', scene_keys: ['downtown_street'] },
        school: { key: 'school', scene_keys: ['downtown_alley'] },
        hospital: { key: 'hospital', scene_keys: ['downtown_street'] },
        'village edge': { key: 'village edge', scene_keys: ['downtown_street'] },
        apartments: { key: 'apartments', scene_keys: ['downtown_street'] },
        church: { key: 'church', scene_keys: ['downtown_street'] },
        'industrial zone': { key: 'industrial zone', scene_keys: ['downtown_street'] },
        subway: { key: 'subway', scene_keys: ['downtown_street'] }
      },
      scenes: {
        downtown_street: {
          key: 'downtown_street', location: 'downtown',
          description: 'The boulevard is damp and too quiet. A bus map hums under flickering light.',
          active_people: ['night janitor'],
          visible_targets: {
            'bus map': { key: 'bus map', aliases: ['map'], description: 'Routes are marked, but one line is erased nightly.' },
            'storm drain': { key: 'storm drain', aliases: ['drain'], description: 'Rainwater circles despite no current storm.' }
          },
          hidden_targets: {},
          exits: { retreat: 'downtown_street' },
          actions: { 'inspect alley': 'downtown_alley' },
          entities: []
        },
        downtown_alley: {
          key: 'downtown_alley', location: 'downtown',
          description: 'The alley smells like rainwater and copier toner. A trophy case stands cracked beside Room 103 signage.',
          active_people: [],
          visible_targets: {
            hallway: { key: 'hallway', aliases: ['alley'], description: 'Narrow and lined with peeling school notices.' },
            rainwater: { key: 'rainwater', aliases: [], description: 'It beads uphill for a second before falling.' },
            'copier toner': { key: 'copier toner', aliases: ['toner'], description: 'Fresh residue leads to a locked service hatch.' },
            'trophy case': { key: 'trophy case', aliases: ['case'], description: 'The glass is cracked inward.', on_investigate: 'inspect_trophy' },
            'room 103': { key: 'room 103', aliases: ['103'], description: 'A painted arrow points nowhere.' }
          },
          hidden_targets: {
            'room 103 ledger': { key: 'room 103 ledger', aliases: ['ledger'], description: "Detentions list names that don't exist in records." }
          },
          exits: { retreat: 'downtown_street' },
          actions: {},
          entities: []
        }
      }
    };
  }

  currentScene() { return this.state.scenes[this.state.player.current_scene]; }

  sceneMarkup() {
    const scene = this.currentScene();
    const parts = [scene.description];
    const targets = Object.keys(scene.visible_targets);
    if (targets.length) parts.push(`Investigations: ${targets.map(k => `[[${k}]]`).join(' ')}`);
    if (scene.active_people.length) parts.push(`Contacts: ${scene.active_people.map(n => `{{${n}}}`).join(' ')}`);
    if (scene.entities.length) parts.push(`Entities: ${scene.entities.map(n => `!!${n}!!`).join(' ')}`);
    const exits = Object.keys(scene.exits);
    if (exits.length) parts.push(`Exits: ${exits.map(e => `>>${e}`).join(' ')}`);
    const actions = Object.keys(scene.actions);
    if (actions.length) parts.push(`Actions: ${actions.map(a => `[Action: ${a}]`).join(' ')}`);
    if (scene.hidden_targets['room 103 ledger']) parts.push('Missing lead: --room 103 ledger--');
    if (this.visitedTargets.size) parts.push(`Visited: ${Array.from(this.visitedTargets).sort().map(v => `~~${v}~~`).join(' ')}`);
    return parts.join('\n');
  }

  uiEffects() {
    const s = this.state.player.stress;
    return { glitch: s >= 3, flicker: s >= 5, scramble: s >= 7, intensity: Math.min(s / 10, 1) };
  }

  getState() {
    const p = this.state.player;
    return {
      player: { name: p.name, health: p.health, stress: p.stress, location: p.current_location, scene: p.current_scene, traits: p.traits },
      scene: { key: this.currentScene().key, location: this.currentScene().location, text: this.sceneMarkup() },
      allies: p.allies, inventory: p.inventory, clues: Array.from(this.state.discovered_clues).sort(),
      history: this.history.slice(-100),
      ui_effects: this.uiEffects(), locations: Object.keys(this.state.locations).sort()
    };
  }

  applyAction(type, id) {
    const prev = this.state.player.current_scene;
    let message = 'Unknown action';
    if (type === 'investigation') { this.visitedTargets.add(id); message = this.investigate(id); }
    else if (type === 'npc') { message = this.talk(id); }
    else if (type === 'exit') { message = id === 'retreat' ? this.run() : this.action(id); }
    else if (type === 'action') { message = this.action(id); }
    else if (type === 'danger') { message = this.investigate(id); this.state.player.stress += 1; message += ' (+1 stress)'; }
    else if (type === 'command') { message = this.command(id); }

    if (this.state.player.current_scene !== prev) this.history.push(`Scene changed: ${prev} -> ${this.state.player.current_scene}`);
    this.history.push(message);
    return message;
  }

  normalize(s) { return String(s || '').trim().toLowerCase().replace(/\s+/g, ' '); }

  investigate(raw) {
    const scene = this.currentScene();
    const key = this.normalize(raw);
    for (const t of Object.values(scene.visible_targets)) {
      if (key === this.normalize(t.key) || t.aliases.map(a => this.normalize(a)).includes(key)) {
        if (t.on_investigate === 'inspect_trophy') {
          scene.hidden_targets['room 103 ledger'] && (scene.visible_targets['room 103 ledger'] = scene.hidden_targets['room 103 ledger']);
          delete scene.hidden_targets['room 103 ledger'];
          this.state.discovered_clues.add('school_emblem');
          return `${t.description} You find a clue and a hidden ledger slot behind cracked glass.`;
        }
        return t.description;
      }
    }
    return 'You find nothing by that name here.';
  }

  action(name) {
    const scene = this.currentScene();
    const target = scene.actions[this.normalize(name)];
    if (!target) return 'No such action in this scene.';
    this.state.player.current_scene = target;
    return `Action: ${name}`;
  }
  talk(name) { return this.currentScene().active_people.map(n => this.normalize(n)).includes(this.normalize(name)) ? `You speak with ${name}. They seem uneasy but cooperative.` : 'No one by that name is here.'; }
  run() { const to = this.currentScene().exits.retreat; if (!to) return 'No immediate route to run.'; this.state.player.current_scene = to; return 'You flee.'; }
  go(loc) { const l = this.state.locations[this.normalize(loc)]; if (!l) return 'Unknown location.'; this.state.player.current_location = l.key; this.state.player.current_scene = l.scene_keys[0]; return `Moved to ${l.key}.`; }

  command(raw) {
    const [cmd, ...rest] = String(raw || '').trim().split(/\s+/);
    const arg = rest.join(' ');
    if (!cmd) return 'No command provided.';
    if (cmd === 'go') return this.go(arg);
    if (cmd === 'investigate') return this.investigate(arg);
    if (cmd === 'action') return this.action(arg);
    if (cmd === 'talk') return this.talk(arg);
    if (cmd === 'run') return this.run();
    return `Unknown command: ${raw}`;
  }
}
