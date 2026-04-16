"""
Domain object: Locations

Locations are planets and other places in the game.
They contain puzzles that can be triggered by certain actions.
"""
import json
from typing import Optional

from pydantic import BaseModel


class ActionTrigger(BaseModel):
    """
    Conditions and effects of puzzles at a location
    """

    action_name: str|None = None
    require_good: str|None = None
    require_crew_member: str|None = None
    activated_message: str|None = None
    not_activated_message: str|None = None
    activate_clear_cargo: str|None = None
    activate_gain_crew_member: str|None = None
    activate_gain_cargo: str|None = None
    activate_gain_connection: str|None = None
    deactivate: bool = True


class Location(BaseModel):
    """
    Planets, spaceships and special places on the ground
    """

    galaxy: dict
    name: str
    description: str
    image: str
    type: str = "planet"
    connected_names: list[str]
    connected_locs: list["Location"] = []
    resources: list[str] = []
    active: bool = True
    trigger: ActionTrigger

    def __repr__(self) -> str:
        return f"<{self.name}: {self.type}; provides {self.resources}; {self.active}>"

    def add_connection(self, location) -> None:
        self.connected_locs.append(location)

    def activate(self, game):
        if self.trigger.deactivate:
            self.active = False
        if self.trigger.activate_clear_cargo:
            game.cargo = ""
        if self.trigger.activate_gain_crew_member:
            game.crew.append(self.trigger.activate_gain_crew_member)
        if self.trigger.activate_gain_cargo:
            game.cargo = self.trigger.activate_gain_cargo
        if self.trigger.activate_gain_connection:
            self.connected_names.append(self.trigger.activate_gain_connection)
            self.connected_locs.append(self.galaxy[self.trigger.activate_gain_connection])

    def contact(self, game):
        if self.active:
            if (self.trigger.require_good is None or (game.cargo == self.trigger.require_good)) and (
                self.trigger.require_crew_member is None or (self.trigger.require_crew_member in game.crew)
            ):
                self.activate(game)
                game.message = self.trigger.activated_message
            else:
                game.message = self.trigger.not_activated_message


def create_galaxy(filename: str):
    """Loads entire playing environment from a JSON file"""
    j = json.load(open(filename, encoding="utf-8"))
    galaxy = {}

    locs = [Location(galaxy=galaxy, **loc) for loc in j]
    # builds connection graph
    for location in locs:
        location.galaxy = galaxy
        galaxy[location.name] = location
        location.connected_locs = []
        for targetname in location.connected_names:
            target = None
            for p in locs:
                if p.name == targetname:
                    target = p
            if target is None:
                raise ValueError(f"connection not found when building galaxy for '{targetname}'")
            location.add_connection(target)

    return galaxy
