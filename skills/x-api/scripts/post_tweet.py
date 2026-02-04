#!/usr/bin/env python3
"""
Post a tweet to X.

Usage: python3 post_tweet.py "Your tweet text"
"""

import sys
import os

# Add scripts directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from x_api_client import get_client, XAPIClientError


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 post_tweet.py <tweet text>")
        sys.exit(1)

    text = sys.argv[1]

    try:
        client = get_client()
        result = client.post_tweet(text)

        if "data" in result:
            tweet_id = result["data"]["id"]
            print(f"Tweet posted successfully!")
            print(f"Tweet ID: {tweet_id}")
            print(f"URL: https://x.com/i/status/{tweet_id}")
        else:
            print(f"Error posting tweet: {result}")
            sys.exit(1)

    except XAPIClientError as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
