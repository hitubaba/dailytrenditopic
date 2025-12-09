#!/usr/bin/env python3
# generate_index.py
# Simple generator using pytrends. If pytrends fails, it will fallback to a small static list
# Usage in Actions: python generate_index.py
import os, sys, html
from datetime import datetime

MAX_ITEMS = int(os.environ.get("MAX_TRENDS", "12"))
REGION = os.environ.get("TRENDS_REGION", "india")  # use 'india' for pytrends pn
TEMPLATE = "templates/index_template.html"
OUTPUT = "index.html"
SITEMAP = "sitemap.xml"

def fetch_trends_pytrends(region):
    try:
        from pytrends.request import TrendReq
    except Exception as e:
        print("pytrends not installed or import failed:", e)
        return None
    try:
        pytrends = TrendReq(hl='en-US', tz=330)
        # trending_searches expects values like 'india', 'united_states'
        df = pytrends.trending_searches(pn=region)
        terms = df[0].tolist()[:MAX_ITEMS]
        return terms
    except Exception as e:
        print("pytrends fetch error:", e)
        return None

def build_cards(terms):
    cards = []
    r = 1
    for t in terms:
        safe = html.escape(t)
        q = html.escape(t.replace(' ', '+'))
        card = f'''
<div class="card">
  <div class="rank">#{r}</div>
  <div class="title"><a href="https://www.google.com/search?q={q}" target="_blank" rel="noopener">{safe}</a></div>
  <div class="source">Search on Google · Explore</div>
</div>'''
        cards.append(card)
        r += 1
    return "\n".join(cards)

def main():
    now = datetime.utcnow()
    today = now.strftime("%Y-%m-%d")
    terms = fetch_trends_pytrends(REGION)
    if not terms:
        print("Using fallback static list.")
        terms = [
            "कुंभ राशिफल",
            "Vande Mataram Parliament",
            "Akhanda 2 release date",
            "Fluminense vs Bahia",
            "76ers vs Lakers",
            "Shubman Gill",
            "England cricket",
            "Manali weather",
            "Amar Ujala",
            "Bulls vs Warriors"
        ][:MAX_ITEMS]

    cards = build_cards(terms)

    if not os.path.exists(TEMPLATE):
        print("Template missing:", TEMPLATE)
        sys.exit(1)

    with open(TEMPLATE, "r", encoding="utf-8") as f:
        tpl = f.read()

    canonical = os.environ.get("CANONICAL_URL", "https://hitubaba.github.io/dailytrenditopic/")
    out = tpl.replace("{{TREND_CARDS}}", cards)
    out = out.replace("{{TODAY_DATE}}", today)
    out = out.replace("{{REGION}}", REGION)
    out = out.replace("{{CANONICAL_URL}}", canonical)
    out = out.replace("{{YEAR}}", str(now.year))

    with open(OUTPUT, "w", encoding="utf-8") as f:
        f.write(out)
    print("Wrote", OUTPUT)

    sitemap = f'''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>{canonical}</loc>
    <lastmod>{today}</lastmod>
    <changefreq>daily</changefreq>
    <priority>0.9</priority>
  </url>
</urlset>
'''
    with open(SITEMAP, "w", encoding="utf-8") as f:
        f.write(sitemap)
    print("Wrote", SITEMAP)

if __name__ == "__main__":
    main()
