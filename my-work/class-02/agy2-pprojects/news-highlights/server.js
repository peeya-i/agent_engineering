import http from 'http';
import url from 'url';
import { fetchNews, TOPICS } from './src/newsService.js';
import { renderTemplate, renderNewsCards } from './src/templateRenderer.js';

const PORT = process.env.PORT || 3000;

export function createServer() {
  return http.createServer(async (req, res) => {
    const parsedUrl = url.parse(req.url, true);
    const pathname = parsedUrl.pathname;
    const query = parsedUrl.query;

    try {
      // Health Check Endpoint
      if (pathname === '/health') {
        res.writeHead(200, { 'Content-Type': 'application/json' });
        return res.end(JSON.stringify({ status: 'healthy', service: 'Google News Highlights' }));
      }

      // JSON API Endpoint
      if (pathname === '/api/news') {
        const type = query.type || 'top';
        const topic = query.topic;
        const q = query.q;
        const items = await fetchNews({ type, topic, query: q });
        
        res.writeHead(200, { 'Content-Type': 'application/json' });
        return res.end(JSON.stringify({ count: items.length, items }));
      }

      // Web Dashboard Routes: Top Headlines
      if (pathname === '/' || pathname === '/index.html') {
        const items = await fetchNews({ type: 'top' });
        const cardsHtml = renderNewsCards(items);

        const html = renderTemplate('index.html', {
          PAGE_TITLE: 'Top Headlines',
          HEADER_TITLE: '🔥 Top Google News Headlines',
          ARTICLE_COUNT: items.length,
          NEWS_CARDS: cardsHtml,
          ACTIVE_TOP: 'active',
          SEARCH_QUERY: ''
        });

        res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
        return res.end(html);
      }

      // Topic Routes e.g. /topic/technology or /topic/world
      if (pathname.startsWith('/topic/')) {
        const catParam = pathname.replace('/topic/', '').trim().toUpperCase();
        const topicKey = TOPICS[catParam] ? catParam : 'TECHNOLOGY';
        
        const items = await fetchNews({ type: 'topic', topic: topicKey });
        const cardsHtml = renderNewsCards(items);

        const activeKey = `ACTIVE_${topicKey}`;
        const data = {
          PAGE_TITLE: `${topicKey} News`,
          HEADER_TITLE: `📰 ${topicKey} News Feed`,
          ARTICLE_COUNT: items.length,
          NEWS_CARDS: cardsHtml,
          SEARCH_QUERY: ''
        };
        data[activeKey] = 'active';

        const html = renderTemplate('index.html', data);
        res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
        return res.end(html);
      }

      // Search Route e.g. /search?q=Kubernetes
      if (pathname === '/search') {
        const searchQuery = (query.q || '').trim();
        const items = searchQuery 
          ? await fetchNews({ type: 'search', query: searchQuery })
          : await fetchNews({ type: 'top' });

        const cardsHtml = renderNewsCards(items);

        const html = renderTemplate('index.html', {
          PAGE_TITLE: `Search: "${searchQuery}"`,
          HEADER_TITLE: `🔍 Search Results for "${searchQuery}"`,
          ARTICLE_COUNT: items.length,
          NEWS_CARDS: cardsHtml,
          SEARCH_QUERY: searchQuery
        });

        res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
        return res.end(html);
      }

      // 404 Route
      res.writeHead(404, { 'Content-Type': 'text/html; charset=utf-8' });
      res.end('<h1>404 Page Not Found</h1><p><a href="/">Return to Google News Highlights</a></p>');

    } catch (error) {
      console.error('Server error:', error);
      res.writeHead(500, { 'Content-Type': 'text/html; charset=utf-8' });
      res.end(`<h1>500 Internal Server Error</h1><p>${error.message}</p>`);
    }
  });
}

export const server = createServer();

// Run server directly if invoked via CLI
if (process.argv[1] && process.argv[1].endsWith('server.js')) {
  const appServer = createServer();
  appServer.listen(PORT, () => {
    console.log(`🌐 Google News Highlights Web Server running at http://localhost:${PORT}`);
  });
}
