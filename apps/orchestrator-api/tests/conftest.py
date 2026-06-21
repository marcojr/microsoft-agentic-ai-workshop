import shutil
import sys
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[3]
MCP_SRC = ROOT / "mcp-server" / "src"
MCP_DATA_DIR = MCP_SRC / "enterprise_agentops_mcp" / "data"

if str(MCP_SRC) not in sys.path:
    sys.path.insert(0, str(MCP_SRC))


@pytest.fixture(autouse=True)
def isolated_mcp_mock_data_dir(tmp_path, monkeypatch) -> None:
    from enterprise_agentops_mcp.services import mock_data_service

    data_dir = tmp_path / "data"
    shutil.copytree(MCP_DATA_DIR, data_dir)
    monkeypatch.setattr(mock_data_service, "DATA_DIR", data_dir)
