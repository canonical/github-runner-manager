#  Copyright 2024 Canonical Ltd.
#  See LICENSE file for licensing details.
from random import randint
from unittest.mock import MagicMock

import pytest

import github_runner_manager.reactive.process_manager
from github_runner_manager.manager.runner_manager import RunnerManager
from github_runner_manager.reactive.runner_manager import reconcile
from github_runner_manager.reactive.types_ import RunnerConfig


def test_reconcile(monkeypatch: pytest.MonkeyPatch):
    """
    arrange: Mocked runner manager, reactive process manager, runner config and quantity.
    act: Call reconcile.
    assert: The cleanup method of runner manager is called and the reconcile method of
        process manager is called.
    """
    runner_manager = MagicMock(spec=RunnerManager)
    reactive_process_manager = MagicMock(spec=github_runner_manager.reactive.process_manager)
    runner_config = MagicMock(RunnerConfig)
    quantity = randint(0, 10)
    monkeypatch.setattr(
        "github_runner_manager.reactive.runner_manager.process_manager",
        reactive_process_manager,
    )

    reconcile(quantity, runner_manager, runner_config)
    runner_manager.cleanup.assert_called_once()
    reactive_process_manager.reconcile.assert_called_once_with(
        quantity=quantity, runner_config=runner_config
    )
