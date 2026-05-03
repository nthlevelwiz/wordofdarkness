# THE BELL THAT RINGS AT 3:17

## 1) Module Overview
- **Genre/Tone:** Institutional horror, procedural occult investigation, high pressure at fixed time event (3:17 PM).
- **Playable PC:** Mara Vey (provided build).
- **Core Loop:** Investigate -> collect procedural leverage -> recruit allies -> confront Bell Monitor using rules/records/authority (or flee/sacrifice).
- **Failure Pressure:** `time`, `stress`, `memory_damage`, and the 3:17 bell pulse.
- **Design Notes:** Non-linear node graph. Most conflict can be solved socially/procedurally; violence is risky and often ineffective until ritual anchors are weakened.

---

## 2) Core Flags / State Variables
Use provided variables plus these additions.

```yaml
flags:
  # required
  knows_317: false
  knows_accounting_period: false
  knows_excuse_loophole: false
  knows_records_weakness: false
  knows_janitor_task_loop: false
  has_fire_source: true        # starts true because Mara has a lighter
  has_signed_excuse: false
  has_forged_excuse: false
  has_work_order: false
  befriended_tobin: false
  befriended_ibarra: false
  recruited_lorne: false
  angered_principal: false
  janitor_released: false
  janitor_hostile: false
  bell_records_destroyed: false
  player_marked_absent: false
  bell_rang_once: false

  # added
  has_blank_excuse_form: false
  has_brass_handbell: false
  principal_ally: false
  office_access_granted: false
  room103_unlocked: false
  saw_absent_chalkboard: false
  knows_pre_ring_warning: false
  forged_excuse_quality_good: false
  forged_excuse_quality_weak: false
  monitor_observed_rulebound: false
  final_confrontation_started: false

meters:
  time: 0            # abstract units; 1-2 per major action
  memory_damage: 0   # 0..4+
  stress: 0          # 0..6+
```

---

## 3) Player Character Data (Demo)

```yaml
player:
  name: Mara Vey
  background: Former city claims adjuster; now municipal occult liability investigator.
  primary:
    mind: 4
    heart: 3
    blood: 1
    nerve: 2
  secondary:
    logic: 4
    archive: 3
    pattern: 5
    occult: 2
    empathy: 3
    presence: 2
    composure: 4
    faith: 1
    force: 1
    endurance: 2
    menace: 1
    instinct: 2
    notice: 3
    reflex: 2
    stealth: 1
    hands: 2
  traits:
    - Paper Trail: once/scene reroll Archive or Pattern on records/schedules/maps/institutional systems.
    - Not a Fighter: -2 on direct Force attacks unless scene prepared.
    - Claims Logic: after observing a repeating rule behavior, +2 Pattern vs that entity.
  inventory:
    - Cheap flashlight
    - Municipal badge
    - Broken voice recorder
    - Packet of carbon-copy incident forms
    - Box cutter
    - Lighter
```

---

## 4) Locations, Actions, Scenes

> **Location lock:** This module uses exactly the 10 required major locations with unchanged names and roles.

## LOCATION: Municipal Occult Office
**Purpose:** Start case; establish liability framing and open travel options.

**Available actions**
- review_case
- call_destinations
- depart_to_records
- depart_to_hospital
- depart_to_church
- depart_to_school

**Scene text**
> Fluorescent lights hum above dented filing cabinets. A city seal peels from the wall beside a bulletin board of impossible claims. Your desk holds a case folder stamped SCHOOL INCIDENT: MEMORY LOSS EVENT. A broken voice recorder clicks once and dies.

**Visible investigation targets**
- `case folder` -> sets `knows_317` (mentions repeated 3:17 ring)
- `impossible claims board` -> flavor + stress risk -1 (you’ve seen worse)
- `broken voice recorder` -> foreshadow command-drop effects

**Hidden investigation targets**
- `city seal` -> unlocks authority framing (+1 future Presence vs Voss once)

**NPCs/entities present**
- none live, remote dispatcher by phone (non-interaction flavor)

