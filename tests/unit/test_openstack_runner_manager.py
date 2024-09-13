# Copyright 2024 Canonical Ltd.
# See LICENSE file for licensing details.

"""Module for unit-testing OpenStack runner manager."""

import secrets
from datetime import datetime, timedelta
from unittest.mock import MagicMock

import pytest

from github_runner_manager.openstack_cloud import openstack_runner_manager
from src.github_runner_manager.openstack_cloud.openstack_cloud import OpenStackCredentials
from tests.unit.factories import openstack_factory


@pytest.fixture(scope="function", name="mock_openstack_runner_manager")
def mock_openstack_runner_manager_fixture():
    """The mocked OpenStackRunnerManager instance."""
    return openstack_runner_manager.OpenStackRunnerManager(
        manager_name="mock-manager",
        prefix="mock-manager",
        credentials=OpenStackCredentials(
            auth_url="http://test-keystone-url.com",
            project_name="test-project-name",
            username="test-user-name",
            password=secrets.token_hex(16),
            region_name="test-region-name",
            project_domain_name="test-project-domain-name",
            user_domain_name="test-user-domain-name",
        ),
        server_config=openstack_runner_manager.OpenStackServerConfig(
            image="test-image", flavor="test-flavor", network="test-network"
        ),
        runner_config=openstack_runner_manager.GitHubRunnerConfig(
            github_path="test-org/test-repo", labels=["test-label1", "test-label2"]
        ),
        service_config=openstack_runner_manager.SupportServiceConfig(
            proxy_config=None,
            dockerhub_mirror=None,
            ssh_debug_connections=None,
            repo_policy_compliance=None,
        ),
    )


@pytest.mark.parametrize(
    "instance, expected_result",
    [
        pytest.param(
            openstack_runner_manager.OpenstackInstance(
                server=openstack_factory.ServerFactory(
                    status="DELETED",
                ),
                prefix="test",
            ),
            False,
            id="instance deleted",
        ),
        pytest.param(
            openstack_runner_manager.OpenstackInstance(
                server=openstack_factory.ServerFactory(
                    status="STOPPED",
                ),
                prefix="test",
            ),
            False,
            id="instance stopped",
        ),
        pytest.param(
            openstack_runner_manager.OpenstackInstance(
                server=openstack_factory.ServerFactory(
                    status="ERROR",
                ),
                prefix="test",
            ),
            False,
            id="instance in ERROR",
        ),
        pytest.param(
            openstack_runner_manager.OpenstackInstance(
                server=openstack_factory.ServerFactory(
                    status="UNKNOWN",
                ),
                prefix="test",
            ),
            False,
            id="instance in UNKNOWN",
        ),
        pytest.param(
            openstack_runner_manager.OpenstackInstance(
                server=openstack_factory.ServerFactory(
                    created_at=(datetime.now() - timedelta(hours=2)).strftime(
                        "%Y-%m-%dT%H:%M:%SZ"
                    ),
                    status="BUILD",
                ),
                prefix="test",
            ),
            False,
            id="stuck in BUILD status",
        ),
        pytest.param(
            openstack_runner_manager.OpenstackInstance(
                server=openstack_factory.ServerFactory(
                    created_at=datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
                    status="BUILD",
                ),
                prefix="test",
            ),
            True,
            id="just spawned",
        ),
        pytest.param(
            openstack_runner_manager.OpenstackInstance(
                server=openstack_factory.ServerFactory(
                    status="ACTIVE",
                ),
                prefix="test",
            ),
            True,
            id="active",
        ),
    ],
)
def test__runner_health_check(
    mock_openstack_runner_manager: openstack_runner_manager.OpenStackRunnerManager,
    instance: openstack_runner_manager.OpenstackInstance,
    expected_result: bool,
):
    """
    arrange: given OpenStack instance in different states.
    act: when _runner_health_check is called.
    assert: expected health check result is returned.
    """
    mock_openstack_runner_manager._health_check = MagicMock(return_value=True)
    assert mock_openstack_runner_manager._runner_health_check(instance=instance) == expected_result
