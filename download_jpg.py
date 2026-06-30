import csv
import os
import urllib.request
import urllib3
from io import BytesIO
from PIL import Image

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

SRC = "movies.csv"
DST_DIR = "posters_jpg"
os.makedirs(DST_DIR, exist_ok=True)

with open(SRC, "r", encoding="utf-8-sig") as f:
    movies = list(csv.DictReader(f))

for m in movies:
    path = os.path.join(DST_DIR, f"{m['id']}.jpg")
    if os.path.exists(path):
        print(f"  [{m['id']}] 已存在，跳過")
        continue
    try:
        req = urllib.request.Request(m["cover"], headers={"User-Agent": "Mozilla/5.0"})
        resp = urllib.request.urlopen(req, timeout=10)
        img = Image.open(BytesIO(resp.read()))
        img = img.convert("RGB")
        img.save(path, "JPEG", quality=85)
        print(f"  [{m['id']}] {m['cn_name']} -> {path}")
    except Exception as e:
        print(f"  [{m['id']}] 失敗: {e}")

print(f"\n完成！共 {len(movies)} 張海報已存至 {DST_DIR}/")
