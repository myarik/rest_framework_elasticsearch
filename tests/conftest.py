# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os

import pytest

from elasticsearch_dsl import search as search_
from elasticsearch_dsl.connections import connections
from elasticsearch.helpers import bulk
from elasticsearch import Elasticsearch

from .test_data import create_test_index, DATA


def pytest_configure():
    import django
    from django.conf import settings

    settings.configure(
        SITE_ID=1,
        SECRET_KEY='not very secret in tests',
        ROOT_URLCONF='tests.urls',
        TEMPLATES=[
            {
                'BACKEND': 'django.template.backends.django.DjangoTemplates',
                'APP_DIRS': True,
                'OPTIONS': {
                    "debug": True,  # We want template errors to raise
                }
            },
        ],
        ALLOWED_HOSTS=['localhost', 'testserver']
    )

    django.setup()


@pytest.fixture(scope='session')
def es_client():
    connection = Elasticsearch([os.environ.get('TEST_ES_SERVER', {})])
    connections.add_connection('default', connection)
    return connection


@pytest.fixture(scope='session')
def es_data_client(es_client):
    # create mappings
    create_test_index(es_client)
    # load data
    bulk(es_client, DATA, raise_on_error=True, refresh=True)
    yield es_client
    es_client.indices.delete('test-*', ignore=404)


@pytest.fixture
def search(es_data_client, scope='function'):
    return search_.Search(index='test')
