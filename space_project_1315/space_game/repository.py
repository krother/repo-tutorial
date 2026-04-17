import json
from tkinter import SEPARATOR

import base32_lib as base32

from space_game.game import SpaceGame
from space_game.location import Location
from space_game.utils import serialize_game, deserialize_game

import duckdb

con = duckdb.connect()
con.sql("""
CREATE TABLE games (
    id VARCHAR(10) PRIMARY KEY,
    location VARCHAR(100),
    cargo VARCHAR(50),
    crew VARCHAR(100),
    )
""")

LOCATIONS: dict[tuple[str, str], Location] = {}

# test_repository is in the chapters/ folder
# uv run pytest tests/test_repository.py 

def create_game(galaxy_file: str, start_location: str) -> SpaceGame:
    # import base32_lib as base32
    game_id = base32.generate(length=10, checksum=True)

    locations: list[Location] = create_galaxy(galaxy_file)
    for location in locations:
        create_location(game_id, location)

    game = SpaceGame(
        game_id=game_id, 
        location=get_location(game_id, name=start_location),
        get_location=get_location,
    )
    values = serialize_game(game)
    con.sql("INSERT INTO games VALUES (?,?,?,?)",
        params=values)
    return game


def get_game(game_id) -> SpaceGame:
    cursor = con.sql("SELECT * FROM games WHERE id = ?",
                  params=(game_id,))
    result = cursor.fetchall()
    return deserialize_game(result[0], get_location)


def update_game(game: SpaceGame):
    values = serialize_game(game)
    con.sql("UPDATE games SET location=?, cargo=?, crew=? WHERE id=?",
        params=(values[1], values[2], values[3], values[0]))


def create_location(game_id: str, location: Location) -> Location:
    LOCATIONS[(game_id, location.name)] = location
    return location

def get_location(game_id: str, name: str) -> Location:
    return LOCATIONS[(game_id, name)]

def update_location(game_id: str, location: Location) -> None:
    pass

def create_galaxy(filename: str):
    """Loads entire playing environment from a JSON file"""
    # TODO: this will be used for data ingestion
    j = json.load(open(filename, encoding="utf-8"))
    return [Location(**loc) for loc in j]
