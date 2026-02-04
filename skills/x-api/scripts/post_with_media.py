#!/usr/bin/env python3
"""
Post a tweet with media.

Usage: python3 post_with_media.py "Tweet text" <path_to_media_file>
"""

import sys
import os

# Add scripts directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from x_api_client import get_client, XAPIClientError


def main():
    if len(sys.argv) < 3:
        print("Usage: python3 post_with_media.py <tweet text> <path_to_media_file>")
        sys.exit(1)

    text = sys.argv[1]
    media_path = sys.argv[2]

    try:
        client = get_client()
        result = client.post_with_media(text, media_path)

        if "data" in result:
            tweet_id = result["data"]["id"]
            print(f"Tweet with media posted successfully!")
            print(f"Tweet ID: {tweet_id}")
            print(f"URL: https://x.com/i/status/{tweet_id}")
        else:
            print(f"Error posting tweet with media: {result}")
            sys.exit(1)

    except XAPIClientError as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
