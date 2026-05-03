from __future__ import annotations

import json
import random
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Callable, Dict, List, Optional, Set, Tuple, Union


PRIMARY_ATTRS = ("mind", "heart", "blood", "nerve")
SECONDARY_ATTRS = (
    "logic", "archive", "pattern", "occult",
    "empathy", "presence", "composure", "faith",
    "force", "endurance", "menace", "instinct",
    "notice", "reflex", "stealth", "hands",
)

DIFFICULTIES = {
    "easy": 9,
    "normal": 12,
    "hard": 15,
    "extreme": 18,
    "supernatural": 21,
}


@dataclass
class AttributeBlock:
    primary: Dict[str, int]
    secondary: Dict[str, int]

    def get_primary(self, name: str) -> int:
        return self.primary.get(name.lower(), 0)

    def get_secondary(self, name: str) -> int:
        return self.secondary.get(name.lower(), 0)


@dataclass
class Character:
    name: str
    description: str
    attributes: AttributeBlock
    traits: List[str] = field(default_factory=list)
    inventory: List[str] = field(default_factory=list)
    allies: List["Ally"] = field(default_factory=list)
    flags: Set[str] = field(default_factory=set)
    health: int = 10
    stress: int = 0
    current_location: str = "downtown"
    current_scene: str = "downtown_street"


@dataclass
class Ally:
    name: str
    description: str
    attributes: AttributeBlock
    traits: List[str] = field(default_factory=list)


@dataclass
class NPC:
    name: str
    description: str


@dataclass
class Entity:
    name: str
    description: str
    attributes: AttributeBlock
    health: int = 8
    stress: int = 0
    tags: Set[str] = field(default_factory=set)


@dataclass
class Clue:
    key: str
    text: str


@dataclass
class PlotEvent:
    key: str
    text: str


@dataclass
class InvestigationTarget:
    key: str
    aliases: List[str]
    description: str
    on_investigate: Optional[Callable[["Engine", "GameState", "Scene"], str]] = None


@dataclass
class InteractionOption:
    key: str
    text: str
    primary: Optional[str] = None
    secondary: Optional[str] = None
    difficulty: Optional[int] = None
    modifiers: int = 0
    on_success: Optional[Callable[["Engine", "GameState"], str]] = None
    on_failure: Optional[Callable[["Engine", "GameState"], str]] = None


@dataclass
class Interaction:
    key: str
    title: str
    description: str
    participants: List[str]
    options: List[InteractionOption]
    allow_run: bool = True


@dataclass
class CombatEncounter:
    key: str
    enemy: Entity
    allow_escape: bool = True


@dataclass
class Scene:
    key: str
    location: str
    description: str
    active_people: List[str] = field(default_factory=list)
    entities: List[str] = field(default_factory=list)
    visible_targets: Dict[str, InvestigationTarget] = field(default_factory=dict)
    hidden_targets: Dict[str, InvestigationTarget] = field(default_factory=dict)
    clues: Dict[str, Clue] = field(default_factory=dict)
    plot_events: Dict[str, PlotEvent] = field(default_factory=dict)
    exits: Dict[str, str] = field(default_factory=dict)
    actions: Dict[str, str] = field(default_factory=dict)


@dataclass
class Location:
    key: str
    name: str
    description: str
    scene_keys: List[str] = field(default_factory=list)
    actions: Dict[str, str] = field(default_factory=dict)


@dataclass
class GameState:
    player: Character
    locations: Dict[str, Location]
    scenes: Dict[str, Scene]
    npcs: Dict[str, NPC] = field(default_factory=dict)
    entities: Dict[str, Entity] = field(default_factory=dict)
    interactions: Dict[str, Interaction] = field(default_factory=dict)
    flags: Set[str] = field(default_factory=set)
    discovered_clues: Set[str] = field(default_factory=set)
    temporary_commands: Set[str] = field(default_factory=set)

    def current_scene(self) -> Scene:
        return self.scenes[self.player.current_scene]


def normalize(text: str) -> str:
    return " ".join(text.strip().lower().split())


def roll_check(character_or_party: Union[Character, List[Character], Tuple[Character, ...]],
               primary: str,
               secondary: str,
               difficulty: int,
               modifiers: int = 0) -> Dict[str, Union[str, int]]:
    if isinstance(character_or_party, Character):
        party = [character_or_party] + list(character_or_party.allies)
    else:
        party = list(character_or_party)

    best_primary = max(c.attributes.get_primary(primary) for c in party)
    best_secondary = max(c.attributes.get_secondary(secondary) for c in party)
    die = random.randint(1, 10)
    total = die + best_primary + best_secondary + modifiers
    margin = total - difficulty

    if margin < 0:
        result = "failure"
    elif margin == 0:
        result = "tie/complication"
    elif margin <= 2:
        result = "weak success"
    elif margin <= 5:
        result = "clean success"
    else:
        result = "strong success"

    return {
        "die": die,
        "primary": best_primary,
        "secondary": best_secondary,
        "modifiers": modifiers,
        "total": total,
        "difficulty": difficulty,
        "margin": margin,
        "result": result,
    }


