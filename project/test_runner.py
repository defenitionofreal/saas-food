from django.test.runner import DiscoverRunner
from django.db import connections

import logging

logger = logging.getLogger(__name__)


class CustomTestRunner(DiscoverRunner):

    def __init__(self, *args, **kwargs):
        # Add any initialization code you need here
        print("INIT WWWW")
        logger.info('Initializing custom test runner')
        super().__init__(*args, **kwargs)

    def setup_databases(self, **kwargs):
        # # Install pg_trgm and btree_gin extension for all test databases
        # for alias in connections:
        #     with connections[alias].cursor() as cursor:
        #         cursor.execute('CREATE EXTENSION IF NOT EXISTS pg_trgm')
        #         cursor.execute('CREATE EXTENSION IF NOT EXISTS btree_gin')
        logger.info('Setting up test databases')
        print("----------Using custom test runner for PyTest!----------")
        return super().setup_databases(**kwargs)

    def teardown_databases(self, old_config, **kwargs):
        # for alias in connections:
        #     with connections[alias].cursor() as cursor:
        #         cursor.execute('DROP EXTENSION IF EXISTS pg_trgm')
        #         cursor.execute('DROP EXTENSION IF EXISTS btree_gin')
        logger.info('Tearing down test databases')
        return super().teardown_databases(old_config, **kwargs)
