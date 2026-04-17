import os
import json

import base32_lib as base32
from pymongo import MongoClient

import space_game.config
from space_game.location import Location
from space_game.game import SpaceGame
from space_game.errors import LocationNotFound

conn = MongoClient()
db = conn.get_database(os.getenv("MONGODB_DATABASE"))


def create_galaxy(filename: str):
    """Loads entire playing environment from a JSON file"""
    # TODO: this will be used for data ingestion
    j = json.load(open(filename, encoding="utf-8"))
    return [Location(**loc) for loc in j]


def create_game(galaxy_file: str, start_location: str) -> SpaceGame:
    game_id = base32.generate(length=10, checksum=True)

    locations: list[Location] = create_galaxy(galaxy_file)
    for location in locations:
        create_location(game_id, location)

    game = SpaceGame(
        game_id=game_id,
        location=get_location(game_id, start_location),
        get_location=get_location,
    )
    j = game.model_dump()
    j.pop("get_location")
    result = db.games.insert_one(j)
    # result.inserted_id
    return game


def get_game(game_id) -> SpaceGame:
    result = db.games.find_one({"game_id": game_id})
    result["get_location"] = get_location
    return SpaceGame(**result)  # includes database id


def update_game(game: SpaceGame) -> SpaceGame:
    j = game.model_dump()
    j.pop("get_location")
    db.games.update_one({"game_id": game.game_id}, {"$set": j})
    return game


LOCATION_CACHE = {}

def get_location(game_id: str, name: str) -> Location:
    if (game_id, name) in LOCATION_CACHE:
        return LOCATION_CACHE[(game_id, name)]
    result = db.locations.find_one({"game_id": game_id, "name": name})
    if result is not None:
        loc = Location(**result)  # includes database id
        LOCATION_CACHE[(game_id, name)] = loc
        return loc
    raise LocationNotFound(f"no location {name} in game {game_id}")


def create_location(game_id: str, location: Location) -> Location:
    j = location.model_dump()
    j["game_id"] = game_id
    db.locations.insert_one(j)
    return location


def update_location(game_id: str, location: Location) -> Location:
    j = location.model_dump()
    db.locations.update_one({"game_id": game_id, "name": location.name}, {"$set": j})
    return location


def delete_location(game_id: str, name: str) -> None:
    db.locations.delete_one({"game_id": game_id, "name": name})


def add_location_batch(game_id: str, locations: list[Location]) -> None:
    data = []
    for loc in locations:
        j = loc.model_dump()
        j["game_id"] = game_id
        data.append(j)
    db.locations.insert_many(data)