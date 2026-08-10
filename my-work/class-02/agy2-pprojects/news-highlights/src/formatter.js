import pc from 'picocolors';

/**
 * Format news items for CLI rendering
 * @param {Array} items 
 * @param {Object} options
 * @param {number} options.limit
 * @param {boolean} options.json
 * @param {string} options.headerTitle
 */
export function formatNewsOutput(items, { limit = 10, json = false, headerTitle = 'Google News Highlights' } = {}) {
  const slicedItems = items.slice(0, limit);

  if (json) {
    return JSON.stringify(slicedItems, null, 2);
  }

  if (slicedItems.length === 0) {
    return pc.yellow('⚠️ No news headlines found.');
  }

  let output = `\n${pc.bgBlue(pc.white(pc.bold(`  📰 ${headerTitle.toUpperCase()}  `)))}\n`;
  output += pc.dim(`Showing top ${slicedItems.length} result(s)\n\n`);

  slicedItems.forEach((item, index) => {
    const num = pc.bold(pc.cyan(`[${index + 1}]`));
    const title = pc.bold(item.title);
    const source = item.source ? pc.magenta(` (${item.source})`) : '';
    const time = item.pubDate ? pc.dim(`• ${item.pubDate}`) : '';
    const link = pc.underline(pc.gray(item.link));

    output += `${num} ${title}${source} ${time}\n`;
    output += `    🔗 ${link}\n\n`;
  });

  return output;
}
