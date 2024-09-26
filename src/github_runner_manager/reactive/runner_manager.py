#  Copyright 2024 Canonical Ltd.
#  See LICENSE file for licensing details.

"""Module for reconciling amount of runner and reactive runner processes."""
import logging

from github_runner_manager.manager.runner_manager import RunnerManager
from github_runner_manager.reactive import process_manager
from github_runner_manager.reactive.types_ import RunnerConfig

logger = logging.getLogger(__name__)


def reconcile(quantity: int, runner_manager: RunnerManager, runner_config: RunnerConfig) -> int:
    """Reconcile runners reactively.

    The reconciliation attempts to make the following equation true:
        quantity_of_current_runners + reactive_processes_consuming_jobs == quantity.

    A few examples:

    1. If there are 5 runners and 5 reactive processes and the quantity is 10,
        no action is taken.
    2. If there are 5 runners and 5 reactive processes and the quantity is 15,
        5 reactive processes are created.
    3. If there are 5 runners and 5 reactive processes and quantity is 7,
        3 reactive processes are killed.
    4. If there are 5 runners and 5 reactive processes and quantity is 5,
        all reactive processes are killed.
    5. If there are 5 runners and 5 reactive processes and quantity is 4,
        1 runner is killed and all reactive processes are killed.


    So if the quantity is equal to the sum of the current runners and reactive processes,
    no action is taken,

    If the quantity is greater than the sum of the current
    runners and reactive processes, additional reactive processes are created.

    If the quantity is greater than or equal to the quantity of the current runners,
    but less than the sum of the current runners and reactive processes,
    additional reactive processes will be killed.

    If the quantity is less than the sum of the current runners,
    additional runners are killed and all reactive processes are killed.

    In addition to this behaviour, reconciliation also checks the queue at the start and
    removes all idle runners if the queue is empty, to ensure that
    no idle runners are left behind if there are no new jobs.

    Args:
        quantity: Number of intended amount of runners + reactive processes.
        runner_manager: The runner manager to interact with current running runners.
        runner_config: The reactive runner config.

    Returns:
        The number of reactive processes created. If negative, its absolute value is equal
        to the number of processes killed.
    """
    runner_manager.cleanup()
    return process_manager.reconcile(
        quantity=quantity,
        runner_config=runner_config,
    )
