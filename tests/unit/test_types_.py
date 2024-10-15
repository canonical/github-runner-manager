#  Copyright 2024 Canonical Ltd.
#  See LICENSE file for licensing details.
"""Module for testing the general types."""
import pytest
from pydantic import ValidationError

from github_runner_manager.types_ import ProxyConfig


def test_check_use_aproxy():
    """
    arrange: Create a dictionary of values representing a proxy configuration with use_aproxy set\
        to True but neither http nor https provided.
    act: Call the check_use_aproxy method with the provided values.
    assert: Verify that the method raises a ValueError with the expected message.
    """
    with pytest.raises(ValidationError) as exc_info:
        ProxyConfig(use_aproxy=True)

    assert "aproxy requires http or https to be set" in str(exc_info.value)
