import json

from space_game.game import SpaceGame
from space_game.location import Location


GAMES: dict[str, SpaceGame] = {}
LOCATIONS: dict[tuple[str, str], Location] = {}

# test_repository is in the chapters/ folder
# uv run pytest tests/test_repository.py 

def create_game(galaxy_file: str, start_location: str) -> SpaceGame:
    game_id = "1"
    locations: list[Location] = create_galaxy(galaxy_file)
    for location in locations:
        create_location(game_id, location)

    game = SpaceGame(
        game_id=game_id, 
        location=get_location(game_id, name=start_location),
        get_location=get_location,
    )
    GAMES[game_id] = game
    return game


def get_game(game_id) -> SpaceGame:
    return GAMES[game_id]

def create_location(game_id: str, location: Location) -> Location:
    LOCATIONS[(game_id, location.name)] = location
    return location

def get_location(game_id: str, name: str) -> Location:
    return LOCATIONS[(game_id, name)]


def create_galaxy(filename: str):
    """Loads entire playing environment from a JSON file"""
    # TODO: this will be used for data ingestion
    j = json.load(open(filename, encoding="utf-8"))
    return [Location(**loc) for loc in j]
