#  Copyright 2024 Canonical Ltd.
#  See LICENSE file for licensing details.
from random import randint
from unittest.mock import MagicMock

import pytest

import github_runner_manager.reactive.process_manager
from github_runner_manager.manager.runner_manager import FlushMode, RunnerInstance, RunnerManager
from github_runner_manager.reactive.runner_manager import reconcile
from github_runner_manager.reactive.types_ import QueueConfig, RunnerConfig


@pytest.mark.parametrize(
    "runner_quantity, desired_quantity, expected_process_quantity",
    [
        pytest.param(5, 5, 0, id="zero processes to spawn"),
        pytest.param(5, 10, 5, id="5 processes to spawn"),
        pytest.param(5, 7, 2, id="2 processes to spawn"),
        pytest.param(0, 5, 5, id="no runners running"),
        pytest.param(0, 0, 0, id="zero quantity"),
    ],
)
def test_reconcile_positive_runner_diff(
    runner_quantity: int,
    desired_quantity: int,
    expected_process_quantity: int,
    monkeypatch: pytest.MonkeyPatch,
):
    """
    arrange: Mock the difference of amount of runners and desired quantity to be positive.
    act: Call reconcile.
    assert: The cleanup method of runner manager is called and the reconcile method of
        process manager is called with the expected quantity.
    """
    runner_manager = MagicMock(spec=RunnerManager)
    runner_manager.get_runners = MagicMock(
        return_value=(tuple(MagicMock(spec=RunnerInstance) for _ in range(runner_quantity)))
    )
    reactive_process_manager = MagicMock(spec=github_runner_manager.reactive.process_manager)
    runner_config = MagicMock(spec=RunnerConfig)
    runner_config.queue = MagicMock(spec=QueueConfig)
    monkeypatch.setattr(
        "github_runner_manager.reactive.runner_manager.process_manager",
        reactive_process_manager,
    )
    monkeypatch.setattr(
        "github_runner_manager.reactive.runner_manager.get_queue_size",
        lambda _: randint(1, 10),
    )

    reconcile(desired_quantity, runner_manager, runner_config)
    runner_manager.cleanup.assert_called_once()
    reactive_process_manager.reconcile.assert_called_once_with(
        quantity=expected_process_quantity, runner_config=runner_config
    )


@pytest.mark.parametrize(
    "runner_quantity, desired_quantity, expected_number_of_runners_to_delete",
    [
        pytest.param(6, 5, 1, id="one additional runner"),
        pytest.param(8, 5, 3, id="multiple additional runners"),
        pytest.param(10, 0, 10, id="zero desired quantity"),
    ],
)
def test_reconcile_negative_runner_diff(
    runner_quantity: int,
    desired_quantity: int,
    expected_number_of_runners_to_delete: int,
    monkeypatch: pytest.MonkeyPatch,
):
    """
    arrange: Mock the difference of amount of runners and desired quantity to be negative.
    act: Call reconcile.
    assert: The additional amount of runners are deleted and the reconcile method of the
        process manager is called with zero quantity.
    """
    runner_manager = MagicMock(spec=RunnerManager)
    runner_manager.get_runners = MagicMock(
        return_value=(tuple(MagicMock(spec=RunnerInstance) for _ in range(runner_quantity)))
    )
    reactive_process_manager = MagicMock(spec=github_runner_manager.reactive.process_manager)
    runner_config = MagicMock(spec=RunnerConfig)
    runner_config.queue = MagicMock(spec=QueueConfig)
    monkeypatch.setattr(
        "github_runner_manager.reactive.runner_manager.process_manager",
        reactive_process_manager,
    )
    monkeypatch.setattr(
        "github_runner_manager.reactive.runner_manager.get_queue_size",
        lambda _: randint(1, 10),
    )

    reconcile(desired_quantity, runner_manager, runner_config)
    runner_manager.cleanup.assert_called_once()
    runner_manager.delete_runners.assert_called_once_with(expected_number_of_runners_to_delete)
    reactive_process_manager.reconcile.assert_called_once_with(
        quantity=0, runner_config=runner_config
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
