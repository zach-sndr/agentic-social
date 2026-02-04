#!/usr/bin/env python3
"""
Retweet a post.

Usage: python3 retweet.py <post_url_or_id_to_retweet>
"""

import sys
import os

# Add scripts directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from x_api_client import get_client, XAPIClientError


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 retweet.py <post_url_or_id_to_retweet>")
        sys.exit(1)

    post_link = sys.argv[1]

    try:
        client = get_client()
        result = client.retweet(post_link)

        if "data" in result:
            # API returns 'rest_id' for the retweet ID
            retweet_id = result["data"].get("rest_id") or result["data"].get("id")
            print(f"Retweeted successfully!")
            print(f"Retweet ID: {retweet_id}")
            print(f"URL: https://x.com/i/status/{retweet_id}")
        else:
            print(f"Error retweeting: {result}")
            sys.exit(1)

    except XAPIClientError as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
