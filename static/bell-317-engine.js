export class GameEngine {
  constructor() {
    this.state = this.buildBell317State();
    this.history = ['Case file initialized: THE BELL THAT RINGS AT 3:17.'];
    this.visitedTargets = new Set();
  }

  buildBell317State() {
    return {
      player: {
        name: 'Mara Vey', health: 10, stress: 0,
        current_location: 'municipal occult office', current_scene: 'office_start',
        traits: ['Paper Trail', 'Not a Fighter', 'Claims Logic'],
        inventory: ['Cheap flashlight', 'Municipal badge', 'Broken voice recorder', 'Packet of carbon-copy incident forms', 'Box cutter', 'Lighter'],
        allies: ['Ms. Ibarra', 'Tobin Hale', 'Father Lorne']
      },
      flags: new Set(['has_fire_source']),
      discovered_clues: new Set(),
      locations: {
        'municipal occult office': { key: 'municipal occult office', scene_keys: ['office_start'] },
        'downtown records office': { key: 'downtown records office', scene_keys: ['records_main'] },
        hospital: { key: 'hospital', scene_keys: ['hospital_main'] },
        'church basement': { key: 'church basement', scene_keys: ['church_main'] },
        'school exterior': { key: 'school exterior', scene_keys: ['school_exterior'] },
        'school lobby / principal voss': { key: 'school lobby / principal voss', scene_keys: ['school_lobby'] },
        'north hallway': { key: 'north hallway', scene_keys: ['north_hallway'] },
        'attendance office': { key: 'attendance office', scene_keys: ['attendance_office'] },
        'room 103': { key: 'room 103', scene_keys: ['room_103'] },
        'basement bell chamber': { key: 'basement bell chamber', scene_keys: ['bell_chamber'] }
      },
      scenes: {
        office_start: {
          key: 'office_start', location: 'municipal occult office',
          description: 'Fluorescent lights buzz over a folder marked SCHOOL INCIDENT. The timestamp 3:17 appears on each page.',
          active_people: [], entities: [], hidden_targets: {}, exits: {},
          visible_targets: {
            'case folder': { key: 'case folder', aliases: ['folder'], description: 'The case log repeats a daily unscheduled bell at 3:17.', flag: 'knows_317', note: 'You note the 3:17 anomaly and open travel options.' }
          },
          actions: { 'to records': 'records_main', 'to hospital': 'hospital_main', 'to church': 'church_main', 'to school': 'school_exterior' }
        },
        records_main: {
          key: 'records_main', location: 'downtown records office',
          description: 'A clerk watches from behind plexiglass. A SCHOOL BOARD 1987 box sags under a leaking tile beside a locked cabinet.',
          active_people: [], entities: [], hidden_targets: {}, exits: {},
          visible_targets: {
            'school board 1987 box': { key: 'school board 1987 box', aliases: ['1987 box'], description: 'Margin notes define a hidden 3:17 accounting period.', flag: 'knows_accounting_period' },
            'locked cabinet': { key: 'locked cabinet', aliases: ['cabinet'], description: 'Blank excused forms and disciplinary circulars are filed inside.', flag: 'knows_excuse_loophole' },
            'fire inspection reports': { key: 'fire inspection reports', aliases: ['reports'], description: 'Records and schedules are listed as control documents for bell systems.', flag: 'knows_records_weakness' },
            copier: { key: 'copier', aliases: [], description: 'The copier warms up with a cough.', flag: 'has_forged_excuse', note: 'You forge an excuse form from recovered templates.' }
          },
          actions: { 'to school': 'school_exterior', 'to office': 'office_start' }
        },
        hospital_main: {
          key: 'hospital_main', location: 'hospital',
          description: 'A teacher stares blankly behind a curtain. A visitor badge reads IBARRA, E. A folded bell schedule sits on a bedside table.',
          active_people: [], entities: [], hidden_targets: {}, exits: {},
          visible_targets: {
            'visitor badge': { key: 'visitor badge', aliases: ['ibarra'], description: 'Ms. Ibarra confirms victims are marked absent before memory loss.', flag: 'befriended_ibarra' },
            'folded bell schedule': { key: 'folded bell schedule', aliases: ['origami crane'], description: 'The final printed line was scratched out, but pressure marks show 3:17.' }
          },
          actions: { 'to school': 'school_exterior', 'to office': 'office_start' }
        },
        school_exterior: {
          key: 'school_exterior', location: 'school exterior',
          description: 'Silent students stand in second-floor windows. Front doors, side gate, and office entrance wait under a tracking camera.',
          active_people: [], entities: [], hidden_targets: {}, exits: {},
          visible_targets: { 'security camera': { key: 'security camera', aliases: ['camera'], description: 'Its feed routes toward the attendance office.' } },
          actions: { 'enter lobby': 'school_lobby', 'take side gate': 'north_hallway' }
        },
        school_lobby: {
          key: 'school_lobby', location: 'school lobby / principal voss',
          description: 'Principal Voss blocks the attendance office door, hand on a red folder while the PA clicks overhead.',
          active_people: ['Principal Voss'], entities: [], hidden_targets: {}, exits: {},
          visible_targets: {
            'principal voss': { key: 'principal voss', aliases: ['voss'], description: 'He can sign formal excuse slips if convinced.', flag: 'has_signed_excuse' },
            'attendance office door': { key: 'attendance office door', aliases: ['door'], description: 'The office contains ledgers and forms.', flag: 'office_access_granted' }
          },
          actions: { 'to hallway': 'north_hallway', 'to attendance': 'attendance_office' }
        },
        north_hallway: {
          key: 'north_hallway', location: 'north hallway',
          description: 'Rainwater and toner scent the hall. A janitor mops a dry patch. A student at lockers covers his ears before each click.',
          active_people: ['Tobin Hale', 'Janitor Remainder'], entities: [], hidden_targets: {}, exits: {},
          visible_targets: {
            'paper bell schedule': { key: 'paper bell schedule', aliases: ['schedule'], description: 'The final line was scratched out after 3:17.' },
            'student near lockers': { key: 'student near lockers', aliases: ['tobin'], description: 'Tobin hears a pre-ring one second early.', flag: 'befriended_tobin' },
            janitor: { key: 'janitor', aliases: ['dry floor patch'], description: 'His bucket holds a stale work order: corridor C, indefinite.', flag: 'has_work_order' }
          },
          actions: { 'to room 103': 'room_103', 'to attendance': 'attendance_office', 'to lobby': 'school_lobby' }
        },
        attendance_office: {
          key: 'attendance_office', location: 'attendance office',
          description: 'A wall clock is stopped at 3:17. Filing cabinets crowd a red attendance ledger. The intercom whispers names followed by absent.',
          active_people: [], entities: [], hidden_targets: {}, exits: {},
          visible_targets: {
            'red attendance ledger': { key: 'red attendance ledger', aliases: ['ledger'], description: 'Every victim was marked absent before symptoms.', flag: 'knows_records_weakness' },
            'blank excused absence forms': { key: 'blank excused absence forms', aliases: ['blank forms'], description: 'Carbon-copy forms for formal excuse processing.', flag: 'has_blank_excuse_form' },
            'intercom handset': { key: 'intercom handset', aliases: ['intercom'], description: 'A command channel tied to authority routing.' }
          },
          actions: { 'to room 103': 'room_103', 'to bell chamber': 'bell_chamber', 'to hallway': 'north_hallway' }
        },
        room_103: {
          key: 'room_103', location: 'room 103',
          description: 'Detention desks face the wall. A chalkboard lists ABSENT names, ending with MARA VEY unfinished. A brass handbell rests on the desk.',
          active_people: [], entities: [], hidden_targets: {}, exits: {},
          visible_targets: {
            chalkboard: { key: 'chalkboard', aliases: ['absent'], description: 'Your name is being written under ABSENT.', flag: 'player_marked_absent' },
            'brass handbell': { key: 'brass handbell', aliases: ['handbell'], description: 'A manual override bell used before automated schedules.', flag: 'has_brass_handbell' }
          },
          actions: { 'to bell chamber': 'bell_chamber', 'to hallway': 'north_hallway' }
        },
        bell_chamber: {
          key: 'bell_chamber', location: 'basement bell chamber',
          description: 'Old brick arches frame a bronze bell. Attendance slips wrap the clapper. A tall hall-monitor figure waits with a blank paper face.',
          active_people: [], entities: ['Bell Monitor'], hidden_targets: {},
          visible_targets: {
            'bell monitor': { key: 'bell monitor', aliases: ['monitor'], description: 'It asks your attendance status.', flag: 'final_confrontation_started' },
            'clapper wrapped in attendance slips': { key: 'clapper wrapped in attendance slips', aliases: ['attendance slips'], description: 'Destroying slips may weaken it.', flag: 'bell_records_destroyed' }
          },
          exits: { retreat: 'north_hallway' },
          actions: {}
        },
        church_main: { key: 'church_main', location: 'church basement', description: 'Emergency candles sit beneath a child\'s drawing of a bell with teeth. Father Lorne waits by folding chairs.', active_people: [], entities: [], hidden_targets: {}, exits: {}, visible_targets: { 'father lorne': { key: 'father lorne', aliases: ['lorne'], description: 'He warns that records and authority bind the entity.', flag: 'recruited_lorne' }, 'emergency candles': { key: 'emergency candles', aliases: ['candles'], description: "They'll burn ledgers quickly.", flag: 'has_fire_source' } }, actions: { 'to school': 'school_exterior', 'to office': 'office_start' } }
      }
    };
  }
  currentScene() { return this.state.scenes[this.state.player.current_scene]; }
  normalize(s) { return String(s || '').trim().toLowerCase().replace(/\s+/g, ' '); }
  uiEffects() { const s = this.state.player.stress; return { glitch: s >= 3, flicker: s >= 5, scramble: s >= 7, intensity: Math.min(s / 10, 1) }; }
  sceneMarkup() {
    const scene = this.currentScene(); const parts = [scene.description];
    const targets = Object.keys(scene.visible_targets); if (targets.length) parts.push(`Investigations: ${targets.map(k => `[[${k}]]`).join(' ')}`);
    if (scene.active_people.length) parts.push(`Contacts: ${scene.active_people.map(n => `{{${n}}}`).join(' ')}`);
    if (scene.entities.length) parts.push(`Entities: ${scene.entities.map(n => `!!${n}!!`).join(' ')}`);
    const exits = Object.keys(scene.exits || {}); if (exits.length) parts.push(`Exits: ${exits.map(e => `>>${e}`).join(' ')}`);
    const actions = Object.keys(scene.actions || {}); if (actions.length) parts.push(`Actions: ${actions.map(a => `[Action: ${a}]`).join(' ')}`);
    if (this.visitedTargets.size) parts.push(`Visited: ${Array.from(this.visitedTargets).sort().map(v => `~~${v}~~`).join(' ')}`);
    return parts.join('\n');
  }
  getState() { const p = this.state.player; return { player: { name: p.name, health: p.health, stress: p.stress, location: p.current_location, scene: p.current_scene, traits: p.traits }, scene: { key: this.currentScene().key, location: this.currentScene().location, text: this.sceneMarkup() }, allies: p.allies, inventory: p.inventory, clues: Array.from(this.state.discovered_clues).sort(), history: this.history.slice(-100), ui_effects: this.uiEffects(), locations: Object.keys(this.state.locations).sort() }; }
  investigate(raw) {
    const scene = this.currentScene(); const key = this.normalize(raw);
    for (const t of Object.values(scene.visible_targets)) {
      if (key === this.normalize(t.key) || (t.aliases || []).map(a => this.normalize(a)).includes(key)) {
        if (t.flag) this.state.flags.add(t.flag);
        if (t.flag) this.state.discovered_clues.add(t.flag);
        return t.note ? `${t.description} ${t.note}` : t.description;
      }
    }
    return 'You find nothing by that name here.';
  }
  action(name) { const target = this.currentScene().actions[this.normalize(name)]; if (!target) return 'No such action in this scene.'; this.state.player.current_scene = target; this.state.player.current_location = this.currentScene().location; return `Action: ${name}`; }
  talk(name) { return this.currentScene().active_people.map(n => this.normalize(n)).includes(this.normalize(name)) ? `You speak with ${name}. They seem uneasy but cooperative.` : 'No one by that name is here.'; }
  run() { const to = this.currentScene().exits.retreat; if (!to) return 'No immediate route to run.'; this.state.player.current_scene = to; this.state.player.current_location = this.currentScene().location; return 'You flee.'; }
  go(loc) { const l = this.state.locations[this.normalize(loc)]; if (!l) return 'Unknown location.'; this.state.player.current_location = l.key; this.state.player.current_scene = l.scene_keys[0]; return `Moved to ${l.key}.`; }
  command(raw) { const [cmd, ...rest] = String(raw || '').trim().split(/\s+/); const arg = rest.join(' '); if (!cmd) return 'No command provided.'; if (cmd === 'go') return this.go(arg); if (cmd === 'investigate') return this.investigate(arg); if (cmd === 'action') return this.action(arg); if (cmd === 'talk') return this.talk(arg); if (cmd === 'run') return this.run(); return `Unknown command: ${raw}`; }
  applyAction(type, id) {
    const prev = this.state.player.current_scene;
    let message = 'Unknown action';
    if (type === 'investigation') { this.visitedTargets.add(id); message = this.investigate(id); }
    else if (type === 'npc') message = this.talk(id);
    else if (type === 'exit') message = id === 'retreat' ? this.run() : this.action(id);
    else if (type === 'action') message = this.action(id);
    else if (type === 'danger') { message = this.investigate(id); this.state.player.stress += 1; message += ' (+1 stress)'; }
    else if (type === 'command') message = this.command(id);
    if (this.state.player.current_scene !== prev) this.history.push(`Scene changed: ${prev} -> ${this.state.player.current_scene}`);
    this.history.push(message);
    return message;
  }
}
