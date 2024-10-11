#  Copyright 2024 Canonical Ltd.
#  See LICENSE file for licensing details.
from datetime import datetime, timedelta
from unittest.mock import MagicMock

import pytest

from github_runner_manager.openstack_cloud import health_checks, openstack_cloud
from github_runner_manager.openstack_cloud.openstack_cloud import OpenstackCloud
from tests.unit.factories import openstack_factory


@pytest.mark.parametrize(
    "instance, expected_result",
    [
        pytest.param(
            openstack_cloud.OpenstackInstance(
                server=openstack_factory.ServerFactory(
                    status="DELETED",
                ),
                prefix="test",
            ),
            False,
            id="instance deleted",
        ),
        pytest.param(
            openstack_cloud.OpenstackInstance(
                server=openstack_factory.ServerFactory(
                    status="STOPPED",
                ),
                prefix="test",
            ),
            False,
            id="instance stopped",
        ),
        pytest.param(
            openstack_cloud.OpenstackInstance(
                server=openstack_factory.ServerFactory(
                    status="ERROR",
                ),
                prefix="test",
            ),
            False,
            id="instance in ERROR",
        ),
        pytest.param(
            openstack_cloud.OpenstackInstance(
                server=openstack_factory.ServerFactory(
                    status="UNKNOWN",
                ),
                prefix="test",
            ),
            False,
            id="instance in UNKNOWN",
        ),
        pytest.param(
            openstack_cloud.OpenstackInstance(
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
            openstack_cloud.OpenstackInstance(
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
            openstack_cloud.OpenstackInstance(
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
def test_check_active_runner(
    instance: openstack_cloud.OpenstackInstance,
    expected_result: bool,
    monkeypatch: pytest.MonkeyPatch,
):
    """
    arrange: given OpenStack instance in different states.
    act: when check_runner is called.
    assert: expected health check result is returned.
    """
    monkeypatch.setattr(health_checks, "check_active_runner", MagicMock(return_value=True))
    assert (
        health_checks.check_runner(
            openstack_cloud=MagicMock(spec=OpenstackCloud), instance=instance
        )
        == expected_result
    )
