#!/usr/bin/env python3
"""
Delete a tweet.

Usage: python3 delete_post.py <post_url_or_id>
"""

import sys
import os

# Add scripts directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from x_api_client import get_client, XAPIClientError


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 delete_post.py <post_url_or_id>")
        sys.exit(1)

    post_link = sys.argv[1]

    try:
        client = get_client()
        result = client.delete_post(post_link)

        if result.get("data", {}).get("deleted"):
            print("Post deleted successfully!")
        else:
            print(f"Error deleting post: {result}")
            sys.exit(1)

    except XAPIClientError as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
