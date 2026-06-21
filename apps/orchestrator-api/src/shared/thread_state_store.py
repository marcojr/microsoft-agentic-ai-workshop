import json
import os
from pathlib import Path

from src.agents.models import ThreadState, utc_now


class ThreadStateStore:
    """Stores thread state for orchestrator workflows."""

    def __init__(
        self,
        path: Path | None = None,
        *,
        mode: str | None = None,
        table_client: object | None = None,
    ) -> None:
        root = Path(__file__).resolve().parents[2]
        self.path = path or root / ".state" / "thread_state.json"
        self.mode = mode or os.getenv("THREAD_STATE_STORE", "file")
        self.table_name = os.getenv("THREAD_STATE_TABLE_NAME", "AgentThreadState")
        self._table_client = table_client

    def get_or_create(
        self,
        *,
        thread_id: str | None,
        workflow_name: str,
        customer_email: str | None,
        intent: str | None,
    ) -> ThreadState:
        # Step 1: Rehydrate an existing thread when the caller provides one.
        state = self._get(thread_id) if thread_id else None
        if state is not None:
            state.customerEmail = customer_email or state.customerEmail
            state.intent = intent or state.intent
            state.updatedAt = utc_now()
            return self.save(state)

        # Step 2: Create a new workflow thread for this request.
        payload = {
            "workflowName": workflow_name,
            "customerEmail": customer_email,
            "intent": intent,
        }
        if thread_id:
            payload["threadId"] = thread_id
        return self.save(ThreadState(**payload))

    def save(self, state: ThreadState) -> ThreadState:
        # Step 3: Persist thread state for later turns in the same conversation.
        state.updatedAt = utc_now()
        if self.mode == "table":
            self._save_table(state)
            return state
        if self.mode != "file":
            raise ValueError(f"Unsupported THREAD_STATE_STORE: {self.mode}")
        states = self._load()
        states[state.threadId] = state.model_dump()
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps(states, indent=2), encoding="utf-8")
        return state

    def _get(self, thread_id: str | None) -> ThreadState | None:
        if thread_id is None:
            return None
        if self.mode == "table":
            return self._get_table(thread_id)
        if self.mode != "file":
            raise ValueError(f"Unsupported THREAD_STATE_STORE: {self.mode}")
        states = self._load()
        if thread_id not in states:
            return None
        return ThreadState.model_validate(states[thread_id])

    def _load(self) -> dict:
        if not self.path.exists():
            return {}
        return json.loads(self.path.read_text(encoding="utf-8"))

    def _client(self):
        if self._table_client is not None:
            return self._table_client

        connection_string = (
            os.getenv("THREAD_STATE_STORAGE_CONNECTION_STRING")
            or os.getenv("AzureWebJobsStorage")
        )
        if connection_string:
            from azure.data.tables import TableClient

            self._table_client = TableClient.from_connection_string(
                conn_str=connection_string,
                table_name=self.table_name,
            )
            self._table_client.create_table_if_not_exists()
            return self._table_client

        account_url = os.getenv("THREAD_STATE_STORAGE_ACCOUNT_URL")
        if not account_url:
            raise ValueError(
                "THREAD_STATE_STORE=table requires THREAD_STATE_STORAGE_ACCOUNT_URL "
                "or THREAD_STATE_STORAGE_CONNECTION_STRING/AzureWebJobsStorage."
            )

        from azure.data.tables import TableClient
        from azure.identity import DefaultAzureCredential

        self._table_client = TableClient(
            endpoint=account_url,
            table_name=self.table_name,
            credential=DefaultAzureCredential(),
        )
        self._table_client.create_table_if_not_exists()
        return self._table_client

    def _get_table(self, thread_id: str) -> ThreadState | None:
        client = self._client()
        try:
            entity = client.get_entity(partition_key="thread", row_key=thread_id)
        except Exception as exc:
            if exc.__class__.__name__ == "ResourceNotFoundError" or isinstance(exc, KeyError):
                return None
            raise
        return self._entity_to_state(entity)

    def _save_table(self, state: ThreadState) -> None:
        entity = {
            "PartitionKey": "thread",
            "RowKey": state.threadId,
            "threadId": state.threadId,
            "workflowName": state.workflowName,
            "status": state.status,
            "customerEmail": state.customerEmail or "",
            "intent": state.intent or "",
            "orderId": state.orderId or "",
            "approvalId": state.approvalId or "",
            "currentStep": state.currentStep,
            "createdAt": state.createdAt,
            "updatedAt": state.updatedAt,
            "context": json.dumps(state.context),
        }
        self._client().upsert_entity(entity)

    @staticmethod
    def _entity_to_state(entity: dict) -> ThreadState:
        return ThreadState(
            threadId=entity["threadId"],
            workflowName=entity["workflowName"],
            status=entity.get("status", "Started"),
            customerEmail=entity.get("customerEmail") or None,
            intent=entity.get("intent") or None,
            orderId=entity.get("orderId") or None,
            approvalId=entity.get("approvalId") or None,
            currentStep=entity.get("currentStep", "intake"),
            createdAt=entity.get("createdAt"),
            updatedAt=entity.get("updatedAt"),
            context=json.loads(entity.get("context") or "{}"),
        )
