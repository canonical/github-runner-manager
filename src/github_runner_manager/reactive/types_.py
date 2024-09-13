#  Copyright 2024 Canonical Ltd.
#  See LICENSE file for licensing details.
from pydantic import BaseModel, MongoDsn

from github_runner_manager.manager.cloud_runner_manager import GitHubRunnerConfig
from github_runner_manager.manager.runner_manager import RunnerManagerConfig
from github_runner_manager.openstack_cloud.openstack_runner_manager import OpenStackCloudConfig, \
    OpenStackServerConfig


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
        runner: The GitHub runner configuration.
        openstack_cloud: The OpenStack cloud configuration.
        openstack_server: The OpenStack server configuration.
    """

    queue: QueueConfig
    runner_manager: RunnerManagerConfig
    runner: GitHubRunnerConfig
    openstack_cloud: OpenStackCloudConfig
    openstack_server: OpenStackServerConfig | None = None
