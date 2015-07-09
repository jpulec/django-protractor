=====
Django Protractor
=====

Easily integrate your protractor tests in your django project, and get a fresh test database with every run.
Additionally, there is an included test case mixin to allow any custom setup code to run.

Dependencies
------------
You must have npm and protractor installed. `See Protractor Documentation for more details`_

Quick Start Testing
-------------------

1. Add "protractor" to your INSTALLED_APPS setting like this::

       INSTALLED_APPS = (
         ...
         'protractor',
       )

2. Run the following command to run your protractor tests::

       python manage.py protractor

More Advanced Test Case Customization
-------------------------------------
If you're like me, you'll find that one-time fixture loading for all of your protractor tests just isn't enough.
I use the wonderful `factory_boy`_ for my test setup and wanted to find a way to incorporate it with my protractor acceptance tests.
What spawned is an incredibly hack-y mixin that allows me to do just that.

Create a Subclass of `StaticLiveServerTestCase`_ incorporating the :code:`ProtractorTestCaseMixin` like so, setting the class attribute
:code:`specs` to a list of protractor specs. This list will be piped to the :code:`--specs` arg that protractor recieves. Then do any necessary
setup by overriding the :code:`setUp()` method.

.. code:: python

  from django.contrib.staticfiles.testing import StaticLiveServerTestCase
  from protractor.test import ProtractorTestCaseMixin


  class MyAcceptanceTestCase(ProtractorTestCaseMixin, StaticLiveServerTestCase):
      specs = ['tests/acceptance/test-spec.js',]

      def setUp(self):
          """Do factory setup stuff."""
          super(MyAcceptanceTestCase, self).setUp()

          FooFactory()
          BarFactory()

      def get_protractor_params(self):
          ...

      def test_run(self):
          ...


There are two other hooks that exist as well that can be overridden:

:code:`get_protractor_params()` should return a dict that will be piped to protractor with the :code:`--params` argument.
By default this passes in the value of :code:`self.live_server_url`.

:code:`test_run()` is the actual method that gets discovered by test runners, and calls out to protractor using subprocess.
You may need to override this if you want to do any python assertions about database state after your protractor tests
have run.


Configuration
-------------

There are a variety of options available:

- :code:`--protractor-conf` to specify a protractor config file. Default is :code:`protractor.conf.js`
- :code:`--runserver-command` to specify a different runserver command. Default is :code:`runserver`
- :code:`--specs` to specify which protractor specs to run.
- :code:`--suite` to specify which protractor suite to run.
- :code:`--addrport` to specify which ipaddr:port to run the server on. Default is :code:`localhost:8081`
- :code:`--fixture` to specify which a fixture to load. This can be used multiple times and will load all specified fixtures.

.. _See Protractor Documentation for more details: https://angular.github.io/protractor/#/
.. _factory_boy: https://github.com/rbarrois/factory_boy
.. _StaticLiveServerTestCase: https://docs.djangoproject.com/en/1.8/ref/contrib/staticfiles/#django.contrib.staticfiles.testing.StaticLiveServerTestCase
