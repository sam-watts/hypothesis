# coding=utf-8
#
# This file is part of Hypothesis, which may be found at
# https://github.com/HypothesisWorks/hypothesis-python
#
# Most of this work is copyright (C) 2013-2018 David R. MacIver
# (david@drmaciver.com), but it contains contributions by others. See
# CONTRIBUTING.rst for a full list of people who may hold copyright, and
# consult the git log if you need to determine who owns an individual
# contribution.
#
# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file, You can
# obtain one at http://mozilla.org/MPL/2.0/.
#
# END HEADER

from __future__ import division, print_function, absolute_import

import re

from hypothesis.extra.pytestplugin import LOAD_PROFILE_OPTION

pytest_plugins = str('pytester')

CONFTEST = """
from hypothesis._settings import settings
settings.register_profile("test", settings(max_examples=1))
"""

TESTSUITE = """
from hypothesis import given
from hypothesis.strategies import integers
from hypothesis._settings import settings

def test_this_one_is_ok():
    assert settings().max_examples == 1
"""


def test_runs_reporting_hook(testdir):
    script = testdir.makepyfile(TESTSUITE)
    testdir.makeconftest(CONFTEST)
    result = testdir.runpytest(script, LOAD_PROFILE_OPTION, 'test')
    out = '\n'.join(result.stdout.lines)
    assert '1 passed' in out


def test_pytest_report_header_reports_version(testdir):
    script = testdir.makepyfile(TESTSUITE)
    testdir.makeconftest(CONFTEST)
    result = testdir.runpytest(script, LOAD_PROFILE_OPTION, 'test')
    out = '\n'.join(result.stdout.lines)
    assert re.search(r'hypothesis \d+\.\d+\.\d+', out)


def test_pytest_report_header_reports_settings(testdir):
    script = testdir.makepyfile(TESTSUITE)
    testdir.makeconftest(CONFTEST)
    result = testdir.runpytest(script, LOAD_PROFILE_OPTION, 'test')
    out = '\n'.join(result.stdout.lines)
    assert 'max_examples=1' in out
