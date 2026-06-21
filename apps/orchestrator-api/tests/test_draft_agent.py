from src.agents.draft_agent import DraftAgent


def test_parse_contract_returns_typed_fields() -> None:
    contract = DraftAgent._parse_contract(
        """
        {
          "summary": "John Smith's latest order is delayed and requires approval before compensation is communicated.",
          "approvalRequired": true
        }
        """
    )

    assert contract.summary.startswith("John Smith")
    assert contract.approvalRequired is True
