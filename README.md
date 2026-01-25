# agentic-social

A collection of AI-powered skills for social media content creation and optimization.

## Available Skills

### x-write

Viral-optimized X (Twitter) content creation built on X's open-sourced algorithm.

**What it does:**
- Generates tweets optimized for replies (20x weight), OON discovery (90% priority)
- Uses exact algorithm weights from Twitter's leaked source code
- Creates content that triggers engagement and discovery
- Analyzes and optimizes existing tweets

**Installation:**
```bash
npx add-skill zach-sndr/agentic-social
```

**Usage:**
```
/skills x-write write "a tweet about AI agents"
/skills x-write strategy "my launch announcement"
/skills x-write reply "@elonmusk tweet-content"
```

**Algorithm weights (from source):**
- Reply: 20.0 points (2x baseline, highest weight)
- Retweet: 15.0 points (1.5x baseline)
- Quote Tweet: 15.0 points (1.5x baseline)
- Like: 10.0 points (baseline)

**Key principles:**
- OON (Out-of-Network) discovery = 90% weight
- Follower engagement = 10% weight
- First 6 hours = 91% score potential (critical window)
- 48-hour exponential decay half-life

## Installation

```bash
npx add-skill zach-sndr/agentic-social
```

## Setup

After installation, create your personalized `analyzed.md` file in the skill directory to enable personalization:

1. Copy the `analyzed.md` template from the skill directory
2. Fill in your account details, top tweets, content themes, and goals
3. The skill will use this to personalize all generated content

## Contributing

Contributions welcome! Feel free to:
- Add new social media platform skills
- Improve algorithm optimization
- Add new content frameworks
- Fix bugs and improve documentation

## License

MIT License - see LICENSE file for details

## Algorithm Source

This skill is built on insights from Twitter's open-sourced algorithm:
https://github.com/twitter/the-algorithm
