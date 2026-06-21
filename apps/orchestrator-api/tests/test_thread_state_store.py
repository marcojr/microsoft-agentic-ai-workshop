from src.shared.thread_state_store import ThreadStateStore


class _FakeTableClient:
    def __init__(self) -> None:
        self.entities: dict[tuple[str, str], dict] = {}

    def upsert_entity(self, entity: dict) -> None:
        self.entities[(entity["PartitionKey"], entity["RowKey"])] = entity

    def get_entity(self, *, partition_key: str, row_key: str) -> dict:
        return self.entities[(partition_key, row_key)]


def test_thread_state_store_creates_and_rehydrates_thread(tmp_path) -> None:
    store = ThreadStateStore(tmp_path / "thread_state.json")

    first = store.get_or_create(
        thread_id=None,
        workflow_name="WebshopOrderSupport",
        customer_email="john.smith@contoso.com",
        intent="Investigate delayed order",
    )
    second = store.get_or_create(
        thread_id=first.threadId,
        workflow_name="WebshopOrderSupport",
        customer_email=None,
        intent=None,
    )

    assert first.threadId == second.threadId
    assert second.customerEmail == "john.smith@contoso.com"
    assert second.intent == "Investigate delayed order"


def test_thread_state_store_can_use_table_storage_backend() -> None:
    table_client = _FakeTableClient()
    store = ThreadStateStore(mode="table", table_client=table_client)

    first = store.get_or_create(
        thread_id="thread-123",
        workflow_name="WebshopOrderSupport",
        customer_email="john.smith@contoso.com",
        intent="Investigate delayed order",
    )
    first.status = "WaitingForApproval"
    first.approvalId = "apr-123"
    first.context["lastRunId"] = "run-123"
    store.save(first)

    second = store.get_or_create(
        thread_id="thread-123",
        workflow_name="WebshopOrderSupport",
        customer_email=None,
        intent=None,
    )

    assert second.threadId == "thread-123"
    assert second.status == "WaitingForApproval"
    assert second.approvalId == "apr-123"
    assert second.context["lastRunId"] == "run-123"