class Engine:
    def __init__(self, state: GameState):
        self.state = state
        self.running = True

    def print_scene(self) -> None:
        scene = self.state.current_scene()
        print(f"\n[{scene.location.title()}] {scene.key}")
        print(scene.description)
        if scene.active_people:
            print("People:", ", ".join(scene.active_people))
        if scene.entities:
            print("Entities:", ", ".join(scene.entities))
        if scene.visible_targets:
            print("Investigate:", ", ".join(scene.visible_targets.keys()))
        if scene.actions:
            print("Actions:", ", ".join(scene.actions.keys()))
        if scene.exits:
            print("Exits:", ", ".join(scene.exits.keys()))

    def cmd_help(self) -> None:
        print("Commands: help, stats, inventory, allies, locations, go <location>, action <name>, investigate <target>, talk <name>, run, save [file], load [file], quit")

    def cmd_stats(self) -> None:
        p = self.state.player
        print(f"{p.name}: HP {p.health} Stress {p.stress}")
        print("Primary:", p.attributes.primary)
        print("Secondary:", p.attributes.secondary)
        print("Traits:", ", ".join(p.traits))

    def cmd_investigate(self, raw_target: str) -> None:
        scene = self.state.current_scene()
        key = normalize(raw_target)
        match = None
        for target in scene.visible_targets.values():
            if key == normalize(target.key) or key in [normalize(a) for a in target.aliases]:
                match = target
                break
        if not match:
            print("You find nothing by that name here.")
            return
        print(match.description)
        if match.on_investigate:
            print(match.on_investigate(self, self.state, scene))

    def cmd_action(self, raw_action: str) -> None:
        scene = self.state.current_scene()
        action = normalize(raw_action)
        if action not in scene.actions:
            print("No such action in this scene.")
            return
        self.state.player.current_scene = scene.actions[action]
        self.print_scene()

    def cmd_go(self, raw_location: str) -> None:
        loc_key = normalize(raw_location)
        loc = self.state.locations.get(loc_key)
        if not loc:
            print("Unknown location.")
            return
        self.state.player.current_location = loc_key
        self.state.player.current_scene = loc.scene_keys[0]
        self.print_scene()

    def cmd_talk(self, raw_name: str) -> None:
        scene = self.state.current_scene()
        who = normalize(raw_name)
        if who not in [normalize(n) for n in scene.active_people]:
            print("No one by that name is here.")
            return
        print(f"You speak with {raw_name}. They seem uneasy but cooperative.")

    def cmd_run(self) -> None:
        scene = self.state.current_scene()
        if "retreat" in scene.exits:
            self.state.player.current_scene = scene.exits["retreat"]
            print("You flee.")
            self.print_scene()
        else:
            print("No immediate route to run.")

    def save(self, filename: str = "savegame.json") -> None:
        p = self.state.player
        payload = {
            "player": {
                "name": p.name,
                "description": p.description,
                "attributes": {"primary": p.attributes.primary, "secondary": p.attributes.secondary},
                "traits": p.traits,
                "inventory": p.inventory,
                "allies": [asdict(a) for a in p.allies],
                "flags": list(p.flags),
                "health": p.health,
                "stress": p.stress,
                "current_location": p.current_location,
                "current_scene": p.current_scene,
            },
            "flags": list(self.state.flags),
            "discovered_clues": list(self.state.discovered_clues),
        }
        Path(filename).write_text(json.dumps(payload, indent=2), encoding="utf-8")
        print(f"Saved to {filename}")

    def load(self, filename: str = "savegame.json") -> None:
        data = json.loads(Path(filename).read_text(encoding="utf-8"))
        p = data["player"]
        self.state.player.name = p["name"]
        self.state.player.description = p["description"]
        self.state.player.attributes = AttributeBlock(primary=p["attributes"]["primary"], secondary=p["attributes"]["secondary"])
        self.state.player.traits = p["traits"]
        self.state.player.inventory = p["inventory"]
        self.state.player.flags = set(p["flags"])
        self.state.player.health = p["health"]
        self.state.player.stress = p["stress"]
        self.state.player.current_location = p["current_location"]
        self.state.player.current_scene = p["current_scene"]
        self.state.flags = set(data.get("flags", []))
        self.state.discovered_clues = set(data.get("discovered_clues", []))
        print(f"Loaded {filename}")
        self.print_scene()

    def run_repl(self) -> None:
        self.print_scene()
        self.cmd_help()
        while self.running:
            try:
                raw = input("\n> ").strip()
            except EOFError:
                print("\nGoodbye.")
                break
            if not raw:
                continue
            parts = raw.split(maxsplit=1)
            cmd = normalize(parts[0])
            arg = parts[1] if len(parts) > 1 else ""
            try:
                if cmd == "help":
                    self.cmd_help()
                elif cmd == "stats":
                    self.cmd_stats()
                elif cmd == "inventory":
                    print("Inventory:", ", ".join(self.state.player.inventory) or "(empty)")
                elif cmd == "allies":
                    print("Allies:", ", ".join(a.name for a in self.state.player.allies) or "(none)")
                elif cmd == "locations":
                    print("Locations:", ", ".join(self.state.locations.keys()))
                elif cmd == "go":
                    self.cmd_go(arg)
                elif cmd == "action":
                    self.cmd_action(arg)
                elif cmd == "investigate":
                    self.cmd_investigate(arg)
                elif cmd == "talk":
                    self.cmd_talk(arg)
                elif cmd == "run":
                    self.cmd_run()
                elif cmd == "save":
                    self.save(arg or "savegame.json")
                elif cmd == "load":
                    self.load(arg or "savegame.json")
                elif cmd == "quit":
                    print("Quitting.")
                    self.running = False
                else:
                    print("Unknown command. Type 'help'.")
            except Exception as exc:
                print(f"Error: {exc}")


