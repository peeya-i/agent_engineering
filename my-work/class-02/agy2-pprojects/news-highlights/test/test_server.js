import fs from 'fs';
import path from 'path';
import http from 'http';
import assert from 'assert';
import { fileURLToPath } from 'url';
import { renderTemplate, renderNewsCards } from '../src/templateRenderer.js';
import { createServer } from '../server.js';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const ROOT = path.resolve(__dirname, '..');

console.log('🧪 Starting news-highlights template & server test suite...\n');

// 1. Verify Templates Directory & Component Files
const templatesDir = path.join(ROOT, 'templates');
assert.strictEqual(fs.existsSync(templatesDir), true, 'Templates directory must exist');

const requiredTemplates = [
  'index.html',
  'components/header.html',
  'components/news_card.html',
  'components/footer.html'
];

requiredTemplates.forEach((file) => {
  const fullPath = path.join(templatesDir, file);
  assert.strictEqual(fs.existsSync(fullPath), true, `Template file missing: ${file}`);
  console.log(`  ✓ Template file verified: templates/${file}`);
});

// 2. Verify Template Rendering Engine
const renderedHtml = renderTemplate('index.html', {
  PAGE_TITLE: 'Unit Test Dashboard',
  HEADER_TITLE: 'Test Header',
  ARTICLE_COUNT: 2,
  NEWS_CARDS: renderNewsCards([
    { title: 'Test Article 1', source: 'Test Source', link: 'https://example.com/1', pubDate: 'Today' },
    { title: 'Test Article 2', source: 'Test Source', link: 'https://example.com/2', pubDate: 'Today' }
  ])
});

assert.ok(renderedHtml.includes('Unit Test Dashboard'), 'Rendered HTML should include page title');
assert.ok(renderedHtml.includes('Test Article 1'), 'Rendered HTML should include article 1 title');
assert.ok(renderedHtml.includes('Test Article 2'), 'Rendered HTML should include article 2 title');
assert.ok(renderedHtml.includes('Google News Highlights'), 'Rendered HTML should include header component content');
console.log('\n  ✓ Template renderer tag parsing & component include verified!');

// 3. Verify Server Endpoints
const PORT = 3999;
const appServer = createServer();

appServer.listen(PORT, async () => {
  console.log(`\n  🚀 Test server listening on port ${PORT}...`);

  try {
    // Health Check Endpoint
    const health = await fetchJson(`http://localhost:${PORT}/health`);
    assert.strictEqual(health.status, 'healthy');
    console.log('  ✓ GET /health -> 200 OK');

    // Homepage HTML Endpoint
    const homeHtml = await fetchText(`http://localhost:${PORT}/`);
    assert.ok(homeHtml.includes('<!DOCTYPE html>'));
    assert.ok(homeHtml.includes('Google News Highlights'));
    console.log('  ✓ GET / -> 200 OK (Rendered index.html template)');

    // Topic Feed HTML Endpoint
    const topicHtml = await fetchText(`http://localhost:${PORT}/topic/technology`);
    assert.ok(topicHtml.includes('TECHNOLOGY News Feed'));
    console.log('  ✓ GET /topic/technology -> 200 OK (Rendered topic page)');

    // JSON API Endpoint
    const apiRes = await fetchJson(`http://localhost:${PORT}/api/news?type=top`);
    assert.strictEqual(typeof apiRes.count, 'number');
    assert.ok(Array.isArray(apiRes.items));
    console.log(`  ✓ GET /api/news -> 200 OK (Fetched ${apiRes.count} items)`);

    console.log('\n🎉 ALL TESTS PASSED SUCCESSFULLY!\n');
  } catch (err) {
    console.error('❌ Test execution failed:', err);
    process.exitCode = 1;
  } finally {
    appServer.close();
  }
});

function fetchText(urlStr) {
  return new Promise((resolve, reject) => {
    http.get(urlStr, (res) => {
      let body = '';
      res.on('data', (chunk) => (body += chunk));
      res.on('end', () => resolve(body));
    }).on('error', reject);
  });
}

function fetchJson(urlStr) {
  return fetchText(urlStr).then(JSON.parse);
}
