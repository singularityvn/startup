Using ``async`` and ``await``
=============================
:date: 2010-12-03 10:20
:lang: en

*await handlers before request*

.. important:: 
    A note

.. contents:: Nội dung chính

.. epigraph::

    No matter where you go, there you are.
 
    -- Buckaroo Banzai


.. csv-table:: Frozen Delights!
    :header: "Treat", "Quantity", "Description"
    :widths: 15, 10, 30
 
    "Albatross12", 2.99, "On a stick!"
    "Crunchy Frog", 1.49, "If we took the bones out, it wouldn't be
    crunchy, now would it?"
    "Gannet Ripple", 1.99, "On a stick!"

Using routes
------------

Routes, error handlers, before request, after request, and teardown
functions can all be coroutine functions if Flask is installed with the
``async`` extra (``pip install flask[async]``). This allows views to be
defined with ``async def`` and use ``await``.

.. code-block:: python

    from os import path
    from bs4 import BeautifulSoup
    from pelican import signals, readers, contents
    import logging

    logger = logging.getLogger(__name__)


    def extract_toc(content):
        if isinstance(content, contents.Static):
            return

        soup = BeautifulSoup(content._content, 'html.parser')
        filename = content.source_path
        extension = path.splitext(filename)[1][1:]
        toc = None

        # default Markdown reader
        if not toc and readers.MarkdownReader.enabled and extension in readers.MarkdownReader.file_extensions:
            toc = soup.find('div', class_='toc')
            if toc:
                toc.extract()
                if len(toc.find_next('ul').find_all('li')) == 0:
                    toc = None

        # default reStructuredText reader
        if not toc and readers.RstReader.enabled and extension in readers.RstReader.file_extensions:
            toc = soup.find('div', class_='contents topic')
            if toc:
                toc.extract()
                tag = BeautifulSoup(str(toc), 'html.parser')
                tag.div['class'] = 'toc'
                tag.div['id'] = ''
                p = tag.find('p', class_='topic-title first')
                if p:
                    p.extract()
                toc = tag

        # Pandoc reader (markdown and other formats)
        if 'pandoc_reader' in content.settings['PLUGINS']:
            try:
                from pandoc_reader import PandocReader
            except ImportError:
                PandocReader = False
            if not toc and PandocReader and PandocReader.enabled and extension in PandocReader.file_extensions:
                toc = soup.find('nav', id='TOC')

        if toc:
            toc.extract()
            content._content = soup.decode()
            content.toc = toc.decode()
            if content.toc.startswith('<html>'):
                content.toc = content.toc[12:-14]


    def register():
        signals.content_object_init.connect(extract_toc)

Using Windows
+++++++++++++

.. warning:: 
    
    Using ``async`` on Windows on Python 3.8

    Python 3.8 has a bug related to asyncio on Windows. If you encounter
    something like ``ValueError: set_wakeup_fd only works in main thread``,
    please upgrade to Python 3.9.


Performance
-----------

Async functions require an event loop to run. Flask, as a WSGI
application, uses one worker to handle one request/response cycle.
When a request comes in to an async view, Flask will start an event loop
in a thread, run the view function there, then return the result.

.. figure:: https://martinfowler.com/articles/agileFluency/agile-fluency-model-v2-simple-2-1.png
    :alt: Hello
    :width: 800

    This is the caption of the figure (a simple paragraph).


Each request still ties up one worker, even for async views. The upside
is that you can run async code within a view, for example to make
multiple concurrent database queries, HTTP requests to an external API,
etc. However, the number of requests your application can handle at one
time will remain the same.

.. sidebar:: Optional Sidebar Title
   :subtitle: Optional Sidebar Subtitle

   Subsequent indented lines comprise
   the body of the sidebar, and are
   interpreted as body elements.

**Async is not inherently faster than sync code.** Async is beneficial
when performing concurrent IO-bound tasks, but will probably not improve
CPU-bound tasks. Traditional Flask views will still be appropriate for
most use cases, but Flask's async support enables writing and using
code that wasn't possible natively before.

Async functions will run in an event loop until they complete, at
which stage the event loop will stop. This means any additional
spawned tasks that haven't completed when the async function completes
will be cancelled. Therefore you cannot spawn background tasks, for
example via ``asyncio.create_task``.

If you wish to use background tasks it is best to use a task queue to
trigger background work, rather than spawn tasks in a view
function. With that in mind you can spawn asyncio tasks by serving
Flask with an ASGI server and utilising the asgiref WsgiToAsgi adapter
as described in. This works as the adapter creates an
event loop that runs continually.


When to use Quart instead
-------------------------

Flask's async support is less performant than async-first frameworks due
to the way it is implemented. If you have a mainly async codebase it
would make sense to consider `Quart`_. Quart is a reimplementation of
Flask based on the `ASGI`_ standard instead of WSGI. This allows it to
handle many concurrent requests, long running requests, and websockets
without requiring multiple worker processes or threads.

It has also already been possible to run Flask with Gevent or Eventlet
to get many of the benefits of async request handling. These libraries
patch low-level Python functions to accomplish this, whereas ``async``/
``await`` and ASGI use standard, modern Python capabilities. Deciding
whether you should use Flask, Quart, or something else is ultimately up
to understanding the specific needs of your project.

.. _Quart: https://gitlab.com/pgjones/quart
.. _ASGI: https://asgi.readthedocs.io/en/latest/


Extensions
----------

Flask extensions predating Flask's async support do not expect async views.
If they provide decorators to add functionality to views, those will probably
not work with async views because they will not await the function or be
awaitable. Other functions they provide will not be awaitable either and
will probably be blocking if called within an async view.

Extension authors can support async functions by utilising the
`flask.Flask.ensure_sync` method. For example, if the extension
provides a view function decorator add ``ensure_sync`` before calling
the decorated function,

.. code-block:: python

    def extension(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            ...  # Extension logic
            return current_app.ensure_sync(func)(*args, **kwargs)

        return wrapper

Check the changelog of the extension you want to use to see if they've
implemented async support, or make a feature request or PR to them.


Other event loops
-----------------

At the moment Flask only supports `asyncio`. It's possible to
override `flask.Flask.ensure_sync` to change how async functions
are wrapped to use a different library.