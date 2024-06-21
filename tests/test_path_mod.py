#!/usr/bin/env python3

import re

import pytest

import path_mod as pm


@pytest.mark.unit
def test_run_filter():
    path_before = '/aaa:/bbb:/ccc:/aaa'
    path_items_expected = ['/aaa', '/ccc', '/aaa']

    setup = {
        'path': path_before,
        'sub_parser_name': 'filter',
        'regex': re.compile(r'/b+'),
        'lazy': False,
    }

    path_new = pm.run_filter(setup)

    assert path_new == path_items_expected


@pytest.mark.unit
def test_run_lazy_filter():
    path_before = '/aaa:/bbb:/ccc:/aaa'
    path_items_expected = ['/aaa', '/ccc', '/aaa']

    setup = {
        'path': path_before,
        'sub_parser_name': 'filter',
        'regex': re.compile(r'b'),
        'lazy': True,
    }

    path_new = pm.run_filter(setup)

    assert path_new == path_items_expected
