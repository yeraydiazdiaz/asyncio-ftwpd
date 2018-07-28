# AsyncIO for the Working Python Developer

Code for the examples on my article in medium [AsyncIO for the Working Python Developer](https://medium.com/@yeraydiazdiaz/asyncio-for-the-working-python-developer-5c468e6e2e8e).

The examples in the root directory will only work on Python 3.7, the [alternatives](https://github.com/yeraydiazdiaz/asyncio-ftwpd/blob/master/alternatives) directory includes versions of the examples for:

- Python 3.5 and above in the base `alternatives` directory.
- The `@asyncio.coroutines` subdirectory includes versions of the examples using the  [`asyncio.coroutine` decorator](https://docs.python.org/3.7/library/asyncio-task.html#asyncio.coroutine) and will work on Python 3.4 and above.
- Other subdirectories include versions using libraries like [Trio](https://trio.readthedocs.io) or [Tornado](https://tornadoweb.org).

## Usage:

- Clone this repo
- Create and activate a virtualenv
- `pip install -r requirements.txt`
- `python <NAME_OF_SAMPLE>.py`

Enjoy!
