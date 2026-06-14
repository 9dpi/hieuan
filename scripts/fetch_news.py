import json
import re
import urllib.request
import urllib.error
import xml.etree.ElementTree as ET
from pathlib import Path
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
NEWS_HTML = ROOT / 'news.html'
CACHE_JSON = ROOT / 'scripts' / 'news_cache.json'

FEED_URLS = [
    'https://news.google.com/rss/search?q=%22d%C6%B0%E1%BB%A1ng+l%C3%A3o%22+OR+%22ng%C6%B0%E1%BB%9Di+cao+tu%E1%BB%95i%22+OR+%22ch%C4%83m+s%C3%B3c+ng%C6%B0%E1%BB%9Di+cao+tu%E1%BB%95i%22&hl=vi&gl=VN&ceid=VN:vi',
    'https://news.google.com/rss/search?q=%22%C4%91i%E1%BB%81u+d%C6%B0%E1%BB%A1ng%22+OR+%22s%E1%BB%A9c+kho%E1%BB%83+ng%C6%B0%E1%BB%9Di+cao+tu%E1%BB%95i%22&hl=vi&gl=VN&ceid=VN:vi',
]

KEYWORDS = [
    'dưỡng lão', 'dưỡng lão', 'người cao tuổi', 'chăm sóc người cao tuổi',
    'điều dưỡng', 'sức khỏe người cao tuổi', 'bệnh viện dưỡng lão',
    'viện dưỡng lão', 'bảo vệ sức khỏe người cao tuổi'
]


def fetch_feed(url: str):
    req = urllib.request.Request(url, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36'
    })
    with urllib.request.urlopen(req, timeout=30) as response:
        return response.read().decode('utf-8', errors='ignore')


def clean_text(text: str) -> str:
    text = re.sub(r'<.*?>', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def normalize_title(title: str) -> str:
    title = clean_text(title)
    title = re.sub(r'\s*[-|–]\s*.*$', '', title)
    return title


def is_relevant(item: dict) -> bool:
    text = (item['title'] + ' ' + item['description']).lower()
    return any(k.lower() in text for k in KEYWORDS)


def parse_feed(xml_text: str):
    root = ET.fromstring(xml_text)
    items = []
    for entry in root.findall('.//item'):
        title = normalize_title(entry.findtext('title', default=''))
        link = entry.findtext('link', default='')
        pub_date = entry.findtext('pubDate', default='')
        desc = clean_text(entry.findtext('description', default=''))
        items.append({
            'title': title,
            'link': link,
            'pubDate': pub_date,
            'description': desc[:180],
            'source': 'Google News'
        })
    return items


def build_cards(items):
    cards = []
    for item in items[:6]:
        date = item['pubDate'][:16] if item['pubDate'] else 'Mới nhất'
        cards.append(f'''            <article class="news-card">
                <div class="news-content">
                    <div class="news-date"><i class="far fa-calendar-alt"></i> {date}</div>
                    <h3 class="news-title"><a href="{item['link']}" target="_blank" rel="noopener noreferrer">{item['title']}</a></h3>
                    <p class="news-excerpt">{item['description'] or 'Tin tức liên quan đến chăm sóc, điều dưỡng và sức khỏe người cao tuổi.'}</p>
                    <a href="{item['link']}" target="_blank" rel="noopener noreferrer" class="read-more">Đọc bài gốc <i class="fas fa-arrow-right"></i></a>
                </div>
            </article>''')
    return '\n'.join(cards)


def update_news_html(cards_html: str):
    text = NEWS_HTML.read_text(encoding='utf-8')
    pattern = re.compile(r'<!-- AUTO_NEWS_START -->\s*<!-- AUTO_NEWS_END -->', re.S)
    replacement = '<!-- AUTO_NEWS_START -->\n' + cards_html + '\n            <!-- AUTO_NEWS_END -->'
    new_text, count = pattern.subn(replacement, text, count=1)
    if count == 0:
        raise ValueError('Marker not found in news.html')
    NEWS_HTML.write_text(new_text, encoding='utf-8')


def main():
    all_items = []
    for feed_url in FEED_URLS:
        try:
            xml_text = fetch_feed(feed_url)
            all_items.extend(parse_feed(xml_text))
        except Exception as exc:
            print(f'Fetch failed for {feed_url}: {exc}')

    unique = []
    seen = set()
    for item in all_items:
        key = (item['title'], item['link'])
        if key not in seen:
            seen.add(key)
            if is_relevant(item):
                unique.append(item)

    # fallback to previous cache if nothing relevant was found
    if not unique:
        if CACHE_JSON.exists():
            unique = json.loads(CACHE_JSON.read_text(encoding='utf-8'))
        else:
            unique = []

    CACHE_JSON.write_text(json.dumps(unique[:12], ensure_ascii=False, indent=2), encoding='utf-8')

    if unique:
        update_news_html(build_cards(unique))
    print(f'Updated {len(unique)} news cards from {len(FEED_URLS)} feeds.')


if __name__ == '__main__':
    main()
