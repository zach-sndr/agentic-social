#!/usr/bin/env python3
"""
Search for tweets on X (Twitter).

Usage: python3 search_tweets.py <query> [options]

Search operators:
    #hashtag         - Tweets with hashtag
    @username        - Tweets mentioning user
    from:username    - Tweets from specific user
    to:username      - Tweets to specific user
    "phrase"         - Exact phrase match
    keyword1 AND keyword2  - Both keywords
    keyword1 OR keyword2   - Either keyword
    -unwanted        - Exclude keyword
    has:images       - Tweets with images
    has:videos       - Tweets with videos
    has:links        - Tweets with links
    lang:en          - Language filter
    is:verified      - Only verified users
    min_retweets:N   - Minimum retweets
    min_faves:N      - Minimum likes

Examples:
    python3 search_tweets.py "#python"
    python3 search_tweets.py "from:nasa"
    python3 search_tweets.py "machine learning" 20 recency
    python3 search_tweets.py "#crypto has:images" 10
"""

import sys
import os
from datetime import datetime, timedelta, timezone

# Add scripts directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from x_api_client import get_client, XAPIClientError


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    query = sys.argv[1]

    # Parse optional arguments
    max_results = 10
    hours_ago = None

    i = 2
    while i < len(sys.argv):
        arg = sys.argv[i]
        if arg.isdigit():
            max_results = int(arg)
            i += 1
        elif arg.endswith("h") or arg.endswith("hrs") or arg.endswith("hours"):
            # Parse time like "24h" or "48hrs"
            arg_clean = arg.replace("h", "").replace("hrs", "").replace("hours", "")
            try:
                hours_ago = int(arg_clean)
            except:
                pass
            i += 1
        else:
            i += 1

    try:
        client = get_client()

        # Calculate start_time if hours_ago is specified
        start_time = None
        if hours_ago:
            start_time = (datetime.now(timezone.utc) - timedelta(hours=hours_ago)).strftime("%Y-%m-%dT%H:%M:%SZ")

        print(f"Searching for: {query}")
        if hours_ago:
            print(f"Time limit: Last {hours_ago} hours")
        print(f"Max results: {max_results}")
        print()

        results = client.search_tweets(
            query=query,
            max_results=max_results,
            start_time=start_time,
        )

        if not results:
            print("No results found.")
            sys.exit(0)

        print(f"Found {len(results)} result(s):\n")

        for idx, tweet in enumerate(results, 1):
            # Extract tweet data
            tweet_id = tweet.get("id")
            text = tweet.get("text", "")
            created_at = tweet.get("created_at", "")
            metrics = tweet.get("public_metrics", {})
            author = tweet.get("author", {})

            # Format timestamp
            if created_at:
                try:
                    dt = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
                    created_str = dt.strftime("%Y-%m-%d %H:%M:%S UTC")
                except:
                    created_str = created_at
            else:
                created_str = "Unknown"

            # Get author info
            username = author.get("username", "unknown")
            name = author.get("name", "")
            verified = " ✓" if author.get("verified", False) else ""

            # Format metrics
            likes = metrics.get("like_count", 0)
            retweets = metrics.get("retweet_count", 0)
            replies = metrics.get("reply_count", 0)

            print(f"{idx}. [{created_str}] @{username}{verified}")
            if name:
                print(f"   {name}")
            print(f"   {text[:200]}{'...' if len(text) > 200 else ''}")
            print(f"   Likes: {likes} | Retweets: {retweets} | Replies: {replies}")
            print(f"   URL: https://x.com/i/status/{tweet_id}")
            print()

    except XAPIClientError as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
