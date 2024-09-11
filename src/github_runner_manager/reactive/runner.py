#!/usr/bin/env python3
#  Copyright 2024 Canonical Ltd.
#  See LICENSE file for licensing details.

"""Script to spawn a reactive runner process."""
import logging
import os
import sys

from pydantic import BaseModel

from github_runner_manager.manager.cloud_runner_manager import GitHubRunnerConfig
from github_runner_manager.manager.runner_manager import RunnerManagerConfig
from github_runner_manager.openstack_cloud.openstack_runner_manager import OpenStackCloudConfig, \
    OpenStackServerConfig
from github_runner_manager.reactive.consumer import consume, QueueConfig
from github_runner_manager.reactive.runner_manager import MQ_URI_ENV_VAR, QUEUE_NAME_ENV_VAR


def setup_root_logging() -> None:
    """Set up logging for the reactive runner process."""
    # setup root logger to log in a file which will be picked up by grafana agent and sent to Loki
    logging.basicConfig(
        stream=sys.stdout,
        level=logging.DEBUG,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )


class ReactiveRunnerConfig(BaseModel):
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


def main() -> None:
    """Spawn a process that consumes a message from the queue to create a runner.

    Raises:
        ValueError: If the required environment variables are not set
    """
    mq_uri = os.environ.get(MQ_URI_ENV_VAR)
    queue_name = os.environ.get(QUEUE_NAME_ENV_VAR)

    if not mq_uri:
        raise ValueError(
            f"Missing {MQ_URI_ENV_VAR} environment variable. "
            "Please set it to the message queue URI."
        )

    if not queue_name:
        raise ValueError(
            f"Missing {QUEUE_NAME_ENV_VAR} environment variable. "
            "Please set it to the name of the queue."
        )

    setup_root_logging()
    consume(mq_uri, queue_name)


if __name__ == "__main__":
    main()
