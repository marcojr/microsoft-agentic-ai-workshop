import argparse
import json
import os
from pathlib import Path

from azure.servicebus import ServiceBusClient
from dotenv import load_dotenv


ROOT = Path(__file__).resolve().parents[2]
load_dotenv(ROOT / "mcp-server" / ".env")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--queue",
        default=os.getenv("SERVICE_BUS_AGENT_RUN_EVENTS_QUEUE", "agent-run-events"),
    )
    parser.add_argument("--max-messages", type=int, default=5)
    args = parser.parse_args()

    connection_string = os.getenv("AZURE_SERVICE_BUS_CONNECTION_STRING", "")
    if not connection_string:
        raise RuntimeError("AZURE_SERVICE_BUS_CONNECTION_STRING is required")

    with ServiceBusClient.from_connection_string(connection_string) as client:
        with client.get_queue_receiver(queue_name=args.queue) as receiver:
            messages = receiver.peek_messages(max_message_count=args.max_messages)

    print(f"queue={args.queue}")
    print(f"messages={len(messages)}")
    for index, message in enumerate(messages, start=1):
        body = b"".join(message.body).decode("utf-8")
        try:
            payload = json.loads(body)
        except json.JSONDecodeError:
            payload = body
        print(f"\nmessage {index}")
        print(json.dumps(payload, indent=2) if isinstance(payload, dict) else payload)


if __name__ == "__main__":
    main()