**Action results**
- `review_case`: `time +1`, clue seed of school/hospital/records.
- `call_destinations`: marks all travel nodes known.

**Flags changed**
- `knows_317 = true` after folder investigation.

**Checks required**
- none mandatory.

**Possible transitions**
- Downtown Records Office / Hospital / Church Basement / School Exterior.

---

## LOCATION: Downtown Records Office
**Purpose:** Discover accounting-period contradiction, excuse loophole, records anchor; obtain forms/forgery path.

**Available actions**
- speak_clerk
- investigate_archive_room
- inspect_cabinet
- copy_documents
- forge_excuse
- depart

**Scene text**
> The records office smells of wet paper and copier ozone. A clerk taps a keyboard behind scratched plexiglass. A box labeled SCHOOL BOARD 1987 sags under a leaking ceiling tile. A locked cabinet sits beneath FIRE INSPECTION REPORTS. The copier blinks READY, then NOT READY, then READY again.

**Visible investigation targets**
- `clerk` -> bureaucratic resistance; can grant supervised access
- `school board 1987 box` -> reveals “3:17 accounting period” memo draft
- `locked cabinet` -> contains disciplinary circular and blank excuse forms
- `fire inspection reports` -> reveals basement retrofits, bell chamber access
- `copier` -> can duplicate/alter documents
- `leaking ceiling tile` -> hides water-damaged attendance appendices

**Hidden investigation targets**
- `memo draft margin notes` (from 1987 box) -> `knows_accounting_period = true`
- `disciplinary circular line 12` (from cabinet) -> `knows_excuse_loophole = true`
- `appendix staple marks` (from ceiling tile stash) -> `knows_records_weakness = true`

**NPCs/entities present**
- Records Clerk (minor NPC)

**Action results**
- `speak_clerk`: social gate for cabinet key route.
- `inspect_cabinet`: can obtain `has_blank_excuse_form`.
- `copy_documents`: create backup proof packet (+1 to Voss “show evidence”).
- `forge_excuse`: sets forged flags.

**Flags changed**
- `knows_accounting_period`, `knows_excuse_loophole`, `knows_records_weakness`, `has_blank_excuse_form`, `has_forged_excuse`, `forged_excuse_quality_good|weak`.

**Checks required**
- Access cabinet: Heart+Presence DC12 or Nerve+Hands DC12 (pick lock improvised).
- Forge excuse: Mind+Archive DC15 (Paper Trail reroll allowed).
  - clean/strong success -> `has_forged_excuse=true`, `forged_excuse_quality_good=true`
  - weak/tie -> `has_forged_excuse=true`, `forged_excuse_quality_weak=true`
  - fail -> flagged suspicious copy (future -2 when presented)

**Possible transitions**
- Municipal Office, Hospital, Church Basement, School Exterior.

---

## LOCATION: Hospital
**Purpose:** Victim evidence, Ms. Ibarra ally path, “marked absent before loss” clue.

**Available actions**
- examine_teacher
- speak_nurse
- inspect_bedside
- interact_ibarra
- depart

**Scene text**
> A teacher lies behind a curtain, staring at her own hands like unfamiliar tools. A visitor badge on a chair reads IBARRA, E. The nurse at the station keeps rechecking the same chart. On the bedside table: wilted flowers and a folded bell schedule creased into an origami crane.

**Visible investigation targets**
- `teacher behind curtain` -> confirms personal memory severance
- `visitor badge saying IBARRA, E.` -> starts Ibarra interaction
- `nurse` -> chart says “ABSENT” stamped before cognitive crash
- `bedside table` -> origami crane from bell schedule
- `folded bell schedule/origami crane` -> confirms unscheduled 3:17 line removed

**Hidden investigation targets**
- `chart stamp timestamp` -> proves “absent” notation predated symptoms

**NPCs/entities present**
- Ms. Ibarra, Nurse, victim teacher

**Action results**
- may set `befriended_ibarra` and add ally.

**Flags changed**
- `knows_317`, `befriended_ibarra`.

**Checks required**
- Calm Ibarra: Heart+Empathy DC11.
- Recruit as ally: Heart+Composure DC12 (or auto if you show copied records proof).

