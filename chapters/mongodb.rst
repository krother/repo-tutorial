Part 4: MongoDB
===============

In this chapter we will swap the repository again, this time to **MongoDB**.

Exercise 1: Docker
------------------

To run a MongoDB instance, I recommend **Docker**, because it guarantees a hassle-free installation (especially if you also want to run PostgreSQL in the next chapter).

Create a file `docker-compose.yml` in the project directory containing:

.. code::

   services:
   
     mongodb:
       image: mongo:latest
       restart: "no"
       ports:
         - '27017:27017'

Now you should be able to start the MongoDB container with:

.. code::

   docker compose up mongodb

Exercise 2: Rewrite the repository
----------------------------------

Copy ``repository.py`` once again and get rid of DuckDB-specific code.
Instead, connect using the ``pymongo`` library:

.. code:: python3

   from pymongo import MongoClient
         
   conn = MongoClient()
   db = conn.get_database(os.getenv("MONGODB_DATABASE"))

Configure the ``MONGODB_DATABASE`` variable in the ``.env`` file.


Exercise 3: Implement functions
-------------------------------

Fortunately, ``pydantic`` objects and JSON objects in MongoDB translate into each other well. Here is some code to persist repository functions with MongoDB.

**Unfortunately, the code is buggy. Fix the bugs.**

.. literalinclude:: repository_mongodb.py


Make the tests pass.


Exercise 4: Inspect the database
--------------------------------

After running the tests or playing the game, there should be some data in the database.
Let's take a moment to inspect the database directly.
Log into the database through docker:

.. code::

   docker compose exec -it mongodb mongosh

Try out the following commands one by one:

  show databases

  use test_db

  show collections

  db.games.findOne()

  db.games.countDocuments()

  db.games.deleteMany({})


Exercise 5: Separate test and production databases
--------------------------------------------------

One problem is that at the moment, the tests. will run on the same database as the game itself. Why might that be a problem?

To use a separate test database, you need to override the environment setting in ``conftest.py``.

.. code:: python3

   os.environ["MONGODB_DATABASE"] = "test_db"

.. hint::

   Consider the order of execution. Does it matter where the environment is modified?
   Compare the function ``config.load_dotenv()`` .


Reflection questions
--------------------

- MongoDB generates an extra id field when writing to a collection? Why does ``pydantic`` not complain about it?
- Should we include that extra id in the domain model?
- What effect does a typo in a collection name have?
- Can the impact of typos be mitigated?
- What is a **shard key**. Do we have any good shard keys in our domain data?