def build_demo_state() -> GameState:
    mara = Character(
        name="Mara Vey",
        description="Former city claims adjuster investigating impossible liability events.",
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
            "Paper Trail: once per scene, reroll Archive or Pattern on institutional records.",
            "Not a Fighter: -2 on direct Force attacks unless prepared.",
            "Claims Logic: +2 Pattern after observing rule-bound behavior once.",
        ],
        inventory=["Cheap flashlight", "Municipal badge", "Broken voice recorder", "Carbon-copy incident forms", "Box cutter", "Lighter"],
        current_location="downtown",
        current_scene="downtown_street",
    )

    def inspect_trophy(engine: Engine, state: GameState, scene: Scene) -> str:
        clue = Clue("school_emblem", "A water-damaged emblem repeats the same date: 10/13.")
        scene.clues[clue.key] = clue
        state.discovered_clues.add(clue.key)
        hidden = scene.hidden_targets.pop("room 103 ledger", None)
        if hidden:
            scene.visible_targets[hidden.key] = hidden
        return "You find a clue and a hidden ledger slot behind cracked glass."

    downtown_scene = Scene(
        key="downtown_street",
        location="downtown",
        description="The boulevard is damp and too quiet. A bus map hums under flickering light.",
        active_people=["night janitor"],
        visible_targets={
            "bus map": InvestigationTarget("bus map", ["map"], "Routes are marked, but one line is erased nightly."),
            "storm drain": InvestigationTarget("storm drain", ["drain"], "Rainwater circles despite no current storm."),
        },
        actions={"inspect alley": "downtown_alley"},
        exits={"retreat": "downtown_street"},
    )
    downtown_alley = Scene(
        key="downtown_alley",
        location="downtown",
        description="The alley smells like rainwater and copier toner. A trophy case stands cracked beside Room 103 signage.",
        visible_targets={
            "hallway": InvestigationTarget("hallway", ["alley"], "Narrow and lined with peeling school notices."),
            "rainwater": InvestigationTarget("rainwater", [], "It beads uphill for a second before falling."),
            "copier toner": InvestigationTarget("copier toner", ["toner"], "Fresh residue leads to a locked service hatch."),
            "trophy case": InvestigationTarget("trophy case", ["case"], "The glass is cracked inward.", on_investigate=inspect_trophy),
            "room 103": InvestigationTarget("room 103", ["103"], "A painted arrow points nowhere.")
        },
        hidden_targets={
            "room 103 ledger": InvestigationTarget("room 103 ledger", ["ledger"], "Detentions list names that don't exist in records.")
        },
        exits={"retreat": "downtown_street"},
    )

    locations = {
        "downtown": Location("downtown", "Downtown", "Central district", ["downtown_street"]),
        "school": Location("school", "School", "Silent campus", ["downtown_alley"]),
        "hospital": Location("hospital", "Hospital", "Fluorescent corridors", ["downtown_street"]),
        "village edge": Location("village edge", "Village Edge", "Outskirts", ["downtown_street"]),
        "apartments": Location("apartments", "Apartments", "Concrete towers", ["downtown_street"]),
        "church": Location("church", "Church", "Wood and candle wax", ["downtown_street"]),
        "industrial zone": Location("industrial zone", "Industrial Zone", "Factories", ["downtown_street"]),
        "subway": Location("subway", "Subway", "Echoing tunnels", ["downtown_street"]),
    }

    scenes = {downtown_scene.key: downtown_scene, downtown_alley.key: downtown_alley}
    return GameState(player=mara, locations=locations, scenes=scenes)


if __name__ == "__main__":
    engine = Engine(build_demo_state())
    engine.run_repl()
