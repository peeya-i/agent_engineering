#!/usr/bin/env node

import { Command } from 'commander';
import open from 'open';
import pc from 'picocolors';
import { fetchNews, TOPICS } from '../src/newsService.js';
import { formatNewsOutput } from '../src/formatter.js';

const program = new Command();

program
  .name('gnews')
  .description('CLI application to get live headlines, topic feeds, and search news from Google News')
  .version('1.0.0');

// Shared CLI flags
const addSharedOptions = (cmd) => {
  return cmd
    .option('-l, --limit <number>', 'Number of news stories to display', (val) => parseInt(val, 10), 10)
    .option('-j, --json', 'Output results in JSON format', false)
    .option('-o, --open <index>', 'Open news article link at specified index (1-indexed) in default browser')
    .option('--hl <language>', 'Language locale', 'en-US')
    .option('--gl <country>', 'Country region', 'US');
};

async function handleNewsExecution(fetchOptions, formatOptions, openIndex) {
  try {
    const items = await fetchNews(fetchOptions);

    if (openIndex) {
      const idx = parseInt(openIndex, 10) - 1;
      if (items[idx] && items[idx].link) {
        console.log(pc.green(`🚀 Opening article #${openIndex} in browser: ${items[idx].title}`));
        await open(items[idx].link);
      } else {
        console.error(pc.red(`❌ Invalid index ${openIndex}. Available range: 1 to ${items.length}`));
      }
    }

    const output = formatNewsOutput(items, formatOptions);
    console.log(output);
  } catch (error) {
    console.error(pc.red(`❌ Error: ${error.message}`));
    process.exit(1);
  }
}

// Command: Top headlines (default)
addSharedOptions(
  program
    .command('top', { isDefault: true })
    .description('Fetch top breaking news headlines')
    .action(async (options) => {
      await handleNewsExecution(
        { type: 'top', hl: options.hl, gl: options.gl },
        { limit: options.limit, json: options.json, headerTitle: 'Top Google News Headlines' },
        options.open
      );
    })
);

// Command: Topic headlines
addSharedOptions(
  program
    .command('topic <category>')
    .description(`Fetch news by category (${Object.keys(TOPICS).join(', ')})`)
    .action(async (category, options) => {
      const validTopics = Object.keys(TOPICS);
      const upperCat = category.toUpperCase();

      if (!validTopics.includes(upperCat)) {
        console.error(pc.red(`❌ Unknown category: "${category}". Valid options: ${validTopics.join(', ')}`));
        process.exit(1);
      }

      await handleNewsExecution(
        { type: 'topic', topic: upperCat, hl: options.hl, gl: options.gl },
        { limit: options.limit, json: options.json, headerTitle: `${upperCat} News` },
        options.open
      );
    })
);

// Command: Search news
addSharedOptions(
  program
    .command('search <query...>')
    .description('Search Google News for specific topics or keywords')
    .action(async (queryWords, options) => {
      const query = queryWords.join(' ');
      await handleNewsExecution(
        { type: 'search', query, hl: options.hl, gl: options.gl },
        { limit: options.limit, json: options.json, headerTitle: `Search Results: "${query}"` },
        options.open
      );
    })
);

program.parse(process.argv);
