
def test_get_game_empty():
    with pytest.raises(NoEntryFound):
        get_game("xyz123")


def test_get_location_empty():
    with pytest.raises(NoEntryFound):
        get_location("xyz123", "Magrathea")


def test_create_duplicate(example_location):
    create_location(example_location)
    with pytest.raises(DuplicateEntry):
        create_location(example_location)


def test_delete(example_location):
    create_location(example_location)
    delete_location("default", "Magrathea")
    with pytest.raises(NoEntryFound):
        get_location("default", "Magrathea")


def test_create_batch(location_batch):
    create_location_batch(location_batch)
    for loc in location_batch:
        assert get_location("default", loc.name)

