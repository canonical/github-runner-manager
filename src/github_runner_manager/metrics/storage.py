#  Copyright 2024 Canonical Ltd.
#  See LICENSE file for licensing details.

"""Classes and functions defining the metrics storage.

It contains a protocol and reference implementation.
"""
import logging
import shutil
import tarfile
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Iterator, Protocol


from github_runner_manager.errors import (
    CreateMetricsStorageError,
    DeleteMetricsStorageError,
    GetMetricsStorageError,
    QuarantineMetricsStorageError,
)
from github_runner_manager.types_ import SystemUserConfig

_FILESYSTEM_BASE_DIR_NAME = "runner-fs"
_FILESYSTEM_QUARANTINE_DIR_NAME = "runner-fs-quarantine"

logger = logging.getLogger(__name__)


@dataclass
class MetricsStorage:
    """Storage for the metrics.

    Attributes:
        path: The path to the directory holding the metrics inside the charm.
        runner_name: The name of the associated runner.
    """

    path: Path
    runner_name: str


class StorageManagerProtocol(Protocol):  # pylint: disable=too-few-public-methods
    """A protocol defining the methods for managing the metrics storage.

    Attributes:
        create: Method to create a new storage. Returns the created storage.
          Raises an exception CreateMetricsStorageError if the storage already exists.
        list_all: Method to list all storages.
        get: Method to get a storage by name.
        delete: Method to delete a storage by name.
        move_to_quarantine: Method to archive and delete a storage by name.
    """

    create: Callable[[str], MetricsStorage]
    list_all: Callable[[], Iterator[MetricsStorage]]
    get: Callable[[str], MetricsStorage]
    delete: Callable[[str], None]
    move_to_quarantine: Callable[[str], None]


