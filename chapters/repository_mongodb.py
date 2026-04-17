import os

import base32_lib as base32
from pymongo import MongoClient

import space_game.config
from space_game.location import Location
from space_game.game import SpaceGame


conn = MongoClient()
db = conn.get_database(os.getenv("MONGODB_DATABASE"))


def create_game(galaxy_file: str, start_location: str) -> SpaceGame:
    game_id = base32.generate(length=10, checksum=True)
    game = SpaceGame(
        game_id=game_id,
        location=location,
    )
    j = game.model_dump()
    result = db.games.insert_one(j)
    # result.inserted_id
    return game


def get_game(game_id) -> SpaceGame:
    result = db.games.findOne({"game_id": game_id})
    return SpaceGame(**result)  # includes database id


def update_game(game_id: str, game: SpaceGame) -> SpaceGame:
    db.games.update_one({"game_id": game_id}, {"$set": game})
    return game


def get_location(game_id: str, name: str) -> Location:
    result = db.locations.find_one({"game_id": game_id, "name": name})
    return Location(**result)  # includes database id


def add_location(game_id: str, location: Location) -> Location:
    j = location.model_dump()
    j["game_id"] = "default"
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