**Possible transitions**
- Any hub location, especially School Exterior.

---

## LOCATION: Church Basement
**Purpose:** Occult framing + practical tools; Father Lorne ally path.

**Available actions**
- inspect_room
- interact_lorne
- take_candles
- depart

**Scene text**
> Folding chairs form a crooked circle around coffee urns gone cold. Old hymnals are stacked beside a NO SMOKING sign. Father Lorne watches the stairwell, not the room. Emergency candles sit in a milk crate under a child’s drawing of a bell with teeth.

**Visible investigation targets**
- `folding chairs`
- `coffee urns`
- `old hymnals`
- `Father Lorne`
- `NO SMOKING sign`
- `emergency candles`
- `child’s drawing of bell with teeth`

**Hidden investigation targets**
- `hymnal margin prayer` -> “names written are names kept” (records anchor clue)

**NPCs/entities present**
- Father Lorne

**Action results**
- recruit Lorne, learn weakness, gain fire source if somehow missing.

**Flags changed**
- `recruited_lorne`, `knows_records_weakness`, `has_fire_source=true`.

**Checks required**
- See interaction section; partial success still grants occult clue.

**Possible transitions**
- Any hub location.

---

## LOCATION: School Exterior
**Purpose:** Entry choice, surveillance tension, non-linear branching into lobby or side routes.

**Available actions**
- enter_front_doors
- circle_to_side_gate
- inspect_dumpsters
- approach_office_entrance
- watch_windows

**Scene text**
> The school stands dark except for strips of humming hallway light. Silent students watch from second-floor windows, then step away in unison. Front doors reflect your flashlight. A side gate hangs half-latched near dumpsters. A security camera tracks you with tiny mechanical patience. The office entrance glows under a failing bulb.

**Visible investigation targets**
- `front doors`
- `silent students in windows`
- `side gate`
- `dumpsters`
- `security camera`
- `office entrance`

**Hidden investigation targets**
- `camera housing` -> reveals wire to attendance office monitor (alternate access info)

**NPCs/entities present**
- none directly

**Action results**
- front/office -> School Lobby
- side gate/dumpsters -> North Hallway (harder stealth check if principal angered)

**Flags changed**
- none guaranteed.

**Checks required**
- Side entry stealth: Nerve+Stealth DC11 (DC14 if `angered_principal`).

**Possible transitions**
- School Lobby / North Hallway.

---

## LOCATION: School Lobby / Principal Voss
**Purpose:** Authority route, signed excuse route, office access route.

**Available actions**
- interact_voss
- inspect_attendance_office_door
- inspect_red_folder
- inspect_pa_speaker
- inspect_office_key
- leave_to_hall

**Scene text**
> Principal Voss stands behind the counter with his tie pulled too tight. The attendance office door is shut beside him. A red folder sits under his palm like a shield. Above, the PA speaker clicks, pauses, and clicks again. An office key hangs on a labeled peg: ATTENDANCE.

**Visible investigation targets**
- `Principal Voss`
- `attendance office door`
- `red folder`
- `PA speaker`
- `office key`

**Hidden investigation targets**
- `red folder incident list` -> links Room 103 detentions to memory cases

**NPCs/entities present**
- Principal Voss

**Action results**
- signed excuse / principal ally / angered state / lockdown modifier.

**Flags changed**
- `has_signed_excuse`, `principal_ally`, `angered_principal`, `office_access_granted`.

**Checks required**
- see Principal interaction.

**Possible transitions**
- Attendance Office, North Hallway, School Exterior.

---

## LOCATION: North Hallway
**Purpose:** Central investigative pressure; Tobin + Janitor encounters; Room 103 lead.

**Available actions**
- inspect_hall
- interact_tobin
- interact_janitor
- inspect_room103_door
- inspect_schedule
- move_to_attendance
- move_to_room103

