# dailytrenditopic — Auto-updating daily trending topics (GitHub Pages)

यह project GitHub Pages के लिए तैयार है। यह GitHub Actions का उपयोग करके रोज़ाना Google Trends से शीर्ष खोजशब्द निकालकर `index.html` अपडेट करेगा।

## Quick setup (for hitubaba)

1. नया repo बनाओ: `dailytrenditopic` (Public recommended)
2. इस ZIP के सारे फाइलें अपने repo में डाल दो (same folders)
3. Repo → Settings → Pages में branch = `main`, folder = `/` select करो।
4. Repo → Settings → Secrets → Actions → Add `CANONICAL_URL` with value:
   `https://hitubaba.github.io/dailytrenditopic/`
5. Actions → open `Daily Update Trending Topics` workflow → Run workflow (या wait for schedule)
6. First run will create `index.html` and `sitemap.xml`. If pytrends fails, generator uses a fallback static list.

## Notes
- If you want Hindi-only output or different region, change `TRENDS_REGION` in workflow (e.g., `united_states`, `brazil` etc.)
- If Actions fails, open the failing run log and paste the error here — I will help fix it.
