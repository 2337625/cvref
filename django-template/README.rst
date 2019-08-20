Installation
============

Download repository and run commands::

    python install.py
    pip install -r requirements/dev.txt
    python md.py syncdb
    python md.py collectstatic
    python md.py runserver

Now that the server’s running, visit `http://localhost:8000 <http://localhost:8000/>`_ with your Web browser.
