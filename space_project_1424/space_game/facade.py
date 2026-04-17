"""
A service-level module that serves the main use case: plaing the game.
"""
import os

from space_game.lang import LANG
from space_game.config import DATA_PATH
from space_game.dto import GameData, LocationData
from space_game.repository import create_game, get_game, update_game, update_location


def _get_game_data(game):
    return GameData(
        game_id=game.game_id,
        location=LocationData(
            name=game.location.name,
            image=game.location.image,
            description=game.location.description,
        ),
        cargo=game.cargo,
        crew=[str(s) for s in game.crew],
        commands=[cmd.name for cmd in game.get_commands()],
        message=game.message,
        solved=game.solved,  # added
    )


def start_game(start_location="Pandalor") -> GameData:
    fn = os.path.join(DATA_PATH, f"galaxy_{LANG}.json")
    game = create_game(galaxy_file=fn, start_location=start_location)
    return _get_game_data(game)

    
def execute_command(game_id: str, command: str) -> GameData:
    """call the callback function given by 'command'"""
    game = get_game(game_id)
    for cmd in game.get_commands():
        if cmd.name == command:
            cmd.callback()
            break
    update_game(game)
    update_location(game.game_id, game.location)
    return _get_game_data(game)
