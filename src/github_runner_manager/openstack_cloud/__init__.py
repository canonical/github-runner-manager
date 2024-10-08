# Copyright 2024 Canonical Ltd.
# See LICENSE file for licensing details.

"""Module for managing Openstack cloud."""

import logging
from pathlib import Path
from typing import TypedDict, cast

import yaml

from github_runner_manager.errors import OpenStackInvalidConfigError

logger = logging.getLogger(__name__)


CLOUDS_YAML_PATH = Path(Path.home() / ".config/openstack/clouds.yaml")


class CloudConfig(TypedDict):
    """The parsed clouds.yaml configuration dictionary.

    Attributes:
        clouds: A mapping of key "clouds" to cloud name mapped to cloud configuration.
    """

    clouds: dict[str, dict]


def _validate_cloud_config(cloud_config: dict) -> CloudConfig:
    """Validate the format of the cloud configuration.

    Args:
        cloud_config: The configuration in clouds.yaml format to validate.

    Raises:
        OpenStackInvalidConfigError: if the format of the config is invalid.

    Returns:
        A typed cloud_config dictionary.
    """
    # dict of format: {clouds: <cloud-name>: <cloud-config>}
    try:
        clouds = list(cloud_config["clouds"].keys())
    except KeyError as exc:
        raise OpenStackInvalidConfigError("Missing key 'clouds' from config.") from exc
    if not clouds:
        raise OpenStackInvalidConfigError("No clouds defined in clouds.yaml.")
    return cast(CloudConfig, cloud_config)


def _write_config_to_disk(cloud_config: CloudConfig) -> None:
    """Write the cloud configuration to disk.

    Args:
        cloud_config: The configuration in clouds.yaml format to write to disk.
    """
    CLOUDS_YAML_PATH.parent.mkdir(parents=True, exist_ok=True)
    CLOUDS_YAML_PATH.write_text(encoding="utf-8", data=yaml.dump(cloud_config))


def initialize(cloud_config: dict) -> None:
    """Initialize Openstack integration.

    Validates config and writes it to disk.

    Raises:
        OpenStackInvalidConfigError: If there was an given cloud config.

    Args:
        cloud_config: The configuration in clouds.yaml format to apply.
    """
    try:
        valid_config = _validate_cloud_config(cloud_config)
    # TODO: 2024-04-02 - We should define a new error, wrap it and re-raise it.
    except OpenStackInvalidConfigError:  # pylint: disable=try-except-raise
        raise
    _write_config_to_disk(valid_config)
