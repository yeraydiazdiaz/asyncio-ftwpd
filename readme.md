# AsyncIO for the Working Python Developer

Code for the examples on my article in medium [AsyncIO for the Working Python Developer](https://medium.com/@yeraydiazdiaz/asyncio-for-the-working-python-developer-5c468e6e2e8e).

The examples in the root directory will only work on Python 3.7, the [alternatives](https://github.com/yeraydiazdiaz/asyncio-ftwpd/blob/master/alternatives) directory includes versions of the examples for lower versions:

- Files suffixed with `async-await` use the async/await syntax and will work on Python 3.5 and above
- Files suffixed with `coroutine-decorator` use the [`asyncio.coroutine` decorator](https://docs.python.org/3.7/library/asyncio-task.html#asyncio.coroutine) and will work on Python 3.4 and above
- The first few examples follow the excellent [Gevent for the Working Python Developer](http://sdiehl.github.io/gevent-tutorial/) tutorial that I broadly followed to introduce [asyncio](https://docs.python.org/3/library/asyncio.html), I've included the code using gevent for these examples.
- You will also find versions of some examples using [Tornado](https://tornadoweb.org), as it was the initial idea was to use it for the article and it's an amazing alternative.

## Usage:

- Clone this repo
- Create and activate a virtualenv
- `pip install -r requirements.txt`
- `python <NAME_OF_SAMPLE>.py`

Enjoy!
