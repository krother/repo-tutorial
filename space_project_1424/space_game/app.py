"""
Web frontend for the Pandas go to Space game.

The FastAPI app uses a middleware that translates JSON responses
into HTML pages - so you only need to deliver JSON.
"""
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from space_game.middleware import PreserveJSONResponse, json_to_html

from space_game.facade import GameData, start_game, execute_command

app = FastAPI(default_response_class=PreserveJSONResponse)

# register middleware that automatically uses JINJA templates
# so we only have to write REST functions
# *** Kudos to Tim Weber for finding out! ***
app.middleware("http")(json_to_html)


@app.get("/new_game", response_model=GameData)
def new_game() -> GameData:
    return start_game()


@app.get("/action/{game_id}/{command}", response_model=GameData)
def action(game_id: str, command: str) -> GameData:
    return execute_command(game_id=game_id, command=command)


# Also let FastAPI serve the HTMX "frontend" of our application.
app.mount("/", StaticFiles(directory="static", html=True), name="static")
