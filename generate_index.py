#!/usr/bin/env python3
import os, sys, html, json
from datetime import datetime

MAX_ITEMS = int(os.environ.get("MAX_TRENDS", "20"))
REGION = os.environ.get("TRENDS_REGION", "india")  
TEMPLATE = "templates/index_template.html"
OUTPUT = "index.html"
SITEMAP = "sitemap.xml"


# ---------------------------
# 1) Trends fetch function
# ---------------------------
def fetch_trends_pytrends(region):
    try:
        from pytrends.request import TrendReq
        pytrends = TrendReq(hl='en-US', tz=330)
        df = pytrends.trending_searches(pn=region)
        return df[0].tolist()[:MAX_ITEMS]
    except:
        return None


# ---------------------------
# 2) HTML CARD builder
# ---------------------------
def build_cards(terms):
    cards = []
    for i, t in enumerate(terms, start=1):
        safe = html.escape(t)
        q = html.escape(t.replace(' ', '+'))
        card = f"""
<div class="card">
  <div class="rank">#{i}</div>
  <div class="title"><a href="https://www.google.com/search?q={q}" target="_blank">{safe}</a></div>
  <div class="desc">Trending topic · Explore full story on Google</div>
</div>
"""
        cards.append(card)
    return "\n".join(cards)


# ---------------------------
# 3) SEO JSON-LD (ItemList)
# ---------------------------
def build_itemlist_json(terms):
    items = []
    for i, t in enumerate(terms, start=1):
        item = {
            "@type": "ListItem",
            "position": i,
            "name": t,
            "url": f"https://www.google.com/search?q={t.replace(' ', '+')}"
        }
        items.append(json.dumps(item))
    return ",\n      ".join(items)


# ---------------------------
# 4) Main build process
# ---------------------------
def main():

    now = datetime.utcnow()
    today = now.strftime("%Y-%m-%d")

    terms = fetch_trends_pytrends(REGION)
    if not terms:
        terms = [
            "कुंभ राशिफल",
            "Vande Mataram Parliament",
            "Akhanda 2 release date",
            "Fluminense vs Bahia",
            "76ers vs Lakers",
        ][:MAX_ITEMS]

    if not os.path.exists(TEMPLATE):
        print("Template missing:", TEMPLATE)
        sys.exit(1)

    with open(TEMPLATE, "r", encoding="utf-8") as f:
        tpl = f.read()

    # Build outputs
    cards_html = build_cards(terms)
    json_list = build_itemlist_json(terms)

    canonical = os.environ.get("CANONICAL_URL", "https://hitubaba.github.io/dailytrenditopic/")

    out = tpl.replace("{{TREND_CARDS}}", cards_html)
    out = out.replace("{{TREND_LIST_JSON}}", json_list)
    out = out.replace("{{TODAY_DATE}}", today)
    out = out.replace("{{REGION}}", REGION)
    out = out.replace("{{CANONICAL_URL}}", canonical)
    out = out.replace("{{YEAR}}", str(now.year))

    with open(OUTPUT, "w", encoding="utf-8") as f:
        f.write(out)

    # Sitemap generate
    sitemap = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>{canonical}</loc>
    <lastmod>{today}</lastmod>
    <changefreq>daily</changefreq>
    <priority>1.0</priority>
  </url>
</urlset>
"""
    with open(SITEMAP, "w", encoding="utf-8") as f:
        f.write(sitemap)

    print("DONE: index.html + sitemap.xml updated!")


if __name__ == "__main__":
    main()
