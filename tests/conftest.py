# Copyright 2024 Canonical Ltd.
# See LICENSE file for licensing details.

"""Fixtures for charm tests."""


def pytest_addoption(parser):
    """Parse additional pytest options.

    Args:
        parser: Pytest parser.
    """
    parser.addoption(
        "--path",
        action="store",
        help="The GitHub path to register the runners on, i.e. <org> or <org>/<repo>",
    )
    parser.addoption("--token", action="store", help="The GitHub token to register the runners.")
