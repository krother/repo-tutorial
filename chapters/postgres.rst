
Part 5: PostgreSQL
==================

.. figure:: elephant.png

**In the last round, we will try a SQL database within Docker: PostgreSQL.**

Exercise 1: Start a postgres container
--------------------------------------

Add a new section to your ``docker-compose.yml``:

.. code::

   postgres:
     image: postgres:latest
     restart: "no"
     environment:
       POSTGRES_PASSWORD: '${POSTGRES_PASSWORD}'
     ports:
       - '5432:5432'

Define the ``POSTGRES_PASSWORD`` variable in your ``.env`` file.
Then start the container with:

.. code::

  docker compose up postgres


Exercise 2: Define tables
-------------------------

Create a new repository module (our fourth).
We will use the declarative model in ``SQLAlchemy`` to define tables:

.. code:: python3

   from sqlalchemy import (
       create_engine,
       Table,
       MetaData,
       Column,
       String,
       Boolean,
       select,
       text,
    )
   
   metadata = MetaData()
   
   games = Table(
       "games",
       metadata,
       Column("id", String(10), primary_key=True),
       Column("location", String(100)),
       Column("cargo", String(50)),
       Column("crew", String(100)),
   )

Add the model for locations as well.

Exercise 3: Create the database
-------------------------------

For simplicity, we will create the database within the repository.
This is helper code that will be at least useful for integration testing, even if you do not need it in production.

.. code:: python3

   from sqlalchemy.exc import IntegrityError, ProgrammingError

   try:
       pg = create_engine(
           f"postgresql+psycopg2://{connection}/postgres",
           isolation_level="AUTOCOMMIT"
       )
       with pg.connect() as conn:
           conn.execute(text(f"CREATE DATABASE {dbname}"))
   except ProgrammingError:
       pass
   
   engine = create_engine(
       f"postgresql+psycopg2://{connection}/{dbname}",
       echo=False
   )
   metadata.create_all(engine)


Exercise 4: Read and write
--------------------------

To write, you might use the serializers again:

.. code:: python3

   GAMES_KEYS = ["id", "location", "cargo", "crew"]
   with engine.begin() as con:
        con.execute(
          games.insert().values(
            **dict(zip(GAMES_KEYS, serialize_game(game)))
          ))

Reading is not much different:

.. code:: python3

   with engine.connect() as con:
       result = con.execute(select(games).where(games.c.id == game_id)).fetchall()
       if result:
           return deserialize_game(result[0])


Implement the rest of the repository and check if tests pass.


Exercise 5: Inspect the database
--------------------------------

With docker, you can log into the database:

.. code::

   docker compose exec -it -u postgres postgres psql


Exercise 6: A nasty bug
-----------------------

The following function contains a bug. What is wrong with the code?
How can you prevent similar issues impacting production data?

.. code:: python3

   def delete_location(game_id: str, name: str) -> None:
       """Removes a single location"""
       with engine.begin() as con:
           con.execute(
               locations.delete().where(locations.c.game_id == game_id)
           )


Reflection questions
--------------------

- should you include a foreign key from ``location`` to ``game``?
- what is the n+1 problem?
