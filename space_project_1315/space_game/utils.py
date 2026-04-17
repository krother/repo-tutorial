from typing import Callable

from space_game.game import SpaceGame

SEPARATOR = ";"

def serialize_game(game: SpaceGame) -> tuple[str, str, str, str]:
    return (
        game.game_id, 
        game.location.name,
        game.cargo,
        SEPARATOR.join(game.crew),
    )

def deserialize_game(values: list[str], get_location: Callable) -> SpaceGame:
    return SpaceGame(
        game_id = values[0],
        location = get_location(values[0], values[1]),
        cargo = values[2],
        crew = values[3].split(SEPARATOR),
        get_location = get_location,
    )
