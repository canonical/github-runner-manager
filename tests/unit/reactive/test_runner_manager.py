#  Copyright 2024 Canonical Ltd.
#  See LICENSE file for licensing details.
from random import randint
from unittest.mock import MagicMock

import pytest

import github_runner_manager.reactive.process_manager
from github_runner_manager.manager.runner_manager import FlushMode, RunnerManager
from github_runner_manager.reactive.runner_manager import reconcile
from github_runner_manager.reactive.types_ import QueueConfig, RunnerConfig


def test_reconcile(monkeypatch: pytest.MonkeyPatch):
    """
    arrange: Mock the dependencies.
    act: Call reconcile with random quantity.
    assert: The cleanup method of runner manager is called and the reconcile method of
        process manager is called.
    """
    runner_manager = MagicMock(spec=RunnerManager)
    reactive_process_manager = MagicMock(spec=github_runner_manager.reactive.process_manager)
    runner_config = MagicMock(spec=RunnerConfig)
    runner_config.queue = MagicMock(spec=QueueConfig)
    quantity = randint(0, 10)
    monkeypatch.setattr(
        "github_runner_manager.reactive.runner_manager.process_manager",
        reactive_process_manager,
    )
    monkeypatch.setattr(
        "github_runner_manager.reactive.runner_manager.get_queue_size",
        lambda _: randint(1, 10),
    )

    reconcile(quantity, runner_manager, runner_config)
    runner_manager.cleanup.assert_called_once()
    reactive_process_manager.reconcile.assert_called_once_with(
        quantity=quantity, runner_config=runner_config
    )


def test_reconcile_flushes_idle_runners_when_queue_is_empty(monkeypatch: pytest.MonkeyPatch):
    """
    arrange: Mock the dependencies and set the queue size to 0.
    act: Call reconcile with random quantity.
    assert: The flush_runners method of runner manager is called with FLUSH_IDLE mode.
    """
    runner_manager = MagicMock(spec=RunnerManager)
    reactive_process_manager = MagicMock(spec=github_runner_manager.reactive.process_manager)
    runner_config = MagicMock(spec=RunnerConfig)
    runner_config.queue = MagicMock(spec=QueueConfig)
    quantity = randint(0, 10)
    monkeypatch.setattr(
        "github_runner_manager.reactive.runner_manager.process_manager",
        reactive_process_manager,
    )
    monkeypatch.setattr(
        "github_runner_manager.reactive.runner_manager.get_queue_size",
        lambda _: 0,
    )

    reconcile(quantity, runner_manager, runner_config)

    runner_manager.flush_runners.assert_called_once_with(FlushMode.FLUSH_IDLE)