**Scene text**
> Rainwater and copier toner share the air. A cracked trophy case reflects your silhouette in broken pieces. Room 103 sits halfway down the hall. A janitor mops the same dry floor patch in slow circles. Overhead, a PA speaker clicks every seventeen seconds. A paper bell schedule is taped to the wall, its final line scratched out. A student by the lockers covers his ears and whispers before each click.

**Visible investigation targets**
- `rainwater smell`
- `copier toner smell`
- `cracked trophy case`
- `Room 103`
- `janitor`
- `dry floor patch`
- `PA speaker clicking every seventeen seconds`
- `paper bell schedule`
- `scratched-out final line`
- `student near lockers covering his ears`

**Hidden investigation targets**
- `mop bucket work order` -> `has_work_order=true` and `knows_janitor_task_loop=true`
- `schedule glue shadow` -> confirms deleted 3:17 line

**NPCs/entities present**
- Tobin Hale, Janitor Remainder

**Action results**
- Tobin ally opportunity.
- Janitor release/combat branch.
- Unlock Room 103.

**Flags changed**
- `befriended_tobin`, `knows_pre_ring_warning`, `knows_janitor_task_loop`, `has_work_order`, `janitor_released`, `janitor_hostile`, `room103_unlocked`.

**Checks required**
- Multiple via interactions.

**Possible transitions**
- School Lobby, Attendance Office, Room 103.

---

## LOCATION: Attendance Office
**Purpose:** Forms, ledger, records destruction, intercom authority play.

**Available actions**
- inspect_clock
- inspect_filing_cabinets
- inspect_red_ledger
- take_blank_forms
- use_intercom
- burn_records
- forge_on_site

**Scene text**
> The wall clock is dead at 3:17. Filing cabinets crowd the room like metal teeth. A red attendance ledger lies open to today. Blank excused absence forms are stacked beside carbon paper. The intercom handset leaks a whisper of names, each followed by the word absent.

**Visible investigation targets**
- `wall clock stopped at 3:17`
- `filing cabinets`
- `red attendance ledger`
- `blank excused absence forms`
- `intercom handset whispering names`

**Hidden investigation targets**
- `ledger correction fluid` -> reveals edits by unknown “Monitor” hand

**NPCs/entities present**
- none by default; Voss may enter if angered.

**Action results**
- acquire forms, forge docs, burn anchors, call PA command sequence.

**Flags changed**
- `has_blank_excuse_form`, `has_forged_excuse`, `bell_records_destroyed`, `knows_records_weakness`.

**Checks required**
- Burn quietly: Nerve+Hands DC12; failure adds stress +1 and alerts security.
- Forge on-site: Mind+Archive DC14.
- Intercom command prep: Heart+Presence DC13 grants +2 in Chain-of-Command ending check.

**Possible transitions**
- School Lobby, North Hallway, Basement Bell Chamber (if clue chain found).

---

## LOCATION: Room 103
**Purpose:** Personal threat escalation; Tobin crisis; brass handbell clue/tool.

**Available actions**
- enter_room
- inspect_chalkboard
- speak_tobin
- take_handbell
- hide_and_listen

**Scene text**
> Detention desks face the wall as if punished for looking away. On the chalkboard, names are written under ABSENT in careful block letters. At the bottom: MARA VEY, unfinished, chalk still dusting the tray. Tobin crouches beneath the teacher’s desk, shaking. A brass handbell rests on the front desk beside a broken piece of white chalk.

**Visible investigation targets**
- `detention desks facing wall`
- `chalkboard listing names under ABSENT`
- `player’s name unfinished`
- `Tobin beneath teacher’s desk`
- `brass handbell`

**Hidden investigation targets**
- `chalk handwriting` -> matches ledger correction hand

**NPCs/entities present**
- Tobin (if not already moved), ambient manifestation

**Action results**
- set `player_marked_absent` risk if linger too long.
- can gain `has_brass_handbell` (used as distraction/tool, not weapon).

**Flags changed**
- `saw_absent_chalkboard`, `has_brass_handbell`, possible `player_marked_absent=true` on failed composure.

**Checks required**
- Resist marking panic: Heart+Composure DC13.

**Possible transitions**
- North Hallway, Basement Bell Chamber (via hidden service stair clue).

