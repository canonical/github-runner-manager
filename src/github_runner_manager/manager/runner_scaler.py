# Copyright 2024 Canonical Ltd.
# See LICENSE file for licensing details.

"""Module for scaling the runners amount."""

import logging
import time
from dataclasses import dataclass

import github_runner_manager.reactive.runner_manager as reactive_runner_manager
from github_runner_manager.errors import IssueMetricEventError, MissingServerConfigError
from github_runner_manager.manager.cloud_runner_manager import HealthState
from github_runner_manager.manager.github_runner_manager import GitHubRunnerState
from github_runner_manager.manager.runner_manager import (
    FlushMode,
    IssuedMetricEventsStats,
    RunnerInstance,
    RunnerManager,
)
from github_runner_manager.metrics import events as metric_events
from github_runner_manager.reactive.types_ import RunnerConfig as ReactiveRunnerConfig

logger = logging.getLogger(__name__)


@dataclass
class RunnerInfo:
    """Information on the runners.

    Attributes:
        online: The number of runner in online state.
        busy: The number of the runner in busy state.
        offline: The number of runner in offline state.
        unknown: The number of runner in unknown state.
        runners: The names of the online runners.
        busy_runners: The names of the busy runners.
    """

    online: int
    busy: int
    offline: int
    unknown: int
    runners: tuple[str, ...]
    busy_runners: tuple[str, ...]


