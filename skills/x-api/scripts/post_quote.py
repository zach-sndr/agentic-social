#!/usr/bin/env python3
"""
Post a quote tweet.

Usage: python3 post_quote.py "Quote text" <post_url_or_id_to_quote>
"""

import sys
import os

# Add scripts directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from x_api_client import get_client, XAPIClientError


def main():
    if len(sys.argv) < 3:
        print("Usage: python3 post_quote.py <quote text> <post_url_or_id_to_quote>")
        sys.exit(1)

    text = sys.argv[1]
    quote_post = sys.argv[2]

    try:
        client = get_client()
        result = client.post_quote(text, quote_post)

        if "data" in result:
            tweet_id = result["data"]["id"]
            print(f"Quote tweet posted successfully!")
            print(f"Tweet ID: {tweet_id}")
            print(f"URL: https://x.com/i/status/{tweet_id}")
        else:
            print(f"Error posting quote: {result}")
            sys.exit(1)

    except XAPIClientError as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
