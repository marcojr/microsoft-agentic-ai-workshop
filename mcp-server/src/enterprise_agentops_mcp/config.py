import os
from pathlib import Path

from dotenv import load_dotenv

_MCP_ROOT = Path(__file__).resolve().parents[2]
_REPO_ROOT = _MCP_ROOT.parent

load_dotenv(_REPO_ROOT / ".env", override=False)
load_dotenv(_MCP_ROOT / ".env", override=False)
load_dotenv(override=False)

DATA_MODE = os.getenv("MCP_DATA_MODE", "mock")
KNOWLEDGE_MODE = os.getenv(
    "MCP_KNOWLEDGE_MODE",
    "mock" if DATA_MODE == "mock" else "search",
)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

AI_PRIMARY_PROVIDER = os.getenv("AI_PRIMARY_PROVIDER", "azure_openai")
AI_PRIMARY_VENDOR = os.getenv("AI_PRIMARY_VENDOR", "Azure OpenAI")
AI_PRIMARY_MODEL = os.getenv("AI_PRIMARY_MODEL", "gpt-5-mini")

AI_SECONDARY_PROVIDER = os.getenv("AI_SECONDARY_PROVIDER", "gemini")
AI_SECONDARY_VENDOR = os.getenv("AI_SECONDARY_VENDOR", "Gemini")
AI_SECONDARY_MODEL = os.getenv("AI_SECONDARY_MODEL", "gemini-3.5-flash")

AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT", "")
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY", "")
AZURE_OPENAI_DEPLOYMENT_NAME = os.getenv(
    "AZURE_OPENAI_DEPLOYMENT_NAME", "gpt-5-mini"
)

AZURE_AI_SEARCH_ENDPOINT = os.getenv("AZURE_AI_SEARCH_ENDPOINT", "")
AZURE_AI_SEARCH_KEY = os.getenv("AZURE_AI_SEARCH_KEY", "")
AZURE_AI_SEARCH_INDEX = os.getenv("AZURE_AI_SEARCH_INDEX", "enterprise-knowledge")

DATAVERSE_URL = os.getenv("DATAVERSE_URL", "")
DATAVERSE_SP_CLIENT_ID = os.getenv("DATAVERSE_SP_CLIENT_ID", "")
DATAVERSE_SP_CLIENT_SECRET = os.getenv("DATAVERSE_SP_CLIENT_SECRET", "")
DATAVERSE_SP_TENANT_ID = os.getenv("DATAVERSE_SP_TENANT_ID", "")

POWER_AUTOMATE_APPROVAL_URL = os.getenv("POWER_AUTOMATE_APPROVAL_URL", "")
APPLICATION_INSIGHTS_CONNECTION_STRING = os.getenv(
    "APPLICATION_INSIGHTS_CONNECTION_STRING", ""
)

AZURE_SERVICE_BUS_CONNECTION_STRING = os.getenv(
    "AZURE_SERVICE_BUS_CONNECTION_STRING", ""
)
SERVICE_BUS_APPROVAL_REQUESTS_QUEUE = os.getenv(
    "SERVICE_BUS_APPROVAL_REQUESTS_QUEUE", "approval-requests"
)
SERVICE_BUS_AGENT_RUN_EVENTS_QUEUE = os.getenv(
    "SERVICE_BUS_AGENT_RUN_EVENTS_QUEUE", "agent-run-events"
)
SERVICE_BUS_WORKFLOW_DEADLETTER_QUEUE = os.getenv(
    "SERVICE_BUS_WORKFLOW_DEADLETTER_QUEUE", "workflow-deadletter"
)