class RunnerScaler:
    """Manage the reconcile of runners."""

    def __init__(
        self, runner_manager: RunnerManager, reactive_runner_config: ReactiveRunnerConfig | None
    ):
        """Construct the object.

        Args:
            runner_manager: The RunnerManager to perform runner reconcile.
            reactive_runner_config: Reactive runner configuration.
        """
        self._manager = runner_manager
        self._reactive_config = reactive_runner_config

    def get_runner_info(self) -> RunnerInfo:
        """Get information on the runners.

        Returns:
            The information on the runners.
        """
        runner_list = self._manager.get_runners()
        online = 0
        busy = 0
        offline = 0
        unknown = 0
        online_runners = []
        busy_runners = []
        for runner in runner_list:
            match runner.github_state:
                case GitHubRunnerState.BUSY:
                    online += 1
                    online_runners.append(runner.name)
                    busy += 1
                    busy_runners.append(runner.name)
                case GitHubRunnerState.IDLE:
                    online += 1
                    online_runners.append(runner.name)
                case GitHubRunnerState.OFFLINE:
                    offline += 1
                case _:
                    unknown += 1
        return RunnerInfo(
            online=online,
            busy=busy,
            offline=offline,
            unknown=unknown,
            runners=tuple(online_runners),
            busy_runners=tuple(busy_runners),
        )

    def flush(self, flush_mode: FlushMode = FlushMode.FLUSH_IDLE) -> int:
        """Flush the runners.

        Args:
            flush_mode: Determines the types of runner to be flushed.

        Returns:
            Number of runners flushed.
        """
        metric_stats = self._manager.cleanup()
        delete_metric_stats = self._manager.flush_runners(flush_mode=flush_mode)
        events = set(delete_metric_stats.keys()) | set(metric_stats.keys())
        metric_stats = {
            event_name: delete_metric_stats.get(event_name, 0) + metric_stats.get(event_name, 0)
            for event_name in events
        }
        return metric_stats.get(metric_events.RunnerStop, 0)

    def reconcile(self, quantity: int) -> int:
        """Reconcile the quantity of runners.

        Args:
            quantity: The number of intended runners.

        Returns:
            The Change in number of runners.
        """
        logger.info("Start reconcile to %s runner", quantity)

        if self._reactive_config is not None:
            logger.info("Reactive configuration detected, going into experimental reactive mode.")
            return self._reconcile_reactive(quantity)

        metric_stats = {}
        start_timestamp = time.time()

        try:
            delete_metric_stats = None
            metric_stats = self._manager.cleanup()
            runners = self._manager.get_runners()
            logger.info("Reconcile runners from %s to %s", len(runners), quantity)
            runner_diff = quantity - len(runners)
            if runner_diff > 0:
                try:
                    self._manager.create_runners(runner_diff)
                except MissingServerConfigError:
                    logging.exception(
                        "Unable to spawn runner due to missing server configuration, "
                        "such as, image."
                    )
            elif runner_diff < 0:
                delete_metric_stats = self._manager.delete_runners(-runner_diff)
            else:
                logger.info("No changes to the number of runners.")

            # Merge the two metric stats.
            if delete_metric_stats is not None:
                metric_stats = {
                    event_name: delete_metric_stats.get(event_name, 0)
                    + metric_stats.get(event_name, 0)
                    for event_name in set(delete_metric_stats) | set(metric_stats)
                }
        finally:
            runner_list = self._manager.get_runners()
            self._log_runners(runner_list)
            end_timestamp = time.time()
            self._issue_reconciliation_metric(
                start_timestamp, end_timestamp, metric_stats, runner_list
            )

        return runner_diff

    @staticmethod
    def _log_runners(runner_list: tuple[RunnerInstance]) -> None:
        """Log information about the runners found.

        Args:
            runner_list: The list of runners.
        """
        for runner in runner_list:
            logger.info(
                "Runner %s: state=%s, health=%s",
                runner.name,
                runner.github_state,
                runner.health,
            )
        busy_runners = [
            runner for runner in runner_list if runner.github_state == GitHubRunnerState.BUSY
        ]
        idle_runners = [
            runner for runner in runner_list if runner.github_state == GitHubRunnerState.IDLE
        ]
        offline_healthy_runners = [
            runner
            for runner in runner_list
            if runner.github_state == GitHubRunnerState.OFFLINE
            and runner.health == HealthState.HEALTHY
        ]
        unhealthy_states = {HealthState.UNHEALTHY, HealthState.UNKNOWN}
        unhealthy_runners = [runner for runner in runner_list if runner.health in unhealthy_states]
        logger.info("Found %s busy runners: %s", len(busy_runners), busy_runners)
        logger.info("Found %s idle runners: %s", len(idle_runners), idle_runners)
        logger.info(
            "Found %s offline runners that are healthy: %s",
            len(offline_healthy_runners),
            offline_healthy_runners,
        )
        logger.info("Found %s unhealthy runners: %s", len(unhealthy_runners), unhealthy_runners)

    def _issue_reconciliation_metric(
        self,
        start_timestamp: float,
        end_timestamp: float,
        metric_stats: IssuedMetricEventsStats,
        runner_list: tuple[RunnerInstance],
    ) -> None:
        """Issue the reconciliation metric.

        Args:
            start_timestamp: The start timestamp of the reconciliation.
            end_timestamp: The end timestamp of the reconciliation.
            metric_stats: The metric stats.
            runner_list: The list of runners.
        """
        idle_runners = [
            runner for runner in runner_list if runner.github_state == GitHubRunnerState.IDLE
        ]
        offline_healthy_runners = [
            runner
            for runner in runner_list
            if runner.github_state == GitHubRunnerState.OFFLINE
            and runner.health == HealthState.HEALTHY
        ]

        try:
            available_runners = set(runner.name for runner in idle_runners) | set(
                runner.name for runner in offline_healthy_runners
            )
            logger.info(
                "Current available runners (idle + healthy offline): %s", available_runners
            )
            metric_events.issue_event(
                metric_events.Reconciliation(
                    timestamp=time.time(),
                    flavor=self._manager.manager_name,
                    crashed_runners=metric_stats.get(metric_events.RunnerStart, 0)
                    - metric_stats.get(metric_events.RunnerStop, 0),
                    idle_runners=len(available_runners),
                    duration=end_timestamp - start_timestamp,
                )
            )
        except IssueMetricEventError:
            logger.exception("Failed to issue Reconciliation metric")

    def _reconcile_reactive(self, quantity: int) -> int:
        """Reconcile runners reactively.

        Args:
            quantity: Number of intended runners.

        Returns:
            The difference between intended runners and actual runners. In reactive mode
            this number is never negative as additional processes should terminate after a timeout.
        """
        logger.info("Reactive mode is experimental and not yet fully implemented.")
        self._manager.cleanup()
        return reactive_runner_manager.reconcile(
            quantity=quantity,
            reactive_config=self._reactive_config,
        )
