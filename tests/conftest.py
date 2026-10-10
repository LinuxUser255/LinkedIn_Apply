"""Shared pytest fixtures."""

import os
from collections.abc import Iterator
from pathlib import Path

import pytest

from src.bot import config, utils


@pytest.fixture(autouse=True)
def restore_runtime_state() -> Iterator[None]:
    """Undo changes that activating a profile makes to process-wide state."""
    saved_env = os.environ.copy()
    saved_config = {name: getattr(config, name) for name in config.SETTING_NAMES}
    saved_data_dir = utils.data_path()
    yield
    os.environ.clear()
    os.environ.update(saved_env)
    for name, value in saved_config.items():
        setattr(config, name, value)
    utils.set_data_dir(saved_data_dir)


@pytest.fixture
def app_home(tmp_path: Path) -> Path:
    """Return an empty folder to hold profiles."""
    return tmp_path / "app_home"


@pytest.fixture
def data_root(tmp_path: Path) -> Path:
    """Return an empty folder to hold per-profile results."""
    return tmp_path / "data"
