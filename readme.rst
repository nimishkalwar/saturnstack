=====
SaturnStack
=====

SaturnStack is a Django app for to buy subscriptions.


Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "polls" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'saturnstack',
    ]

2. Include the polls URLconf in your project urls.py like this::

    path('api/saturnstack/',include('saturnstack.urls')),

3. Run ``python manage.py migrate`` to create the saturnstack models.

4. Start the development server and visit http://127.0.0.1:8000/

5. Visit http://127.0.0.1:8000/api/saturnstack/ to run the api views.