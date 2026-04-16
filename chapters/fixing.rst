
Part 3: Fixing a broken Repository
==================================

In this chapter, we will deal with the leftover problem from the last one.

Exercise 1: Delete data between tests
-------------------------------------

Every test needs to start with an empty databse.
Otherwise we will end up in the hell of side effects between tests.

A good place is to define a pytest fixture that is automatically called before each test.
Create a ``tests/conftest.py`` file and add a function to clear the database:

.. code:: python3

    from space_game.repository import con

    @pytest.fixture(autouse=True)
    def clear_database():
        con.sql("DELETE FROM games")

If implemented correctly, the tests in ``test_repository.py`` should now pass.

.. note::

   Shouldn't you place the function for clearing the database in ``repository.py``?


Exercise 2: Debugging
---------------------

The tests for the entire game might still fail.

Play the game (or check the output of a test playing the entire games) and see what is going on. 


Exercise 3: Update function
---------------------------

After every action in the game, we need to make sure that the current state of the game is persisted. 
In ``facade.py`` immediately after the line:

.. code:: python3

    cmd.callback()

update both game and location:

.. code:: python3

    update_game(game)
    update_location(game_id, game.location)

Run the tests in :download:`test_update.py` .

Implement the according methods in the repo.
Now most of the tests should run.

.. hint::
    
    In the dict we did not need to update anything, because the dictionaries were keeping the same reference to objects all the time.


Exercise 4: Add a persistence file
----------------------------------

Duckdb can store its data in a file, e.g.:

.. code:: python3

    con = duckdb.connect("my_ducks.db")

Add the filename to the `.env` file and retrieve it as an environment variable via `os.getenv(...)`.


Exercise 5: Add a primary key
-----------------------------

Make sure every combination of game and location exists only once.
Add a primary key to the ``location`` table - at the end of the respective ``CREATE TABLE`` instruction add:

.. code::

    PRIMARY KEY (game_id, name)


Exercise 6: Profile and caching
-------------------------------

At this point, running the tests may feel considerably slower than before.
Run a profiler to identify bottlenecks:

.. code::

    python -m cProfile -s cumtime -m pytest

Where could you use caching to speed up the tests?
