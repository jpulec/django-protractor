=====
Loggit
=====

Loggit is a django app to record that a certain event transpired. Perhaps a
customer made a purchase. Maybe an email was sent, or an order was shipped.
Whatever domain specific events exist, make a record of them. Loggit ships
with a couple of basic models and is easily extended.

Detailed info is in the 'docs' directory.

Quick Start
-----------

1. Add "loggit" to your INSTALLED_APPS setting like this::

       INSTALLED_APPS = (
         ...
         'loggit',
       )

   And define::
   
       LOGGIT_LOGENTRY_MODEL = '<app_label>.<ModelName>'
       LOGGIT_LOGEVENT_MODEL = '<app_label>.<ModelName>'
    
   i. Optionally install django-generic-m2m. Provided in django-loggit are two
    mixins that will add support for adding a generic M2M relationship to a
    log entry, where objects can be added with a particular label and then will
    be coalesced into the context that can be used by the event's render method.
    See https://github.com/coleifer/django-generic-m2m .

2. IMPORTANT: Loggit uses swappable models for its models. This is done so that
   either the LogEntry or the LogEvent model can be replaced with something that
   implements the same interface. However...For projects on Django 1.7+, this
   means that whichever models you use when you do Loggit's first migrations,
   must be the models you use for the lifetime of that project (i.e. migrations).
   Read about how migrations handle django.contrib.auth and its swappable
   model for more information.

3. Run `python manage.py migrate` to create the taggit models. Before runnning,
   make sure LOGGIT_LOGENTRY_MODEL and LOGGIT_LOGEVENT_MODEL are set to the
   models you would like them to be for the lifetime of the project.

4. Start creating events based on your domain, and implement how you want them
   to be rendered.
