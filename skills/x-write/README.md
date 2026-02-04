# x-write

Viral-optimized X (Twitter) content creation built on X's open-sourced algorithm.

**Algorithm source:** https://github.com/twitter/the-algorithm

## Quick Start

```
/skills x-write write "your topic"
/skills x-write strategy "describe your idea"
/skills x-write reply "@account tweet-content"
/skills x-write analyze-tweet "tweet text"
```

---

## CRITICAL: Create Your Profile Analysis (analyzed.md)

Before using the skill, you must create a personalized `analyzed.md` file in the skill directory.

### Step 1: Copy this prompt and template

```
X Account: zach_sndr
Analyze and evaluate my complete X profile and fill these details. Ensure your output is a markdown file for easy copying. Pull my most popular tweets, and scan my uploaded files for last 28 days data.

Questions:

# User Analysis for x-write

> This file helps the x-write skill personalize content to your account.
> Fill out each section below.

---

## Account Basics

| Field | Your Answer |
|-------|-------------|
| **Handle** | @your_handle |
| **Followers** | ___ |
| **Verification** | Blue / Gold / Gray / Legacy / None |
| **Bio** | Your short bio or one-liner |

---

## What Works for You

### Your Top 5 Tweets

| # | Tweet (first 100 chars) | Replies | RTs | Likes |
|---|-------------------------|---------|-----|-------|
| 1 | | | | |
| 2 | | | | |
| 3 | | | | |
| 4 | | | | |
| 5 | | | | |

### Best Performing Content Type

Pick ONE that gets your best engagement:
- [ ] Opinion/hot takes
- [ ] How-to/educational
- [ ] Personal stories
- [ ] Industry insights
- [ ] News/commentary
- [ ] Threads
- [ ] Quotes/RTs with commentary
- [ ] Other: _____________

### Best Format

Pick ONE:
- [ ] Single tweets
- [ ] Threads
- [ ] Images/GIFs
- [ ] Videos
- [ ] Replies to others

### Worst Performing

What content types get your WORST engagement?
>

---

## Your Voice & Topics

### Content Themes

List your top 5 topics:
1. ___________________
2. ___________________
3. ___________________
4. ___________________
5. ___________________

### Topics You WILL Cover

_______________________________________________________________

### Topics You AVOID

_______________________________________________________________

### Tone

Pick ONE:
- [ ] Professional/formal
- [ ] Casual/friendly
- [ ] Controversial/opinionated
- [ ] Educational
- [ ] Humorous
- [ ] Inspirational
- [ ] Other: _____________

### Length Preference

Pick ONE:
- [ ] Short & punchy (under 200 chars)
- [ ] Medium (200-240 chars)
- [ ] Max out (240-280 chars)

---

## Your Goals

**Main goals** (check all that apply):
- [ ] Grow followers
- [ ] Network/connections
- [ ] Drive traffic
- [ ] Build authority
- [ ] Get clients/sales
- [ ] Share knowledge

**Target audience**:
_______________________________________________________________

---

## Posting Patterns

**Best days**: _________________________________________

**Best times** (your timezone): _________________________________

**Typical posts per day**: _______

---

## Quick Context (Optional Notes)

Any additional context about your account, what's working, or what you're trying to achieve:
```

### Step 2: Gather Your Data (Choose One Option)

**Option A: Use Grok.com (Easiest - No CSVs Needed)**

Grok.com can directly access your X posts and profile, so you don't need CSV files. Just paste the prompt and Grok will pull your data automatically.

**Option B: Use Any AI Agent (Requires CSV Export)**

If you prefer using another AI agent, export your X data first:

#### Download Analytics CSV

1. Open X and go to **More > Premium > Analytics**
2. In the top right corner, click the **Download** button
3. Set the **Date range** to **1 year** (or maximum available)
4. Click **Download** to save the CSV file
5. Note the file location (e.g., `Downloads/analytics_export.csv`)

#### Download Content CSV

1. In Analytics, switch to the **Content** tab
2. In the top right corner, click the **Download** button
3. Set the **Date range** to **1 year** (or maximum available)
4. Click **Download** to save the CSV file
5. Note the file location (e.g., `Downloads/content_export.csv`)

### Step 3: Generate Your Analysis

**If using Grok.com (Option A):**

1. Visit [grok.com](https://grok.com)
2. Paste the prompt from Step 1 (replace `zach_sndr` with your handle)
3. Grok will automatically pull your X posts and profile data
4. Copy the filled template output

**If using another AI agent (Option B):**

1. Open your preferred AI agent (ChatGPT, Claude, etc.)
2. Paste the prompt from Step 1 (replace `zach_sndr` with your handle)
3. **Upload both CSV files** from Step 2:
   - `analytics_export.csv` (or similar name)
   - `content_export.csv` (or similar name)
4. Copy the filled template output

### Step 4: Save to analyzed.md

1. Create or replace `analyzed.md` in the skill directory with the AI's output
2. The skill will now use this to personalize all generated content

---

## Algorithm Weights

| Interaction | Points | Multiplier |
|-------------|--------|------------|
| Reply | 20.0 | 2x baseline (highest) |
| Retweet | 15.0 | 1.5x baseline |
| Quote Tweet | 15.0 | 1.5x baseline |
| Like | 10.0 | baseline |

**Key principles:**
- OON (Out-of-Network) discovery = 90% weight
- Follower engagement = 10% weight
- First 6 hours = 91% score potential (critical window)
- 48-hour exponential decay half-life

## Recommended Models

This skill works best with models that have a more natural, human writing style:

| Model | Why |
|-------|-----|
| **gemini-3-pro** | Natural conversational tone, less formal than Claude |
| **grok-4.1-thinking** | Best human-like style, understands internet culture |

> **Why not Claude?** Claude models tend to be more formal and structured, which can make tweets feel robotic. For viral social content, you want writing that sounds like a real person, not an AI assistant.