---

## LOCATION: Basement Bell Chamber
**Purpose:** Final interaction with Bell Monitor; branching endings.

**Available actions**
- final_interaction
- prepare_scene
- attack
- run

**Scene text**
> Old brick arches end in new drywall, as if decades were stapled together. A bronze bell hangs in a steel frame. Its clapper is wrapped in attendance slips tied with office twine. Beside it stands a tall figure in a hall monitor sash, face smooth and pale as a blank detention form.

**Visible investigation targets**
- `old brick arches`
- `modern drywall`
- `bronze bell`
- `steel frame`
- `clapper wrapped in attendance slips`
- `tall figure with hall monitor sash`
- `face like blank detention form`

**Hidden investigation targets**
- `twine knot seal` -> municipal stamp analogue; +1 authority if noticed

**NPCs/entities present**
- Bell Monitor

**Action results**
- branch to endings.

**Flags changed**
- `final_confrontation_started=true`.

**Checks required**
- based on selected resolution method.

**Possible transitions**
- Endings or retreat to North Hallway on successful run.

---

## 5) Interactions

## INTERACTION: Principal Voss
**Trigger conditions:** In School Lobby; Voss present; not in combat.

**Opening text:**
> “This is a school, not a courthouse,” Voss says, fingers on the red folder. “Tell me why you’re here before you scare my staff.”

**Options / checks / outcomes**
- ask for cooperation -> Heart+Empathy DC12
- threaten legal action -> Heart+Presence DC14 (if municipal badge shown, -1 DC)
- show evidence -> Mind+Archive DC12 (needs clues from Hospital/Records)
- ask for excused absence form -> Heart+Presence DC13 (auto success if principal ally)
- distract him -> Nerve+Hands DC11 (gain office key moment)
- attack him -> combat trigger (security response)
- leave -> exit

**Success result**
- Gains one or more: `has_signed_excuse`, `principal_ally`, `office_access_granted`.

**Failure result**
- `angered_principal=true`; later stealth/social DC +2; possible lockdown scene.

**Partial success result**
- Access granted but no signed form OR signed form with condition (escort).

**Flags changed**
- as above.

**Combat trigger:** choosing attack or repeated intimidation after failure.

**Run option:** Leave to exterior/hallway.

---

## INTERACTION: Janitor Remainder
**Trigger conditions:** North Hallway; janitor active.

**Opening text:**
> He does not look up. “Spill in corridor C. No overtime approved. Spill in corridor C.” The patch under his mop is dry.

**Options**
- talk gently -> Heart+Empathy DC11
- ask about accounting -> Mind+Pattern DC13
- inspect bucket -> Nerve+Notice DC12
- give him a new task -> Heart+Presence or Mind+Archive DC14 (needs `has_work_order` OR fabricated order)
- threaten him -> Blood+Menace DC13
- attack him -> combat
- run -> retreat

**Success result**
- learn loop/weakness, set `knows_janitor_task_loop`, maybe `knows_records_weakness`; on task success `janitor_released=true`, `room103_unlocked=true`.

**Failure result**
- `janitor_hostile=true`, stress +1, may trigger combat.

**Partial success result**
- room103 unlocked but janitor not released.

**Combat trigger:** threaten/attack/failure escalation.

**Run option:** to Lobby or Exterior.

---

## INTERACTION: Tobin Hale
**Trigger conditions:** North Hallway or Room 103.

**Opening text:**
> “It rings before it rings,” Tobin whispers. “Everybody hears the loud one. I hear the one that comes first.”

**Options**
- calm him -> Heart+Empathy DC11
- ask what he hears -> Mind+Pattern DC12
- ask about Room 103 -> Heart+Presence DC12
- ask about the bell -> Mind+Logic DC12
- abandon him -> immediate exit, stress +1
- bring him along -> Heart+Composure DC13

**Success result**
- `befriended_tobin=true`, `knows_pre_ring_warning=true`, ally joins.

**Failure result**
- Tobin flees to Room 103; entering triggers fear check.

**Partial success result**
- clue gained but Tobin not recruited.

