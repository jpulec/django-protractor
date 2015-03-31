=====
Django Protractor
=====

Easily integrate your protractor tests in your django project, and get a fresh test database with every run.

Dependencies
------------
You must have npm and protractor installed. `See Protractor Documentation for more details`_

Quick Start
-----------

1. Add "protractor" to your INSTALLED_APPS setting like this::

       INSTALLED_APPS = (
         ...
         'protractor',
       )

2. Run the following command to run your protractor tests::

       python manage.py protrator


Configuration
-------------

There are a variety of options available:

- :code:`--protrator-conf` to specify a protractor config file. Default is :code:`protractor.conf.js`
- :code:`--runserver-command` to specify a different runserver command. Default is :code:`runserver`
- :code:`--specs` to specify which protractor specs to run.
- :code:`--suite` to specify which protrator suite to run.
- :code:`--addrport` to specify which ipaddr:port to run the server on. Default is :code:`localhost:8081`

.. _See Protractor Documentation for more details: https://angular.github.io/protractor/#/
