Part 2: DuckDB
==============

In this chapter we will swap the dictionary implementation of the repository for a real database: **DuckDB**.


Exercise 1: Identifiers
-----------------------

Consider the following identifiers for games. Which would you prefer and why?

.. code::

   john.doe@email
   1
   user_001
   a
   a4bf2m8
   Il1O0o
   550e8400-e29b-41d4-a716-446655440000
   ABC123!@#
   あいう123
   temp_id_will_change
   2024-01-15-record-42


Exercise 2: Move the dict repo out of the way
---------------------------------------------

Copy the file ``repository.py`` to ``repository_dict.py``. We will use DuckDB in ``repository.py``.

Clear the bodies of the repository functions. Also remove the dictionaries ``GAMES`` and ``LOCATIONS``.

Exercise 3: Create duckdb tables
--------------------------------

Creating tables with duckdb is easy as quack: 

.. code:: python3

    import duckdb

    con = duckdb.connect()
    con.sql("""
    CREATE TABLE games (
        id VARCHAR(10) PRIMARY KEY,
        location VARCHAR(100),
        cargo VARCHAR(50),
        crew VARCHAR(100),
        )     
    """)

Add a table ``location`` as well. Include a ``game_id`` column.
Since the ``ActionTrigger`` class has a 1:1 relationship, you can stuff its fields into the same table.


Exercise 4: Write rows to duckdb
--------------------------------

DuckDB knows how an SQL insert works. Here is an example for the ``games`` table. It uses placeholders for the parameters to prevent SQL injection:

.. code:: python3

    con.sql("INSERT INTO games VALUES (?,?,?,?)",
            params=values)

``values`` would be a list-like type of length 4. To get the values, you will need to write a **serializer function**:

.. code:: python3

    def serialize_game(game: SpaceGame) -> list[str]:
        ...

Implement the serializer.

.. note::

   Where should you put the serializer code?


Exercise 5: Read rows from duckdb
---------------------------------

To read a row, you would use a cursor and a placeholder as well:

.. code:: python3

    cursor = con.sql("SELECT * FROM games WHERE id = ?",
                      params=(game_id,))
    result = cursor.fetchall()

Now, ``result`` is of type ``Sequence[Sequence[Any]]``. To get a game object, you need to **deserialize** it.
Implement a deserializer function and place it where you left the serializer:

.. code:: python3

    def deserialize_game(values: Sequence[Any]) -> SpaceGame:
        ...

Exercise 6: Implement
---------------------

Use the above duckdb code and serializers to implement the repository functions.

.. note::

   Do not forget to read all locations at start in ``create_game()``

Exercise 7: What about the tests?
---------------------------------

Run all tests. You should observe that a considerable amount of them **fail**.

**Figure out why.**

.. hint::
    
    At this moment you might come to the realization that implementing a repository is not a trivial thing. Even if the atomic operations like reading and writing data are quite straightforward, we encounter complexity. The point of the exercise is that we have moved the complexity away from our game logic. So whatever solution we will find, we have a place for the messy parts.
