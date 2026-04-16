
Part 6: Extras and Cleanup
==========================

Exercise 1: Abstract Repository
-------------------------------

Define an **Abstract Base Class** that encapsulates the Repository.
Make the actual implementations subclasses of that abstract class.

**Your domain objects (e.g. game.py may depend on the abstraction)!**

Exercise 2: Switch Repositories
-------------------------------

Add an environment variable ``REPO`` that controls which repository shall be used.

Implement a toplevel module ``repository`` that uses the environment variable to create exactly one repository object.

.. hint::

   Become aware what is the sequence of:

   - creating the repo object
   - reading environment vars with ``load_dotenv()``
   - running ``conftest.py``
   - running fixtures


Exercise 3: Separate integration test mark
------------------------------------------

Some of the tests may take longer to run. You might want to save them up for an integration test suite.

Mark them with:

.. code:: python3

   import pytest

   @pytest.mark.integration
   def test_...
       ...

Run tests with or without a selected mark:

.. code::

   uv run pytest -m 'integration'
   uv run pytest -m 'not integration'


Exercise 4: Idempotency
-----------------------

Consider your repository functions under the aspect of **idempotency**: calling the function twice should yield the same result.

- discuss why idempotency is important
- test for idempotency

Exercise 5: Data ingestion
--------------------------

Create a separate script for **data ingestion**: read the planets from the JSON file and write them to the repository.

Consider any of the following requirements. How would they affect the implementation?

- there are many entries (1B+)
- a complete reload of the data should be possible
- writing any entry might fail in a non-predictable way
- the data model will be subject to further change
- the data is stored in a redundant storage system with eventual consistency
- retroactive deletion should be possible (GDPR requirement)

Exercise 6: Incremental updates
-------------------------------

Ingest the data in two batches. 
Consider the following strategies. Pick one of them:

- check before writing whether an entry exists
- calculate a unique hash for each entry and use them to identify unique entries
- write checkpoints and metadata of already processed entries
- proceed in batches, repeat failed batches


Exercise 7: Read often
----------------------

Write a small load test that reads the same object 1000 times.

Exercise 8: Lint
----------------

Run your repository code through ``black``, ``ruff``, ``flake8`` or similar.

Exercise 9: Log
----------------

Add logging to your repository. Use the following code as a starting point

.. literalinclude:: logger.py
