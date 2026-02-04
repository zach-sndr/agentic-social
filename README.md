# agentic-social

A collection of AI-powered skills for social media content creation and interaction.

## Skills

### [x-write](./skills/x-write/README.md)

Viral-optimized X (Twitter) content creation built on X's open-sourced algorithm.

**Features:**
- Generates tweets optimized for replies (20x weight), OON discovery (90% priority)
- Uses exact algorithm weights from Twitter's leaked source code
- Creates content that triggers engagement and discovery
- Analyzes and optimizes existing tweets

**Quick start:**
```
/skills x-write write "a tweet about AI agents"
/skills x-write strategy "my launch announcement"
/skills x-write reply "@elonmusk tweet-content"
```

---

### [x-api](./skills/x-api/README.md)

X (Twitter) API v2 integration for posting, managing, and retrieving content.

**Features:**
- Post tweets, replies, quotes, and media
- Manage posts (delete, retweet, like)
- Send DMs with optional media
- Search tweets with filters and operators
- Get user posts and home timeline

**Quick start:**
```bash
# Search tweets
python3 scripts/search_tweets.py "from:user" 10 24h

# Get timeline
python3 scripts/get_timeline.py 20
```

## Installation

```bash
npx skills add zach-sndr/agentic-social
```

## Contributing

Contributions welcome! Add new social media platform skills, improve algorithms, or fix bugs.

## License

MIT License - see [LICENSE](./LICENSE) file for details.
