# Copyright 2024 Canonical Ltd.
# See LICENSE file for licensing details.

"""Module for helper functions interacting with GitHub."""
import pathlib
import platform
import subprocess
import tarfile
import typing

import requests

from github_runner_manager import github_client

ARCHITECTURES_ARM64 = {"aarch64", "arm64"}
ARCHITECTURES_X86 = {"x86_64"}


def register_runner(
    path: github_client.GitHubPath,
    workdir: pathlib.Path,
    test_id: str,
    registration_token: str,
    runner_name: str,
) -> None:
    """Register the GitHub runner.

    Args:
        path: The Path to the GitHub org/repo.
        workdir: The directory in which the client is run.
        test_id: The test run ID.
        registration_token: The GitHub token to register the runner.
        runner_name: The runner name to register as.
    """
    _download_github_client(workdir=workdir)
    stdout = subprocess.check_output(
        [
            f"{workdir}/actions-runner/config.sh",
            "--url",
            f"https://github.com/{path}",
            "--token",
            registration_token,
            "--labels",
            f"manager_integration_test,{test_id}",
            "--name",
            runner_name,
            "--ephemeral",
            "--unattended",
        ],
        encoding="utf-8",
    )
    assert "Runner successfully added" in stdout, f"Failed to register runner, {stdout}"


def _download_github_client(workdir: pathlib.Path):
    """Download the GitHub runner binaries.

    Args:
        workdir: The directory in which the client is downloaded and run.
    """
    # Get latest version of the runner
    arch = _get_arch()
    res = requests.get("https://github.com/actions/runner/releases/latest", allow_redirects=False)
    # example Location header: 'https://github.com/actions/runner/releases/tag/v2.319.1'
    version = res.headers["Location"].split("/")[-1].removeprefix("v")
    runner_url = (
        f"https://github.com/actions/runner/releases/download/v{version}/actions-runner-"
        f"linux-{arch}-{version}.tar.gz"
    )
    download_path = workdir / "actions_runner.tar"

    with requests.get(runner_url, stream=True) as r:
        r.raise_for_status()
        with open(download_path, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)

    with tarfile.open(download_path) as tar:
        tar.extractall()


def _get_arch() -> typing.Literal["arm64", "x64"]:
    """Get GitHub runner architecture.

    Raises:
        ValueError: if unsupported arch is detected.

    Returns:
        The machine architecture.
    """
    arch = platform.machine()
    match arch:
        case arch if arch in ARCHITECTURES_ARM64:
            return "arm64"
        case arch if arch in ARCHITECTURES_X86:
            return "x64"
        case _:
            raise ValueError("Unsupported architecture.")
