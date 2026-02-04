#!/usr/bin/env python3
"""
Get timeline posts (home timeline).

Usage: python3 get_timeline.py [count] [exclude]

Examples:
    python3 get_timeline.py 20
    python3 get_timeline.py 50 replies
    python3 get_timeline.py 30 replies,retweets
"""

import sys
import os

# Add scripts directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from x_api_client import get_client, XAPIClientError


def main():
    count = 10
    exclude = None

    if len(sys.argv) > 1:
        try:
            count = int(sys.argv[1])
        except ValueError:
            print("Error: count must be a number")
            sys.exit(1)

    if len(sys.argv) > 2:
        exclude = sys.argv[2].split(",")

    try:
        client = get_client()
        posts = client.get_timeline(count=count, exclude=exclude)

        print(f"\nYour Timeline (last {count} posts):")
        print(f"Found {len(posts)} post(s)\n")

        for i, post in enumerate(posts, 1):
            created_at = post.get("created_at", "N/A")
            text = post.get("text", "")
            author_id = post.get("author_id", "N/A")
            metrics = post.get("public_metrics", {})
            tweet_id = post.get("id", "")

            print(f"{i}. [{created_at}] Author ID: {author_id}")
            print(f"   {text[:100]}{'...' if len(text) > 100 else ''}")
            print(f"   Likes: {metrics.get('like_count', 0)} | "
                  f"Retweets: {metrics.get('retweet_count', 0)} | "
                  f"Replies: {metrics.get('reply_count', 0)}")
            print(f"   URL: https://x.com/i/status/{tweet_id}")
            print()

    except XAPIClientError as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
