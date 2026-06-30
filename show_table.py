import sys
import csv
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open('movies.csv', 'r', encoding='utf-8-sig') as f:
    rows = list(csv.DictReader(f))

print(f'共 {len(rows)} 部電影\n')
header = f'{"ID":<3} {"中文名稱":<16} {"英文名稱":<24} {"分類":<14} {"地區":<14} {"時長":<8} {"上映日期":<14} {"評分":<4}'
print(header)
print('-' * 100)
for r in rows:
    print(f'{r["id"]:<3} {r["cn_name"]:<16} {r["en_name"]:<24} {r["categories"]:<14} {r["region"]:<14} {r["duration"]:<8} {r["release_date"]:<14} {r["score"]:<4}')
