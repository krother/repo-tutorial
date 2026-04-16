"""
A service-level module that serves the main use case: plaing the game.
"""
import os

from space_game.lang import LANG
from space_game.location import create_galaxy
from space_game.game import SpaceGame
from space_game.config import DATA_PATH
from space_game.dto import GameData, LocationData


GAMES = {}  # TODO: move this to a database asap


def _get_game_data(game_id, game):
    return GameData(
        game_id=game_id,
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


def start_game() -> GameData:
    galaxy = create_galaxy(os.path.join(DATA_PATH, f"galaxy_{LANG}.json"))
    game = SpaceGame(location=galaxy["Pandalor"])  # core business object
    game_id = "1"
    GAMES[game_id] = game
    return _get_game_data(game_id, game)

    
def execute_command(game_id: str, command: str) -> GameData:
    """call the callback function given by 'command'"""
    game = GAMES[game_id]
    for cmd in game.get_commands():
        if cmd.name == command:
            cmd.callback()
            break
    return _get_game_data(game_id, game)
