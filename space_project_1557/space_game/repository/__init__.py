
import os

repo = os.getenv("REPO_TYPE")

if repo == "duckdb":
    from space_game.repository import repository_duckdb as repo_used
if repo == "mongodb":
    from space_game.repository import repository_mongodb as repo_used
if repo == "dict":
    from space_game.repository import repository_dict as repo_used
