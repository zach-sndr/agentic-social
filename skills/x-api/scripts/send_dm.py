#!/usr/bin/env python3
"""
Send a direct message.

Usage: python3 send_dm.py <recipient_handle> <message_text> [path_to_media]
"""

import sys
import os

# Add scripts directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from x_api_client import get_client, XAPIClientError


def main():
    if len(sys.argv) < 3:
        print("Usage: python3 send_dm.py <recipient_handle> <message_text> [path_to_media]")
        sys.exit(1)

    recipient = sys.argv[1]
    text = sys.argv[2]
    media = sys.argv[3] if len(sys.argv) > 3 else None

    try:
        client = get_client()
        result = client.send_dm(recipient, text, media)

        if "data" in result:
            dm_id = result["data"]["dm_event_id"]
            conversation_id = result["data"]["dm_conversation_id"]
            print(f"DM sent successfully!")
            print(f"DM Event ID: {dm_id}")
            print(f"Conversation ID: {conversation_id}")
        else:
            print(f"Error sending DM: {result}")
            sys.exit(1)

    except XAPIClientError as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
