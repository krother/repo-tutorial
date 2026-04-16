
from space_game.repository import get_game, get_location, create_game, update_game, update_location
from test_repository import example_location, location_batch, TEST_JSON


def test_update_game():
    game = create_game(TEST_JSON, start_location="Magrathea")
    game.crew.append("pingu")
    update_game(game)
    game = get_game(game.game_id)
    assert "pingu" in game.crew

def test_update_location():
    game = create_game(TEST_JSON, start_location="Magrathea")
    loc = get_location(game.game_id, "Magrathea")
    loc.active = False
    loc.connected_names.append("Filtwodl")
    update_location(game.game_id, loc)
    loc = get_location(game.game_id, "Magrathea")
    assert loc.active is False
    assert "Filtwodl" in loc.connected_names
