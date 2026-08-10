import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const TEMPLATES_DIR = path.resolve(__dirname, '../templates');

/**
 * Load and render template from templates/ directory
 * @param {string} templateName Relative template path (e.g. 'index.html')
 * @param {Object} data Key-value pairs for placeholders (e.g. { HEADER_TITLE: '...' })
 * @returns {string} Fully rendered HTML string
 */
export function renderTemplate(templateName, data = {}) {
  const filePath = path.join(TEMPLATES_DIR, templateName);
  
  if (!fs.existsSync(filePath)) {
    throw new Error(`Template file not found at: ${filePath}`);
  }

  let html = fs.readFileSync(filePath, 'utf-8');

  // Process {% include 'path/to/component.html' %} directives
  const includeRegex = /\{%\s*include\s+['"]([^'"]+)['"]\s*%\}/g;
  html = html.replace(includeRegex, (match, includePath) => {
    const componentPath = path.join(TEMPLATES_DIR, includePath);
    if (fs.existsSync(componentPath)) {
      return fs.readFileSync(componentPath, 'utf-8');
    }
    return `<!-- Component not found: ${includePath} -->`;
  });

  // Replace variable placeholders {{KEY}}
  Object.keys(data).forEach((key) => {
    const regex = new RegExp(`\\{\\{\\s*${key}\\s*\\}\\}`, 'g');
    html = html.replace(regex, data[key] ?? '');
  });

  // Clear any remaining unreplaced placeholders {{ANYTHING}}
  html = html.replace(/\{\{\s*[A-Z0-9_]+\s*\}\}/g, '');

  return html;
}

/**
 * Render news items array into formatted HTML cards using news_card.html component template
 * @param {Array} newsItems List of article objects
 * @returns {string} Concatenated HTML cards
 */
export function renderNewsCards(newsItems = []) {
  if (!newsItems || newsItems.length === 0) {
    return `
      <div class="empty-state">
        <h3>⚠️ No Headlines Found</h3>
        <p>Try refining your search keyword or selection.</p>
      </div>
    `;
  }

  const cardTemplatePath = path.join(TEMPLATES_DIR, 'components/news_card.html');
  let cardTemplate = '<div class="news-card"><h3>{{TITLE}}</h3></div>';

  if (fs.existsSync(cardTemplatePath)) {
    cardTemplate = fs.readFileSync(cardTemplatePath, 'utf-8');
  }

  return newsItems.map((item) => {
    let card = cardTemplate;
    const replacements = {
      TITLE: escapeHtml(item.title || 'Untitled Story'),
      SOURCE: escapeHtml(item.source || 'Google News'),
      LINK: escapeHtml(item.link || '#'),
      PUB_DATE: item.pubDate || 'Recently',
      ISO_DATE: item.isoDate || new Date().toISOString()
    };

    Object.keys(replacements).forEach((key) => {
      const regex = new RegExp(`\\{\\{\\s*${key}\\s*\\}\\}`, 'g');
      card = card.replace(regex, replacements[key]);
    });

    return card;
  }).join('\n');
}

function escapeHtml(str) {
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;');
}