**Combat trigger:** none direct.

**Run option:** leave conversation.

---

## INTERACTION: Father Lorne
**Trigger conditions:** Church Basement.

**Opening text:**
> “I tried prayers first,” Lorne says. “It answered with paperwork.”

**Options**
- ask about bell -> Mind+Occult DC12
- ask for help -> Heart+Presence DC13
- challenge his fear -> Heart+Faith DC12
- ask for tools -> Mind+Archive DC11
- leave

**Success result**
- `recruited_lorne=true`; gain ally; `knows_records_weakness=true`; `has_fire_source=true`.

**Failure result**
- not recruited; still gives minimal warning clue.

**Partial success result**
- grants occult clue and candles but stays behind.

**Combat trigger:** none.

**Run option:** leave basement.

---

## INTERACTION: Bell Monitor (Final)
**Trigger conditions:** Basement Bell Chamber; confrontation active.

**Opening text:**
> The figure raises a clipboard that has no paper. “State your attendance status.” The bell rope tightens without being touched.

**Options / checks / ending mapping**
- present signed excuse -> if `has_signed_excuse` and `knows_excuse_loophole` => Administrative Victory (auto or DC9 confirm).
- present forged excuse -> Mind+Archive DC15; good forgery +2, weak forgery -2.
  - clean success => Fraudulent Escape
  - weak/tie/fail with substitute target => Someone Else Pays
- argue accounting contradiction -> Mind+Logic or Mind+Pattern DC15; requires 3 core knowledge flags => Procedural Exorcism
- burn attendance slips -> Nerve+Hands or Heart+Composure DC14; requires `has_fire_source` and records weakness => Fire Drill
- command it using school authority -> Heart+Presence DC14; advantage if `principal_ally` or `janitor_released` or `has_work_order` => Chain of Command
- offer yourself in exchange for someone else -> Heart+Faith or Heart+Composure DC13 => Substitution
- attack it -> contested combat (usually unwinnable unless records already destroyed)
- run -> Nerve+Reflex DC13 => Survivor on success, Marked Absent risk on failure

**Success/Failure/Partial**
- Each option routes to ending table.

**Combat trigger:** choosing attack or repeated failed hostile commands.

**Run option:** explicit `run`.

---

## 6) Combat Triggers & Guidance
- **Principal conflict combat:** security/staff scuffle, nonlethal but causes time/stress spikes and lockdown penalties.
- **Janitor combat:** entity uses repetitive slam/mop entangle; defeating physically only disperses briefly unless loop broken.
- **Bell Monitor combat:** while bell schedule intact and records anchored, takes reduced/no lasting damage; each round risks memory attack.
- **Memory attack (Monitor):** opposed by Heart+Composure or ally best (Lorne Faith/Occult may substitute once/round).

---

## 7) Run-Away Options
- Any interaction marked `allow_run=true`.
- Running from final scene can still achieve **Survivor** if successful.
- If command-loss effect currently disables `run`, player must restore via calm action or ally intervention.

---

## 8) Plot Events (Engine Hooks)
```yaml
plot_events:
  - key: bell_pre_echo
    trigger: befriended_tobin and imminent_317
    effect: '+2 on next react/resist check'
    text: 'Tobin flinches a second early: "Now."'

  - key: first_317_ring
    trigger: time >= threshold_317 and not final_resolved and not bell_rang_once
    effect: bell_rang_once=true; apply memory routine

  - key: memory_threshold_1
    trigger: memory_damage >= 1
    effect: disable_command_map_for_scene

  - key: memory_threshold_2
    trigger: memory_damage >= 2
    effect: disable_command_run_for_scene

  - key: memory_threshold_3
    trigger: memory_damage >= 3
    effect: disable_command_talk_or_investigate_until_recover

  - key: memory_threshold_4
    trigger: memory_damage >= 4
    effect: player_marked_absent=true; final checks +2 DC
```

