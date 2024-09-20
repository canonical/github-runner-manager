#  Copyright 2024 Canonical Ltd.
#  See LICENSE file for licensing details.

"""Module containing reactive scheduling related types."""

from pydantic import BaseModel, MongoDsn

from github_runner_manager.manager.runner_manager import RunnerManagerConfig
from github_runner_manager.openstack_cloud.openstack_runner_manager import (
    OpenStackRunnerManagerConfig,
)


class QueueConfig(BaseModel):
    """The configuration for the message queue.

    Attributes:
        mongodb_uri: The URI of the MongoDB database.
        queue_name: The name of the queue.
    """

    mongodb_uri: MongoDsn
    queue_name: str


class RunnerConfig(BaseModel):
    """The configuration for the reactive runner to spawn.

    Attributes:
        queue: The queue configuration.
        runner_manager: The runner manager configuration.
        cloud_runner_manager: The OpenStack runner manager configuration.
        github_token: str
        supported_labels: The supported labels for the runner.
    """

    queue: QueueConfig
    runner_manager: RunnerManagerConfig
    cloud_runner_manager: OpenStackRunnerManagerConfig
    github_token: str
    supported_labels: tuple[str, ...]
