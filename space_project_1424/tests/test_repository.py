
from pydantic_core.core_schema import tuple_positional_schema
import pytest

from space_game.config import DATA_PATH

from space_game.location import Location, ActionTrigger
from space_game.repository import (
    create_game,
    create_location,
    get_game,
    get_location,
)

TEST_JSON = DATA_PATH / "magrathea.json"

@pytest.fixture
def example_location():
    return Location(
        name="Magrathea",
        description="once home of world builders, now a sad ruin",
        image="magrathea.png",
        type="planet",
        connected_names=["earth"],
        active=False,
        trigger=ActionTrigger(),
    )

@pytest.fixture
def location_batch():
    result = []
    for num in range(1, 11):
        result.append(
            Location(
                name=f"planet {num}",
                description=f"this is planet #{num}",
                image=f"{num}.png",
                type="planet",
                connected_names=["earth"],
                active=False,
                trigger=ActionTrigger(),
            )
        )
    return result


def test_create_and_get_location(example_location):
    create_location("xyz123", example_location)
    loc = get_location("xyz123", "Magrathea")
    assert loc.name == "Magrathea"


def test_create_game():
    game = create_game(TEST_JSON, "Magrathea")
    assert game.game_id is not None
    assert game.location.name == "Magrathea"
    assert game.crew == ["panda"]


def test_create_and_get():
    game = create_game(TEST_JSON, "Magrathea")
    game = get_game(game.game_id)
    assert game.location.name == "Magrathea"


def test_create_multiple(location_batch):
    for loc in location_batch:
        create_location("xyz", loc)
    for loc in location_batch:
        assert get_location("xyz", loc.name)


def test_get_location_for_game(example_location):
    create_location("xyz", example_location)
    game = create_game(TEST_JSON, start_location="Magrathea")
    loc = get_location(game.game_id, "Magrathea")
    assert loc.name == "Magrathea"
