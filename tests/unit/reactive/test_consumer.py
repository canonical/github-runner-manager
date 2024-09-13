#  Copyright 2024 Canonical Ltd.
#  See LICENSE file for licensing details.

import secrets
from contextlib import closing
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

def test_consume(caplog: pytest.LogCaptureFixture, queue_config: QueueConfig):
    """
    arrange: A job placed in the message queue.
    act: Call consume
    assert: The job is logged.
    """
    job_details = consumer.JobDetails(
        labels=[secrets.token_hex(16), secrets.token_hex(16)],
        run_url=FAKE_RUN_URL,
    )
    _put_in_queue(job_details.json(), queue_config.queue_name)


    consumer.consume(queue_config=queue_config, runner_manager=MagicMock())
    assert str(job_details.labels) in caplog.text
    assert job_details.run_url in caplog.text


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

    with pytest.raises(JobError) as exc_info:
        consumer.consume(queue_config=queue_config, runner_manager=MagicMock())
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