### 3:17 Bell Event Resolution Logic
1. If `has_signed_excuse && knows_excuse_loophole`: no memory damage.
2. Else if forged excuse: roll validation (Archive DC15 modified by forgery quality).
3. Else apply resistance check:
   - base: Heart+Composure DC14
   - Tobin ally: +2 react
   - Lorne ally: may use his best Occult/Faith as secondary (party highest rule)
4. On fail: `memory_damage +1`, `stress +1`.

---

## 9) NPCs and Ally Stats
```yaml
allies:
  ms_ibarra:
    role: teacher, memory victim
    combatant: false
    secondary: { archive: 4, empathy: 3, composure: 3 }
    perk: '+1 Archive when validating school records'

  tobin_hale:
    role: student, pre-ring hearer
    combatant: fragile
    secondary: { notice: 4, instinct: 3, composure: 1 }
    perk: 'pre-ring warning event (+2 react)'

  father_lorne:
    role: failed exorcist
    secondary: { occult: 4, faith: 4, composure: 2 }
    perk: 'can anchor memory defense once per bell event'

  principal_voss:
    role: obstacle/authority
    temporary_ally: true
    secondary: { presence: 4, archive: 3 }
    perk: 'authority validation bonus for command ending'

entities:
  janitor_remainder:
    nature: looping enforcement remnant
    weakness: valid work order reassignment

  bell_monitor:
    nature: institutional predator
    strengths:
      - immunity to normal violence while schedule valid
      - memory and identity attacks
    weaknesses:
      - formal excuse loophole
      - schedule contradiction
      - record anchor destruction
      - valid authority override
```

---

## 10) Skill Check Reference (Suggested DCs)
- Routine clue extraction: DC11-12
- Gaining cooperation under pressure: DC12-13
- Procedural leverage (forgery/contradiction): DC14-15
- Final confrontation actions: DC13-15
- Direct violent solution (discouraged): contested + penalties from traits

Use formula: `1d10 + primary + secondary + modifiers`.

---

## 11) Clue Graph (Compact)
```text
knows_317
  -> North Hallway schedule focus
  -> Bell timing awareness

knows_accounting_period (Records 1987 memo / Janitor accounting line)
  + knows_excuse_loophole (circular / Voss paperwork / forms)
  + knows_records_weakness (Records evidence / Lorne / Janitor bucket)
  -> unlock Procedural Exorcism path

has_signed_excuse + knows_excuse_loophole
  -> Administrative Victory

has_forged_excuse (+ quality)
  -> Fraudulent Escape OR Someone Else Pays

has_fire_source + knows_records_weakness
  -> Fire Drill

principal_ally OR janitor_released OR has_work_order
  -> Chain of Command

offer_self + pass composure/faith
  -> Substitution

run_final pass
  -> Survivor

memory_damage >=4 OR marked_absent + fail_final
  -> Marked Absent
```

---

## 12) Ending Conditions & Text

## ENDING: Administrative Victory
**Conditions:** `has_signed_excuse && knows_excuse_loophole`

**Ending text:**
> You place the signed form beneath the Bell Monitor’s blank face. It stamps the paper with a sound like a closing locker. The rope slackens. Across the school, people remember their own names in one long shuddering breath.

**Mechanical result:** clean win; `memory_damage` stops, school stable.

**Future campaign hook:** Who inserted the 3:17 line in 1987, and why was it scratched out instead of destroyed?

---

## ENDING: Fraudulent Escape
**Conditions:** `has_forged_excuse` + successful forgery validation

**Ending text:**
> The Monitor scans your forged signature and accepts it. You walk out while the bell remains hungry. Tomorrow’s attendance ledger already has one blank line where another name should be.

**Mechanical result:** player survives; unresolved collateral risk.

**Future campaign hook:** A parent reports their child “still in class” but absent from every record.

---

## ENDING: Someone Else Pays
**Conditions:** weak/failed forged excuse and substitute available

**Ending text:**
> The document buckles under scrutiny. The Monitor tilts its head toward the nearest weaker claim. The correction is made in chalk, then in bloodless silence.

**Mechanical result:** partial win; ally or victim lost/marked absent.

**Future campaign hook:** Surviving ally asks Mara to reverse a substitution judgment.

