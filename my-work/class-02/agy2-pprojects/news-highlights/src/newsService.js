import Parser from 'rss-parser';

const parser = new Parser();

export const TOPICS = {
  WORLD: 'WORLD',
  NATION: 'NATION',
  BUSINESS: 'BUSINESS',
  TECHNOLOGY: 'TECHNOLOGY',
  ENTERTAINMENT: 'ENTERTAINMENT',
  SPORTS: 'SPORTS',
  SCIENCE: 'SCIENCE',
  HEALTH: 'HEALTH',
};

/**
 * Fetch news items from Google News RSS feed
 * @param {Object} options
 * @param {'top'|'topic'|'search'} options.type
 * @param {string} [options.topic]
 * @param {string} [options.query]
 * @param {string} [options.hl] - Language (default: 'en-US')
 * @param {string} [options.gl] - Country (default: 'US')
 * @returns {Promise<Array>}
 */
export async function fetchNews({ type = 'top', topic, query, hl = 'en-US', gl = 'US' } = {}) {
  const ceid = `${gl}:${hl.split('-')[0] || 'en'}`;
  let feedUrl = `https://news.google.com/rss?hl=${hl}&gl=${gl}&ceid=${ceid}`;

  if (type === 'topic' && topic) {
    const formattedTopic = topic.toUpperCase();
    feedUrl = `https://news.google.com/rss/headlines/section/topic/${formattedTopic}?hl=${hl}&gl=${gl}&ceid=${ceid}`;
  } else if (type === 'search' && query) {
    feedUrl = `https://news.google.com/rss/search?q=${encodeURIComponent(query)}&hl=${hl}&gl=${gl}&ceid=${ceid}`;
  }

  try {
    const feed = await parser.parseURL(feedUrl);
    
    return (feed.items || []).map((item) => {
      // Google News items often format title as "Headline Title - Source Name"
      let headline = item.title || '';
      let sourceName = item.source?._ || item.source || '';
      
      if (!sourceName && headline.includes(' - ')) {
        const parts = headline.split(' - ');
        sourceName = parts.pop().trim();
        headline = parts.join(' - ').trim();
      }

      return {
        title: headline,
        source: sourceName,
        link: item.link || '',
        pubDate: item.pubDate ? new Date(item.pubDate).toLocaleString() : 'N/A',
        isoDate: item.isoDate || item.pubDate,
        guid: item.guid,
      };
    });
  } catch (error) {
    throw new Error(`Failed to fetch Google News RSS feed from ${feedUrl}: ${error.message}`);
  }
}
