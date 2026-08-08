# Node.js Google News CLI Application

Design and build a feature-rich, standalone command-line application in Node.js that fetches and displays real-time top headlines and search results from Google News RSS feeds with rich terminal formatting.

## User Review Required

> [!IMPORTANT]
> The application will use modern Node.js (`ES modules`) and minimal dependencies (`commander`, `chalk`, `fast-xml-parser`) for fast execution and clean terminal UI formatting.

## Proposed Changes

### Application Core (`/home/pi-net/Documents/Antigravity/my-first-project`)

#### [NEW] [package.json](file:///home/pi-net/Documents/Antigravity/my-first-project/package.json)
- Define Node module with dependencies (`commander`, `chalk`, `fast-xml-parser`) and `bin` entry (`google-news`).

#### [NEW] [src/api.js](file:///home/pi-net/Documents/Antigravity/my-first-project/src/api.js)
- Fetch Google News RSS feed for:
  - Main top headlines (`https://news.google.com/rss`)
  - Topic categories (World, Business, Technology, Science, Sports, Health, Entertainment)
  - Keyword search (`https://news.google.com/rss/search?q=...`)
- Parse RSS XML into clean JSON structures.

#### [NEW] [src/formatter.js](file:///home/pi-net/Documents/Antigravity/my-first-project/src/formatter.js)
- Beautiful terminal output with color-coded badges, relative timestamps, source publishing names, numbered items, and clickable links.
- Supports JSON output format when `--json` flag is provided.

#### [NEW] [bin/google-news.js](file:///home/pi-net/Documents/Antigravity/my-first-project/bin/google-news.js)
- CLI entry point with command-line options:
  - `-l, --limit <number>` (default: 10)
  - `-t, --topic <category>` (world, tech, business, etc.)
  - `-s, --search <query>` (search news by keyword)
  - `-j, --json` (raw JSON output)
  - `-h, --help`

---

## Verification Plan

### Automated / Manual Verification
1. Install dependencies with `npm install`.
2. Link or run CLI locally: `node bin/google-news.js` to verify top headlines.
3. Test topic flags: `node bin/google-news.js --topic technology --limit 5`.
4. Test keyword search: `node bin/google-news.js --search "AI" --limit 5`.
5. Test JSON output: `node bin/google-news.js --json --limit 2`.
