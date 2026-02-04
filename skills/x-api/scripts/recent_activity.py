#!/usr/bin/env python3
"""
Get recent posts from a user within a specific timeframe.

Usage: python3 recent_activity.py <username> <timeframe> [count]

Examples:
    python3 recent_activity.py elonmusk 2hrs 20
    python3 recent_activity.py nasa 8hrs
    python3 recent_activity.py github 1d 50
"""

import sys
import os
import json

# Add scripts directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from x_api_client import get_client, XAPIClientError


def main():
    if len(sys.argv) < 3:
        print("Usage: python3 recent_activity.py <username> <timeframe> [count]")
        print("Timeframe examples: 2hrs, 8hrs, 1d, 1w")
        sys.exit(1)

    username = sys.argv[1]
    timeframe = sys.argv[2]
    count = int(sys.argv[3]) if len(sys.argv) > 3 else 10

    try:
        client = get_client()
        posts = client.get_user_posts(username, timeframe, max_results=count)

        print(f"\nRecent posts from @{username} (last {timeframe}):")
        print(f"Found {len(posts)} post(s)\n")

        for i, post in enumerate(posts, 1):
            created_at = post.get("created_at", "N/A")
            text = post.get("text", "")
            metrics = post.get("public_metrics", {})
            tweet_id = post.get("id", "")

            print(f"{i}. [{created_at}] ID: {tweet_id}")
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
