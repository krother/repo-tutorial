
Part 1: Repository
==================

Why do we need a Repository?
----------------------------

Adding a persistence layer
++++++++++++++++++++++++++

At the moment, only one game is active at a time.
If you want to manage multiple games being served in parallel, you will need to think about storing the game data.
This is why we need a **persistence layer** where the storing is managed.

Domain Objects
++++++++++++++

At the same time, we want to have a stable **domain model**. At the moment, the modules ``game.py`` and ``location.py`` contain the complete game mechanics. Ideally, the domain model is independent of everything else - it should not depend on any low-level mechanics (e.g. persistence).

.. note::
    
    This produces a dilemma: how are we supposed to manage persistence, if the core game does not know about it?

The solution: a Repository
++++++++++++++++++++++++++

We want to have a repository module that handles persistence. The repository should know about the domain model, not the other way around.
This is an example of the **Dependency Inversion Principle** (although I do not find the term very clear):
We put the domain model in the center to keep it clean. We group all other code that handles the messy real-world details around it (such as API endpoints, file paths and SQL queries).
Thus, the Repository Pattern is an example of good program design.

TODO:
DEPENDENCY GRAPH
DTO vs ENTITY

.. note::

   You may have heard the term **hexagonal architecture**. It means more or less the same thing, but we will not analyze the word in detail.


Exercise 1: Refactor galaxy
---------------------------

Take a look at ``location.py``. The ``Location`` class (planets and places on planets) contains a complete graph with all planets.
Let's assume that **the galaxy is potentially huge**. The complete graph should not be kept in memory.
Before you can add a Repository, we need to remove the graph.

Modify the code in ``location.py``:

- remove the ``Location.galaxy`` attribute
- remove ``Location.connected_locs`` and all uses of it
- remove ``Location.add_connection()`` completely
- strip the ``create_galaxy()`` function of the part that builds the connection graph. All you need is:

.. code:: python3

    j = json.load(open(filename, encoding="utf-8"))
    return [Location(**loc) for loc in j]

At this moment the tests should stop working. Stay tuned!

Exercise 2: Create repository
-----------------------------

Let's prepare for adding the repository. For a start, we use a Python dictionary for persistence:

- create a new file ``repository.py``
- move the ``create_galaxy()`` function to the new module
- create two empty dictionaries: ``GAMES`` and ``LOCATIONS``
- add an attribute ``game_id:str`` to ``game.SpaceGame``

Exercise 3: Repository functions
--------------------------------

Create the following interface in ``repository.py``. Leave the function bodies empty for now:

.. code:: python3

    def create_game(galaxy_file: str, start_location: str) -> SpaceGame:

    def get_game(game_id) -> SpaceGame:

    def create_location(game_id: str, location: Location) -> Location:

    def get_location(game_id: str, name: str) -> Location:

Exercise 4: Test-Driven-Development
-----------------------------------

Copy tests in :download:``test_repository.py`` to the ``tests/`` folder.
Let's run the tests:

.. code::

   uv run pytest tests/test_repository.py

Of course, they all fail – we haven't implemented anything yet.

Implement the repository methods using the dictionaries ``GAMES`` and ``LOCATIONS``.
Use ``"abc"`` as a game id for now. Make the tests pass one by one.

Notes:
++++++

- ``create_game`` needs to call ``get_location()``
- store the game_id along with a location in ``LOCATIONS``
- call ``create_galaxy()`` in ``create_game()`` and create all locations 

Continue implementing until ``test_repository.py`` passes.

Exercise 5: Connect things
--------------------------

The other tests still fail. We need to connect a few things.

- edit ``facade.start_game()`` to use ``repository.create_game()``
- ``facade.execute_command()`` should use ``repository.get_game()``
- ``game.get_commands()`` needs to use ``repository.get_location()``

.. warning::
    
   **Wait, there is a circular import!**

   We do not want to import the repository anyway.
   Lets use a **callback function** instead!

   Add an attribute ``get_location: Callable[[str, str], Location]`` to ``game.SpaceGame``.
   This design pattern is called *ports + adapters* in the DDD lingo.

Passing the ``get_location`` attribute should help you to make all tests pass.

Exercise 6: More tests
----------------------

Consider writing a few more tests to reinforce the structure:

- read the same object twice
- write the same object twice. What should happen?
- write with an error (create a game with a starting planet that does not exist)


Reflection Questions
--------------------

- should there be a ``location.id`` attribute?
- should there be a ``location.game_id`` attribute?
- should the data ingestion really be part of ``create_game()``?
