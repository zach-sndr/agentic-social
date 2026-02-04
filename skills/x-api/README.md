# x-api

X (Twitter) API v2 integration for posting tweets, replies, quotes, managing posts, sending DMs, searching tweets, and retrieving timeline/user activity.

## Quick Start

Set up credentials in `/root/.env`:
```
X_API_KEY=your_api_key_here
X_API_SECRET=your_api_secret_here
X_ACCESS_TOKEN=your_access_token_here
X_ACCESS_SECRET=your_access_token_secret_here
```

Or set environment variables directly:
```bash
export X_API_KEY=your_api_key_here
export X_API_SECRET=your_api_secret_here
export X_ACCESS_TOKEN=your_access_token_here
export X_ACCESS_SECRET=your_access_token_secret_here
```

## Available Scripts

All scripts are located in `scripts/` directory and can be run directly.

### Search Tweets

```bash
# Basic search
python3 scripts/search_tweets.py "#python"

# Search by user
python3 scripts/search_tweets.py "from:nasa"

# Search with time filter (last 24 hours)
python3 scripts/search_tweets.py "machine learning" 20 24h

# Complex search with hashtag filter
python3 scripts/search_tweets.py "#crypto has:images" 10
```

### Posting Content

```bash
# Post a tweet
python3 scripts/post_tweet.py "Hello world!"

# Post a reply
python3 scripts/post_reply.py "Reply text" "https://x.com/user/status/123456789"

# Post a quote tweet
python3 scripts/post_quote.py "Quote comment" "https://x.com/user/status/123456789"

# Post with media
python3 scripts/post_with_media.py "Caption" /path/to/image.jpg
```

### Managing Posts

```bash
# Delete a post
python3 scripts/delete_post.py "https://x.com/user/status/123456789"

# Retweet
python3 scripts/retweet.py "https://x.com/user/status/123456789"

# Like a post
python3 scripts/like_post.py "https://x.com/user/status/123456789"
```

### Direct Messages

```bash
# Send a DM
python3 scripts/send_dm.py username "Message text"

# Send a DM with media
python3 scripts/send_dm.py username "Check this out" /path/to/image.jpg
```

### Retrieving Data

```bash
# Get user's recent activity
python3 scripts/recent_activity.py elonmusk 2hrs

# Get home timeline
python3 scripts/get_timeline.py 20
```

## Python Client Library

For advanced usage, import the client directly:

```python
from scripts.x_api_client import get_client

client = get_client()

# Post a tweet
result = client.post_tweet("Hello!")

# Search tweets
tweets = client.search_tweets("from:user", max_results=10)

# Get user posts
posts = client.get_user_posts("username", "2hrs", max_results=20)

# Get timeline
timeline = client.get_timeline(count=50)
```

## API Costs (Pay-Per-Use)

| Operation | Cost |
|-----------|------|
| Post (Read) | $0.005 per tweet |
| User (Read) | $0.01 per user |
| DM Event (Read) | $0.01 per DM |
| Content (Create) | $0.01 per request |
| User Interaction | $0.015 per request |

### Rate Limits

| Endpoint | Per User |
|----------|----------|
| Search recent | 300/15min |
| User posts | 900/15min |
| Timeline | 180/15min |

## Authentication

Required credentials (get these from the X Developer Portal):
- `X_API_KEY` - Consumer Key (API Key)
- `X_API_SECRET` - Consumer Secret (API Secret)
- `X_ACCESS_TOKEN` - Access Token
- `X_ACCESS_SECRET` - Access Token Secret

Required permissions/scopes:
- `tweet.write` - Post and repost
- `tweet.read` - View posts
- `users.read` - View users
- `dm.write` - Send DMs
- `like.write` - Like posts
- `media.write` - Upload media
