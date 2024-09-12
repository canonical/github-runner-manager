# Copyright 2024 Canonical Ltd.
# See LICENSE file for licensing details.

"""Module for testing integration with GitHub."""

import pathlib
import secrets

import pytest

from github_runner_manager import github_client
from tests.integration.helpers import github as github_helper


@pytest.fixture(scope="module", name="github_client")
def github_client_fixture(pytestconfig: pytest.Config):
    """The GitHub client fixture."""
    token = pytestconfig.getoption("--token")
    assert token, "--token is required to test Github client."
    return github_client.GithubClient(token=token)


@pytest.fixture(scope="module", name="path")
def path_fixture(pytestconfig: pytest.Config):
    """The GitHub path fixture."""
    path = pytestconfig.getoption("--path")
    assert path, "--path is required to test GitHub client."


def test_github_client(
    github_client: github_client.GithubClient,
    path: github_client.GitHubPath,
    tmp_path: pathlib.Path,
):
    """
    arrange: Given GitHub client.
    act: \
        1. when get_runner_registration_token is run.
        2. when get_runner_github_info is run.
        3. when delete_runner is run.
    assert: \
        1. a runner can be registered with the token.
        2. self hosted runners are returned.
        3. runner is deleted from registered runners.
    """
    # 1. a runner can be registered with the token.
    test_path = tmp_path / "test_github_client"
    test_path.mkdir(parents=True, exist_ok=True)
    token = github_client.get_runner_registration_token(path=path)
    test_id = secrets.token_hex(4)
    test_runner_name = f"test-{test_id}"
    github_helper.register_runner(
        path=path,
        workdir=test_path,
        test_id=test_id,
        registration_token=token,
        runner_name=test_runner_name,
    )

    # 2. when get_runner_github_info is run, self hosted runners are returned.
    runners = github_client.get_runner_github_info(path=path)
    assert runners, "No registered runners found."
    target_runner = [test_runner_name == runner.name for runner in runners]
    assert target_runner, "Test runner not registered."
    registered_runner = target_runner[0]

    # 3. runner is unregistered successfully
    assert github_client.get_runner_remove_token(path=path), "Unable to retrieve remove token"
    github_client.delete_runner(path=path, runner_id=registered_runner.id)
