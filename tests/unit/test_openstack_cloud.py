#  Copyright 2024 Canonical Ltd.
#  See LICENSE file for licensing details.
import secrets
from pathlib import Path

import pytest
import yaml

from github_runner_manager import openstack_cloud
from github_runner_manager.errors import OpenStackInvalidConfigError


@pytest.fixture(autouse=True, name="clouds_yaml_path")
def clouds_yaml_path(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> Path:
    """Mocked clouds.yaml path.

    Returns:
        Path: Mocked clouds.yaml path.
    """
    clouds_yaml_path = tmp_path / "clouds.yaml"
    monkeypatch.setattr("github_runner_manager.openstack_cloud.CLOUDS_YAML_PATH", clouds_yaml_path)
    return clouds_yaml_path


@pytest.fixture(autouse=True, name="cloud_name")
def cloud_name_fixture() -> str:
    """The testing cloud name."""
    return "microstack"


@pytest.fixture(name="clouds_yaml")
def clouds_yaml_fixture(cloud_name: str) -> dict:
    """Testing clouds.yaml."""
    return {
        "clouds": {
            cloud_name: {
                "auth": {
                    "auth_url": secrets.token_hex(16),
                    "project_name": secrets.token_hex(16),
                    "project_domain_name": secrets.token_hex(16),
                    "username": secrets.token_hex(16),
                    "user_domain_name": secrets.token_hex(16),
                    "password": secrets.token_hex(16),
                }
            }
        }
    }


def test_initialize(clouds_yaml_path: Path, clouds_yaml: dict):
    """
    arrange: Mocked clouds.yaml data and path.
    act: Call initialize.
    assert: The clouds.yaml file is written to disk.
    """
    openstack_cloud.initialize(clouds_yaml)

    assert yaml.safe_load(clouds_yaml_path.read_text(encoding="utf-8")) == clouds_yaml


@pytest.mark.parametrize(
    "invalid_yaml, expected_err_msg",
    [
        pytest.param(
            {"wrong-key": {"cloud_name": {"auth": {}}}}, "Missing key 'clouds' from config."
        ),
        pytest.param({}, "Missing key 'clouds' from config."),
        pytest.param({"clouds": {}}, "No clouds defined in clouds.yaml."),
    ],
)
def test_initialize_validation_error(invalid_yaml: dict, expected_err_msg):
    """
    arrange: Mocked clouds.yaml data with invalid data.
    act: Call initialize.
    assert: InvalidConfigError is raised.
    """
    with pytest.raises(OpenStackInvalidConfigError) as exc:
        openstack_cloud.initialize(invalid_yaml)
    assert expected_err_msg in str(exc)
