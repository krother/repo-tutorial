import pytest
import sys
import os

from space_game import config
os.environ["REPO_TYPE"] = "dict"

@pytest.fixture(autouse=True) # , scope="session"
def clear_database():
    if os.getenv("REPO_TYPE") == "mongodb":
        from space_game.repository import repo_used
        repo_used.db.games.delete_many({})
        repo_used.db.locations.delete_many({})
    #print("DELETED EVERYTHING")
    #print("DELETE DONE!", file=sys.stderr)