---

## ENDING: Procedural Exorcism
**Conditions:** knows three core clues + successful Logic/Pattern argument

**Ending text:**
> You cite dates, signatures, and an invalid accounting period never ratified by any board. The Monitor freezes mid-gesture. Its sash unthreads into paper strips. Without valid authority, the bell can only hang there—metal, mute, ordinary.

**Mechanical result:** strongest intellectual win; entity dissolved.

**Future campaign hook:** Similar “unratified procedures” surface in other city institutions.

---

## ENDING: Fire Drill
**Conditions:** fire source + records weakness + successful burn check

**Ending text:**
> Flame races through old slips and dry twine. The chamber fills with a bitter paper stink. The Monitor stutters like a jammed announcement, then tears into drifting ash.

**Mechanical result:** win with evidence loss; legal heat on Mara.

**Future campaign hook:** Insurance investigators question how a sealed basement ignited.

---

## ENDING: Chain of Command
**Conditions:** authority support/work order path + successful Presence check

**Ending text:**
> You issue a formal reassignment with the right title, the right room number, and the right tone. The Monitor stamps RECEIVED in red across empty air and turns away to perform its new duty elsewhere.

**Mechanical result:** controlled containment victory.

**Future campaign hook:** Where is “elsewhere,” and who signed the receiving order?

---

## ENDING: Substitution
**Conditions:** player offers self + successful Faith/Composure

**Ending text:**
> “Mark me instead,” you say. The chalk finishes your name. By dawn the school is quiet, and everyone else is present. Your badge remains on a desk nobody can place.

**Mechanical result:** heroic loss; campaign can continue with legacy/investigator successor.

**Future campaign hook:** Mara’s files remain annotated by a handwriting that remembers her.

---

## ENDING: Survivor
**Conditions:** successful final run

**Ending text:**
> You run before the strike. Outside, the air tastes normal again. Behind you, the bell rings once at 3:17 and the windows go dark in sequence.

**Mechanical result:** escape, threat persists.

**Future campaign hook:** Mara forms a task force; return mission planned.

---

## ENDING: Marked Absent
**Conditions:** `memory_damage >= 4` OR (`player_marked_absent` and final failure)

**Ending text:**
> The ledger closes. Conversation steps around the space you occupy. Your flashlight clicks on in an empty hand no one can see.

**Mechanical result:** fail state / character erased from active reality.

**Future campaign hook:** Another investigator finds Mara’s incident forms filled out in tomorrow’s date.

---

## 13) Recommended First-Play Path (Non-Railroad)
- This path does not add or remove locations; it only changes visit order.
- Office -> Records (core procedural clues) -> Hospital (Ibarra + victim proof) -> School Lobby (Voss social route) -> North Hallway (Tobin + Janitor) -> Attendance Office (forms/ledger) -> Bell Chamber.
- Alternate viable opens:
  - Rush School first (high risk, faster tension).
  - Church first for Lorne safety net.
  - Hospital first for empathy path into Voss cooperation.

---

## 14) CLI Implementation Notes
- **Parser nouns:** Ensure investigation targets match concrete nouns in scene text (e.g., `red ledger`, `dry floor patch`, `origami crane`).
- **Synonyms:** Add aliases (`ledger`/`attendance ledger`; `bell`/`bronze bell`).
- **Command loss effects:** Implement temporary disabled command table keyed by `memory_damage` thresholds.
- **Time model:** Increment `time` on major actions; trigger 3:17 event once threshold crossed.
- **Ally stat sharing:** For checks, use highest relevant secondary among Mara + allies.
- **Trait hooks:**
  - `Paper Trail` reroll prompt when eligible.
  - `Claims Logic` auto-grant +2 Pattern after first explicit observation of rule-bound behavior.
  - `Not a Fighter` auto-apply -2 on direct Force unless `scene_prepared=true`.
- **Partial success support:** Preserve tension by advancing scene with cost (stress, flag complications, collateral).
- **Combat balancing:** Emphasize that Bell Monitor absorbs normal damage until procedural weaknesses applied.
