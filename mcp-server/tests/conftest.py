import shutil
from pathlib import Path

import pytest

from enterprise_agentops_mcp import config
from enterprise_agentops_mcp.services import mock_data_service
from enterprise_agentops_mcp.tools import (
    accounts,
    approvals,
    cases,
    customers,
    knowledge,
    observability,
    orders,
    returns,
    shipments,
)


SOURCE_DATA_DIR = Path(__file__).resolve().parents[1] / "src" / "enterprise_agentops_mcp" / "data"


@pytest.fixture(autouse=True)
def isolated_mock_data_dir(tmp_path, monkeypatch) -> None:
    data_dir = tmp_path / "data"
    shutil.copytree(SOURCE_DATA_DIR, data_dir)
    monkeypatch.setattr(mock_data_service, "DATA_DIR", data_dir)


def pytest_runtest_setup() -> None:
    config.DATA_MODE = "mock"

    for module in (
        accounts,
        approvals,
        cases,
        customers,
        knowledge,
        observability,
        orders,
        returns,
        shipments,
    ):
        module.DATA_MODE = "mock"
