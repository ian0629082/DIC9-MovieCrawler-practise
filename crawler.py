import requests
from bs4 import BeautifulSoup
import csv
import re
import time

BASE_URL = "https://ssr1.scrape.center/page/{}"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}
OUTPUT = "movies.csv"


def parse_movie(card):
    a_tag = card.select_one("a[href^='/detail/']")
    movie_id = int(re.search(r"/detail/(\d+)", a_tag["href"]).group(1))

    h2 = card.select_one("h2.m-b-sm")
    title_text = h2.get_text(strip=True)
    cn_name = en_name = ""
    if " - " in title_text:
        cn_name, en_name = title_text.split(" - ", 1)
    else:
        cn_name = title_text

    cover = card.select_one("img.cover")["src"]

    categories = [
        span.get_text(strip=True)
        for span in card.select("button.category span")
    ]

    info_spans = card.select(".m-v-sm.info span")
    region = info_spans[0].get_text(strip=True) if len(info_spans) > 0 else ""
    duration = info_spans[2].get_text(strip=True) if len(info_spans) > 2 else ""

    release = ""
    release_spans = card.select(".m-v-sm.info")
    if len(release_spans) > 1:
        release_text = release_spans[1].get_text(strip=True)
        release = release_text.replace("上映", "").strip()

    score_text = card.select_one("p.score")
    score = score_text.get_text(strip=True) if score_text else ""

    return {
        "id": movie_id,
        "cn_name": cn_name,
        "en_name": en_name,
        "cover": cover,
        "categories": "、".join(categories),
        "region": region,
        "duration": duration,
        "release_date": release,
        "score": score,
    }


def fetch_page(page_num):
    url = BASE_URL.format(page_num)
    resp = requests.get(url, headers=HEADERS, timeout=15, verify=False)
    resp.encoding = "utf-8"
    resp.raise_for_status()
    return resp.text


def parse_page(html):
    soup = BeautifulSoup(html, "html.parser")
    cards = soup.select("div.el-card.item")
    return [parse_movie(card) for card in cards]


def main():
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    all_movies = []
    for page in range(1, 12):
        print(f"Fetching page {page}...")
        try:
            html = fetch_page(page)
        except Exception as e:
            print(f"  Failed: {e}")
            break
        movies = parse_page(html)
        if not movies:
            print(f"  No movies found, stopping")
            break
        all_movies.extend(movies)
        print(f"  Got {len(movies)} movies")
        time.sleep(1)

    with open(OUTPUT, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "id", "cn_name", "en_name", "cover", "categories",
            "region", "duration", "release_date", "score"
        ])
        writer.writeheader()
        writer.writerows(all_movies)

    print(f"\nDone! {len(all_movies)} movies saved to {OUTPUT}")


if __name__ == "__main__":
    main()
