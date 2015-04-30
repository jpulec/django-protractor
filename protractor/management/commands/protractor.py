# -*- coding: utf-8 -*-

import os
import sys
from multiprocessing import Process
from optparse import make_option
import subprocess


from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.db import connection
from django.test.runner import setup_databases


class Command(BaseCommand):
    args = '[--protractor-conf] [--runserver-command] [--specs] [--suite] [--addrport]'
    help = 'Run protractor tests with a test database'

    option_list = BaseCommand.option_list + (
        make_option('--protractor-conf',
            action='store',
            dest='protractor_conf',
            default='protractor.conf.js',
            help='Specify a destination for your protractor configuration'
        ),
        make_option('--runserver-command',
            action='store',
            dest='run_server_command',
            default='runserver',
            help='Specify which command you want to run a server'
        ),
        make_option('--specs',
            action='store',
            dest='specs',
            help='Specify which specs to run'
        ),
        make_option('--suite',
            action='store',
            dest='suite',
            help='Specify which suite to run'
        ),
        make_option('--fixture',
            action='append',
            dest='fixtures',
            help='Specify fixture to load initial data to the database'
        ),
        make_option('--addrport', action='store', dest='addrport',
            type='string', default='8081',
            help='port number or ipaddr:port to run the server on'),
    )

    def handle(self, *args, **options):
        options['verbosity'] = int(options.get('verbosity'))

        if not os.path.exists(options['protractor_conf']):
            raise IOError("Could not find '{}'"
                .format(options['protractor_conf']))

        self.run_webdriver()

        old_config = self.setup_databases(options)

        fixtures = options['fixtures']
        if fixtures:
            for fixture in fixtures:
                call_command('loaddata', fixture,
                             **{'verbosity': options['verbosity']})

        test_server_process = Process(target=self.runserver, args=(options,))
        test_server_process.daemon = True
        test_server_process.start()

        protractor_command = 'protractor {}'.format(options['protractor_conf'])
        if options['specs']:
            protractor_command += '--specs {}'.format(options['specs'])
        if options['suite']:
            protractor_command += '--suite {}'.format(options['suite'])

        return_code = subprocess.call(protractor_command.split())
        self.teardown_databases(old_config, options)
        if return_code:
            self.stdout.write('Failed')
            sys.exit(1)
        else:
            self.stdout.write('Success')

    def setup_databases(self, options):
        return setup_databases(options['verbosity'], False)

    def teardown_databases(self, old_config, options):
        """
        Destroys all the non-mirror databases.
        """
        old_names, mirrors = old_config
        for connection, old_name, destroy in old_names:
            if destroy:
                connection.creation.destroy_test_db(old_name, options['verbosity'])

    def runserver(self, options):
        use_threading = connection.features.test_db_allows_multiple_connections
        self.stdout.write('Starting server...')
        call_command(
            options['run_server_command'],
            addrport=options.get('addrport'),
            shutdown_message='',
            use_reloader=False,
            use_ipv6=False,
            verbosity=0,
            use_threading=use_threading,
            stdout=open(os.devnull, 'wb')
        )

    def run_webdriver(self):
        self.stdout.write('Starting webdriver...')
        with open(os.devnull, 'wb') as f:
            subprocess.call(['webdriver-manager', 'update'], stdout=f, stderr=f)
            subprocess.Popen(['webdriver-manager', 'start'], stdout=f, stderr=f)
