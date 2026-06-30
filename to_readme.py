import csv

SRC = "movies.csv"

with open(SRC, "r", encoding="utf-8-sig") as f:
    movies = list(csv.DictReader(f))

lines = []
lines.append("# 電影資訊爬蟲\n")
lines.append(f"從 [ssr1.scrape.center](https://ssr1.scrape.center/page/1) 爬取共 **{len(movies)}** 部電影資訊。\n")
lines.append("## 電影列表\n")

lines.append("| # | 海報 | 中文片名 | 英文片名 | 分類 | 地區 | 時長 | 上映日期 | 評分 |")
lines.append("|---|------|---------|---------|------|------|------|---------|------|")

for m in movies:
    poster = f'<img src="{m["cover"]}" width="60">'
    lines.append(
        f'| {m["id"]} '
        f'| {poster} '
        f'| {m["cn_name"]} '
        f'| {m["en_name"]} '
        f'| {m["categories"]} '
        f'| {m["region"]} '
        f'| {m["duration"]} '
        f'| {m["release_date"]} '
        f'| {m["score"]} |'
    )

with open("README.md", "w", encoding="utf-8") as f:
    f.write("\n".join(lines) + "\n")

print(f"README.md 已產生，共 {len(movies)} 筆")
