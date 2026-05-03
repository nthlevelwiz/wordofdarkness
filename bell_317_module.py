from __future__ import annotations

from engine import (
    AttributeBlock,
    Character,
    GameState,
    Location,
    Scene,
    InvestigationTarget,
    NPC,
    Ally,
    Engine,
)


def _set_flag(flag: str, text: str):
    def _fn(engine: Engine, state: GameState, scene: Scene) -> str:
        state.flags.add(flag)
        return text
    return _fn


def _forge_excuse(engine: Engine, state: GameState, scene: Scene) -> str:
    result = __import__("engine").roll_check(state.player, "mind", "archive", 15)
    state.flags.add("has_forged_excuse")
    if result["margin"] >= 1:
        state.flags.add("forged_excuse_quality_good")
        return "You forge a clean excuse form. It looks convincing."
    state.flags.add("forged_excuse_quality_weak")
    return "The forgery passes at a glance, but the signature is shaky."


def build_bell_317_state() -> GameState:
    mara = Character(
        name="Mara Vey",
        description="Municipal occult claims investigator.",
        attributes=AttributeBlock(
            primary={"mind": 4, "heart": 3, "blood": 1, "nerve": 2},
            secondary={
                "logic": 4, "archive": 3, "pattern": 5, "occult": 2,
                "empathy": 3, "presence": 2, "composure": 4, "faith": 1,
                "force": 1, "endurance": 2, "menace": 1, "instinct": 2,
                "notice": 3, "reflex": 2, "stealth": 1, "hands": 2,
            },
        ),
        traits=[
            "Paper Trail",
            "Not a Fighter",
            "Claims Logic",
        ],
        inventory=[
            "Cheap flashlight",
            "Municipal badge",
            "Broken voice recorder",
            "Packet of carbon-copy incident forms",
            "Box cutter",
            "Lighter",
        ],
        current_location="municipal occult office",
        current_scene="office_start",
    )

    # Allies/NPCs
    mara.allies = [
        Ally("Ms. Ibarra", "Teacher losing memories.", AttributeBlock({}, {"archive": 4, "empathy": 3, "composure": 3})),
        Ally("Tobin Hale", "Student who hears the pre-ring.", AttributeBlock({}, {"notice": 4, "instinct": 3, "composure": 1})),
        Ally("Father Lorne", "Failed exorcist.", AttributeBlock({}, {"occult": 4, "faith": 4, "composure": 2})),
    ]

    scenes = {
        "office_start": Scene(
            key="office_start",
            location="municipal occult office",
            description="Fluorescent lights buzz over a folder marked SCHOOL INCIDENT. The timestamp 3:17 appears on each page.",
            visible_targets={
                "case folder": InvestigationTarget("case folder", ["folder"], "The case log repeats a daily unscheduled bell at 3:17.", _set_flag("knows_317", "You note the 3:17 anomaly and open travel options.")),
            },
            actions={
                "to records": "records_main",
                "to hospital": "hospital_main",
                "to church": "church_main",
                "to school": "school_exterior",
            },
        ),
        "records_main": Scene(
            key="records_main",
            location="downtown records office",
            description="A clerk watches from behind plexiglass. A SCHOOL BOARD 1987 box sags under a leaking tile beside a locked cabinet.",
            visible_targets={
                "school board 1987 box": InvestigationTarget("school board 1987 box", ["1987 box"], "Margin notes define a hidden 3:17 accounting period.", _set_flag("knows_accounting_period", "You confirm the invalid 3:17 accounting period.")),
                "locked cabinet": InvestigationTarget("locked cabinet", ["cabinet"], "Blank excused forms and disciplinary circulars are filed inside.", _set_flag("knows_excuse_loophole", "You find the formal-excuse loophole and pocket blank forms.")),
                "fire inspection reports": InvestigationTarget("fire inspection reports", ["reports"], "Records and schedules are listed as control documents for bell systems.", _set_flag("knows_records_weakness", "You identify records as ritual anchors.")),
                "copier": InvestigationTarget("copier", [], "The copier warms up with a cough.", _forge_excuse),
            },
            actions={"to school": "school_exterior", "to office": "office_start"},
        ),
        "hospital_main": Scene(
            key="hospital_main",
            location="hospital",
            description="A teacher stares blankly behind a curtain. A visitor badge reads IBARRA, E. A folded bell schedule sits on a bedside table.",
            visible_targets={
                "visitor badge": InvestigationTarget("visitor badge", ["ibarra"], "Ms. Ibarra confirms victims are marked absent before memory loss.", _set_flag("befriended_ibarra", "Ibarra agrees to help validate records.")),
                "folded bell schedule": InvestigationTarget("folded bell schedule", ["origami crane"], "The final printed line was scratched out, but pressure marks show 3:17."),
            },
            actions={"to school": "school_exterior", "to office": "office_start"},
        ),
        "church_main": Scene(
            key="church_main",
            location="church basement",
            description="Emergency candles sit beneath a child's drawing of a bell with teeth. Father Lorne waits by folding chairs.",
            visible_targets={
                "father lorne": InvestigationTarget("father lorne", ["lorne"], "He warns that records and authority bind the entity.", _set_flag("recruited_lorne", "Lorne joins your effort and gives you consecrated lamp oil.")),
                "emergency candles": InvestigationTarget("emergency candles", ["candles"], "They'll burn ledgers quickly.", _set_flag("has_fire_source", "You secure an additional fire source.")),
            },
            actions={"to school": "school_exterior", "to office": "office_start"},
        ),
        "school_exterior": Scene(
            key="school_exterior",
            location="school exterior",
            description="Silent students stand in second-floor windows. Front doors, side gate, and office entrance wait under a tracking camera.",
            visible_targets={
                "security camera": InvestigationTarget("security camera", ["camera"], "Its feed routes toward the attendance office.")
            },
            actions={"enter lobby": "school_lobby", "take side gate": "north_hallway"},
        ),
        "school_lobby": Scene(
            key="school_lobby",
            location="school lobby / principal voss",
            description="Principal Voss blocks the attendance office door, hand on a red folder while the PA clicks overhead.",
            active_people=["Principal Voss"],
            visible_targets={
                "principal voss": InvestigationTarget("principal voss", ["voss"], "He can sign formal excuse slips if convinced.", _set_flag("has_signed_excuse", "After reviewing your evidence, Voss signs a formal excused absence.")),
                "attendance office door": InvestigationTarget("attendance office door", ["door"], "The office contains ledgers and forms.", _set_flag("office_access_granted", "Voss unlocks the attendance office.")),
            },
            actions={"to hallway": "north_hallway", "to attendance": "attendance_office"},
        ),
        "north_hallway": Scene(
            key="north_hallway",
            location="north hallway",
            description="Rainwater and toner scent the hall. A janitor mops a dry patch. A student at lockers covers his ears before each click.",
            active_people=["Tobin Hale", "Janitor Remainder"],
            visible_targets={
                "paper bell schedule": InvestigationTarget("paper bell schedule", ["schedule"], "The final line was scratched out after 3:17."),
                "student near lockers": InvestigationTarget("student near lockers", ["tobin"], "Tobin hears a pre-ring one second early.", _set_flag("befriended_tobin", "Tobin agrees to warn you before bell pulses.")),
                "janitor": InvestigationTarget("janitor", ["dry floor patch"], "His bucket holds a stale work order: corridor C, indefinite.", _set_flag("has_work_order", "You recover the work order and learn the task loop.")),
            },
            actions={"to room 103": "room_103", "to attendance": "attendance_office", "to lobby": "school_lobby"},
        ),
        "attendance_office": Scene(
            key="attendance_office",
            location="attendance office",
            description="A wall clock is stopped at 3:17. Filing cabinets crowd a red attendance ledger. The intercom whispers names followed by absent.",
            visible_targets={
                "red attendance ledger": InvestigationTarget("red attendance ledger", ["ledger"], "Every victim was marked absent before symptoms.", _set_flag("knows_records_weakness", "You confirm the ledger is an anchor.")),
                "blank excused absence forms": InvestigationTarget("blank excused absence forms", ["blank forms"], "Carbon-copy forms for formal excuse processing.", _set_flag("has_blank_excuse_form", "You take blank forms for contingency use.")),
                "intercom handset": InvestigationTarget("intercom handset", ["intercom"], "A command channel tied to authority routing."),
            },
            actions={"to room 103": "room_103", "to bell chamber": "bell_chamber", "to hallway": "north_hallway"},
        ),
        "room_103": Scene(
            key="room_103",
            location="room 103",
            description="Detention desks face the wall. A chalkboard lists ABSENT names, ending with MARA VEY unfinished. A brass handbell rests on the desk.",
            visible_targets={
                "chalkboard": InvestigationTarget("chalkboard", ["absent"], "Your name is being written under ABSENT.", _set_flag("player_marked_absent", "You feel reality trying to file you away.")),
                "brass handbell": InvestigationTarget("brass handbell", ["handbell"], "A manual override bell used before automated schedules.", _set_flag("has_brass_handbell", "You take the brass handbell.")),
            },
            actions={"to bell chamber": "bell_chamber", "to hallway": "north_hallway"},
        ),
        "bell_chamber": Scene(
            key="bell_chamber",
            location="basement bell chamber",
            description="Old brick arches frame a bronze bell. Attendance slips wrap the clapper. A tall hall-monitor figure waits with a blank paper face.",
            entities=["Bell Monitor"],
            visible_targets={
                "bell monitor": InvestigationTarget("bell monitor", ["monitor"], "It asks your attendance status.", _set_flag("final_confrontation_started", "Final interaction available: signed excuse, forged excuse, contradiction, burn, command, sacrifice, attack, or run.")),
                "clapper wrapped in attendance slips": InvestigationTarget("clapper wrapped in attendance slips", ["attendance slips"], "Destroying slips may weaken it.", _set_flag("bell_records_destroyed", "The slips tear and burn; the chamber shudders.")),
            },
            exits={"retreat": "north_hallway"},
        ),
    }

    locations = {
        "municipal occult office": Location("municipal occult office", "Municipal Occult Office", "Starting location", ["office_start"]),
        "downtown records office": Location("downtown records office", "Downtown Records Office", "Records and forms", ["records_main"]),
        "hospital": Location("hospital", "Hospital", "Victim interviews", ["hospital_main"]),
        "church basement": Location("church basement", "Church Basement", "Occult consultation", ["church_main"]),
        "school exterior": Location("school exterior", "School Exterior", "Entry choices", ["school_exterior"]),
        "school lobby / principal voss": Location("school lobby / principal voss", "School Lobby / Principal Voss", "Authority route", ["school_lobby"]),
        "north hallway": Location("north hallway", "North Hallway", "Main investigation", ["north_hallway"]),
        "attendance office": Location("attendance office", "Attendance Office", "Ledgers and forms", ["attendance_office"]),
        "room 103": Location("room 103", "Room 103", "Detention horror", ["room_103"]),
        "basement bell chamber": Location("basement bell chamber", "Basement Bell Chamber", "Final confrontation", ["bell_chamber"]),
    }

    state = GameState(player=mara, locations=locations, scenes=scenes)
    state.flags.update({"has_fire_source"})
    state.npcs = {
        "principal voss": NPC("Principal Voss", "Protective administrator."),
        "janitor remainder": NPC("Janitor Remainder", "Task-loop entity mopping a dry patch."),
        "bell monitor": NPC("Bell Monitor", "Institutional enforcement entity."),
    }
    return state


if __name__ == "__main__":
    Engine(build_bell_317_state()).run_repl()