class StorageManager(StorageManagerProtocol):
    """Manager for the metrics storage."""

    def __init__(self, system_user_config: SystemUserConfig):
        """Initialize the storage manager.

        Args:
            system_user_config: The configuration to decide which user to use to create the storage.
        """
        self._system_user_config = system_user_config

    def create(self, runner_name: str) -> MetricsStorage:
        """Create metrics storage for the runner.

        The method is not idempotent and will raise an exception
        if the storage already exists.

        Args:
            runner_name: The name of the runner.

        Returns:
            The metrics storage object.

        Raises:
            CreateMetricsStorageError: If the creation of the shared filesystem fails.
        """
        try:
            base_dir = self._get_filesystem_base_dir_path(self._system_user_config.user)
            base_dir.mkdir(exist_ok=True)
            # this could be executed as root (e.g. during a charm hook), therefore set permissions
            shutil.chown(
                base_dir, user=self._system_user_config.user, group=self._system_user_config.group
            )
            logger.debug(
                "Changed ownership of %s to %s:%s",
                _FILESYSTEM_BASE_DIR_NAME,
                self._system_user_config.user,
                self._system_user_config.group,
            )

            quarantine_dir = self._get_filesystem_quarantine_dir_path(
                self._system_user_config.user
            )
            quarantine_dir.mkdir(exist_ok=True)
            shutil.chown(
                quarantine_dir,
                user=self._system_user_config.user,
                group=self._system_user_config.group,
            )
            logger.debug(
                "Changed ownership of %s to %s:%s",
                quarantine_dir,
                self._system_user_config.user,
                self._system_user_config.group,
            )

        except OSError as exc:
            raise CreateMetricsStorageError(
                "Failed to create metrics storage directories"
            ) from exc

        runner_fs_path = self._get_runner_fs_path(
            runner_name=runner_name, system_user=self._system_user_config.user
        )

        try:
            runner_fs_path.mkdir()
        except FileExistsError as exc:
            raise CreateMetricsStorageError(
                f"Metrics storage for runner {runner_name} already exists."
            ) from exc

        return MetricsStorage(runner_fs_path, runner_name)

    def list_all(self) -> Iterator[MetricsStorage]:
        """List all the metric storages.

        Args:

        Yields:
            A metrics storage object.
        """
        if not (
            base_dir := self._get_filesystem_base_dir_path(self._system_user_config.user)
        ).exists():
            return

        directories = (entry for entry in base_dir.iterdir() if entry.is_dir())
        for directory in directories:
            try:
                fs = self.get(runner_name=directory.name)
            except GetMetricsStorageError:
                logger.error("Failed to get metrics storage for runner %s", directory.name)
            else:
                yield fs

    def get(self, runner_name: str) -> MetricsStorage:
        """Get the metrics storage for the runner.

        Args:
            runner_name: The name of the runner.

        Returns:
            The metrics storage object.

        Raises:
            GetMetricsStorageError: If the storage does not exist.
        """
        runner_fs_path = self._get_runner_fs_path(
            runner_name=runner_name, system_user=self._system_user_config.user
        )
        if not runner_fs_path.exists():
            raise GetMetricsStorageError(f"Metrics storage for runner {runner_name} not found.")

        return MetricsStorage(runner_fs_path, runner_name)

    def delete(self, runner_name: str) -> None:
        """Delete the metrics storage for the runner.

        Args:
            runner_name: The name of the runner.

        Raises:
            DeleteMetricsStorageError: If the storage could not be deleted.
        """
        runner_fs_path = self._get_runner_fs_path(
            runner_name=runner_name, system_user=self._system_user_config.user
        )

        try:
            shutil.rmtree(runner_fs_path)
        except OSError as exc:
            raise DeleteMetricsStorageError(
                f"Failed to remove metrics storage for runner {runner_name}"
            ) from exc

    def move_to_quarantine(
        self,
        runner_name: str,
    ) -> None:
        """Archive the metrics storage for the runner and delete it.

        Args:
            storage_manager: The storage manager.
            runner_name: The name of the runner.

        Raises:
            QuarantineMetricsStorageError: If the metrics storage could not be quarantined.
        """
        try:
            runner_fs = self.get(runner_name)
        except GetMetricsStorageError as exc:
            raise QuarantineMetricsStorageError(
                f"Failed to get metrics storage for runner {runner_name}"
            ) from exc

        tarfile_path = (
            self._get_filesystem_quarantine_dir_path(self._system_user_config.user)
            .joinpath(runner_name)
            .with_suffix(".tar.gz")
        )
        try:
            with tarfile.open(tarfile_path, "w:gz") as tar:
                tar.add(runner_fs.path, arcname=runner_fs.path.name)
        except OSError as exc:
            raise QuarantineMetricsStorageError(
                f"Failed to archive metrics storage for runner {runner_name}"
            ) from exc

        try:
            self.delete(runner_name)
        except DeleteMetricsStorageError as exc:
            raise QuarantineMetricsStorageError(
                f"Failed to delete metrics storage for runner {runner_name}"
            ) from exc

    @staticmethod
    def _get_runner_fs_path(runner_name: str, system_user: str) -> Path:
        """Get the path of the runner metrics storage.

        Args:
            runner_name: The name of the runner.
            system_user: The name of the system user used to determine the storage location.

        Returns:
            The path of the runner shared filesystem.
        """
        return StorageManager._get_filesystem_base_dir_path(system_user) / runner_name

    @staticmethod
    def _get_filesystem_base_dir_path(system_user: str) -> Path:
        """Get the path of the runner metrics storage.

        Args:
            system_user: The name of the system user used to determine the storage location.

        Returns:
            The path of the runner metrics storage.
        """
        return Path(f"~{system_user}").expanduser() / _FILESYSTEM_BASE_DIR_NAME

    @staticmethod
    def _get_filesystem_quarantine_dir_path(system_user: str) -> Path:
        """Get the path of the runner metrics quarantine storage.

        Args:
            system_user: The name of the system user used to determine the storage location.

        Returns:
            The path of the runner metrics quarantine storage.
        """
        return Path(f"~{system_user}").expanduser() / _FILESYSTEM_QUARANTINE_DIR_NAME
