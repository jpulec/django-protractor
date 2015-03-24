=====
Django Protractor
=====

Easily integrate your protractor tests in your django project.

Quick Start
-----------

1. Add "protractor" to your INSTALLED_APPS setting like this::

       INSTALLED_APPS = (
         ...
         'protractor',
       )

2. Run the following command to run your protractor tests:

   $ python manage.py protrator


Configuration
-------------

There are a variety of options available:

- `--protrator-conf` to specify a protractor config file. Default is `protractor.conf.js`
- `--runserver-command` to specify a different runserver command. Default is `runserver`
- `--specs` to specify which protractor specs to run.
- `--suite` to specify which protrator suite to run.
- `--addrport` to specify which ipaddr:port to run the server on. Default is `localhost:8081`
