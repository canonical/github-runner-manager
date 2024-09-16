#  Copyright 2024 Canonical Ltd.
#  See LICENSE file for licensing details.

import secrets
from contextlib import closing
from queue import Empty
from unittest.mock import MagicMock

import pytest
from kombu import Connection, Message

from github_runner_manager.reactive import consumer
from github_runner_manager.reactive.consumer import JobError
from github_runner_manager.reactive.types_ import QueueConfig

IN_MEMORY_URI = "memory://"
FAKE_RUN_URL = "https://api.github.com/repos/fakeusergh-runner-test/actions/runs/8200803099"


@pytest.fixture(name="queue_config")
def queue_config_fixture() -> QueueConfig:
    """Return a QueueConfig object."""
    queue_name = secrets.token_hex(16)

    # we use construct to avoid pydantic validation as IN_MEMORY_URI is not a valid URL
    return QueueConfig.construct(mongodb_uri=IN_MEMORY_URI, queue_name=queue_name)


@pytest.fixture(name="mock_sleep", autouse=True)
def mock_sleep_fixture(monkeypatch: pytest.MonkeyPatch) -> None:
    """Mock the sleep function."""
    monkeypatch.setattr(consumer, "sleep", lambda _: None)


def test_consume(monkeypatch: pytest.MonkeyPatch, queue_config: QueueConfig):
    """
    arrange: A job placed in the message queue which has not yet been picked up.
    act: Call consume.
    assert: A runner is created and the message is acknowledged.
    """
    job_details = consumer.JobDetails(
        labels=[secrets.token_hex(16), secrets.token_hex(16)],
        run_url=FAKE_RUN_URL,
    )
    _put_in_queue(job_details.json(), queue_config.queue_name)

    runner_manager_mock = MagicMock(spec=consumer.RunnerManager)
    github_client_mock = MagicMock(spec=consumer.GithubClient)
    github_client_mock.get.side_effect = [
        {"status": "queued"},
        {"status": consumer.JobPickedUpStates.IN_PROGRESS},
    ]

    consumer.consume(
        queue_config=queue_config,
        runner_manager=runner_manager_mock,
        github_client=github_client_mock,
    )

    runner_manager_mock.create_runners.assert_called_once_with(1)

    # Ensure message has been acknowledged by assuming an Empty exception is raised
    with pytest.raises(Empty):
        _consume_from_queue(queue_config.queue_name)


def test_consume_reject_if_job_gets_not_picked_up(
    monkeypatch: pytest.MonkeyPatch, queue_config: QueueConfig
):
    """
    arrange: A job placed in the message queue which will not get picked up.
    act: Call consume.
    assert: The message is requeued.
    """
    job_details = consumer.JobDetails(
        labels=[secrets.token_hex(16), secrets.token_hex(16)],
        run_url=FAKE_RUN_URL,
    )
    _put_in_queue(job_details.json(), queue_config.queue_name)

    runner_manager_mock = MagicMock(spec=consumer.RunnerManager)
    github_client_mock = MagicMock(spec=consumer.GithubClient)
    github_client_mock.get.return_value = {"status": "queued"}

    consumer.consume(
        queue_config=queue_config,
        runner_manager=runner_manager_mock,
        github_client=github_client_mock,
    )

    # Ensure message has been requeued by reconsuming it
    msg = _consume_from_queue(queue_config.queue_name)
    assert msg.payload == job_details.json()


@pytest.mark.parametrize(
    "job_str",
    [
        pytest.param(
            '{"labels": ["label1", "label2"], "status": "completed"}', id="run_url missing"
        ),
        pytest.param(
            '{"status": "completed", "run_url": "https://example.com"}', id="labels missing"
        ),
        pytest.param("no json at all", id="invalid json"),
    ],
)
def test_job_details_validation_error(job_str: str, queue_config: QueueConfig):
    """
    arrange: A job placed in the message queue with invalid details.
    act: Call consume
    assert: A JobError is raised and the message is requeued.
    """
    queue_name = queue_config.queue_name
    _put_in_queue(job_str, queue_name)

    runner_manager_mock = MagicMock(spec=consumer.RunnerManager)
    github_client_mock = MagicMock(spec=consumer.GithubClient)
    github_client_mock.get.return_value = {"status": consumer.JobPickedUpStates.IN_PROGRESS}

    with pytest.raises(JobError) as exc_info:
        consumer.consume(
            queue_config=queue_config,
            runner_manager=runner_manager_mock,
            github_client=github_client_mock,
        )
    assert "Invalid job details" in str(exc_info.value)

    # Ensure message has been requeued by reconsuming it
    msg = _consume_from_queue(queue_name)
    assert msg.payload == job_str


def _put_in_queue(msg: str, queue_name: str) -> None:
    """Put a job in the message queue.

    Args:
        msg: The job details.
        queue_name: The name of the queue
    """
    with Connection(IN_MEMORY_URI) as conn:
        with closing(conn.SimpleQueue(queue_name)) as simple_queue:
            simple_queue.put(msg, retry=True)


def _consume_from_queue(queue_name: str) -> Message:
    """Consume a job from the message queue.

    Args:
        queue_name: The name of the queue

    Returns:
        The message consumed from the queue.
    """
    with Connection(IN_MEMORY_URI) as conn:
        with closing(conn.SimpleQueue(queue_name)) as simple_queue:
            return simple_queue.get(block=False)
