
#!/usr/bin/env python3
# generate_index.py
# Requires: pytrends
# pip install pytrends

import os
import sys
from datetime import datetime
from pytrends.request import TrendReq
import html
import json

# Config
REGION = os.environ.get("TRENDS_REGION", "IN")  # change to 'US' or 'GLOBAL' as needed
TEMPLATE_PATH = "templates/index_template.html"
OUTPUT_PATH = "index.html"
SITEMAP_PATH = "sitemap.xml"
MAX_ITEMS = int(os.environ.get("MAX_TRENDS", "12"))

def fetch_trends(region):
    pytrends = TrendReq(hl='en-US', tz=330)
    try:
        # top charts / daily search trends
        # pytrends has trending_searches method (real-time for region)
        df = pytrends.trending_searches(pn=region.lower())  # e.g., 'india' works best with 'india' but we'll try
        # if region is 'IN' map to 'india'
    except Exception as e:
        # fallback to trending_searches without region
        df = pytrends.trending_searches(pn='india')
    terms = df[0].tolist()[:MAX_ITEMS]
    return terms

def build_cards(terms):
    cards = []
    rank = 1
    for t in terms:
        safe_t = html.escape(t)
        card_html = f"""
<div class="card">
  <div class="rank">#{rank}</div>
  <div class="title"><a href="https://www.google.com/search?q={html.escape(t.replace(' ', '+'))}" target="_blank" rel="noopener">{safe_t}</a></div>
  <div class="source">Search on Google · Explore for more</div>
</div>
"""
        cards.append(card_html)
        rank += 1
    return "\n".join(cards)

def main():
    now = datetime.utcnow()
    today_iso = now.strftime("%Y-%m-%d")
    print("Fetching trends for region:", REGION)
    try:
        terms = fetch_trends(REGION)
    except Exception as e:
        print("Error fetching trends:", e)
        terms = ["Trending fetch error — try again later"]

    cards_html = build_cards(terms)

    # read template
    with open(TEMPLATE_PATH, "r", encoding="utf-8") as f:
        template = f.read()

    canonical = os.environ.get("CANONICAL_URL", "https://your-username.github.io/your-repo/")
    out_html = template.replace("{{TREND_CARDS}}", cards_html)
    out_html = out_html.replace("{{TODAY_DATE}}", today_iso)
    out_html = out_html.replace("{{REGION}}", REGION)
    out_html = out_html.replace("{{CANONICAL_URL}}", canonical)
    out_html = out_html.replace("{{YEAR}}", str(datetime.now().year))

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(out_html)
    print("Wrote", OUTPUT_PATH)

    # sitemap
    sitemap = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>{canonical}</loc>
    <lastmod>{today_iso}</lastmod>
    <changefreq>daily</changefreq>
    <priority>0.9</priority>
  </url>
</urlset>
"""
    with open(SITEMAP_PATH, "w", encoding="utf-8") as f:
        f.write(sitemap)
    print("Wrote", SITEMAP_PATH)

if __name__ == "__main__":
    main()
