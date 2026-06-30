# DIC9 MovieCrawler Practise

這是一個電影資料爬蟲與展示練習專案，資料來源為 [ssr1.scrape.center](https://ssr1.scrape.center/page/1)。專案已整理成可部署到 Vercel 的網站，包含靜態電影列表、分類篩選、搜尋，以及 Gemini 電影聊天助理。

## 專案功能

- 爬取並整理 100 筆電影資料
- 產生靜態網站 `index.html`
- 提供 FastAPI API：
  - `/api/movies`
  - `/api/movies/{movie_id}`
  - `/api/categories`
  - `/api/chat`
- 使用 Gemini API 回答電影相關問題
- 支援部署到 Vercel

## 專案結構

```text
.
├── api/
│   └── index.py              # FastAPI / Vercel API 入口
├── posters/                  # GitHub README 可顯示的電影海報 PNG
├── index.html                # 網站首頁
├── movies.json               # 電影資料 JSON
├── movies.csv                # 電影資料 CSV
├── requirements.txt          # Python 套件
├── vercel.json               # Vercel 路由設定
├── VERCEL_DEPLOY.md          # Vercel 部署說明
└── .env.example              # 環境變數範例
```

## 環境變數

本機請建立 `.env`：

```env
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-2.5-flash
```

`.env` 已加入 `.gitignore`，不會被推送到 GitHub。部署 Vercel 時，請在 Vercel 的 Environment Variables 設定同樣的變數。

## 本機執行

```bash
pip install -r requirements.txt
python main.py
```

啟動後開啟：

```text
http://127.0.0.1:8000
```

## Vercel 部署

1. 將專案推送到 GitHub。
2. 到 Vercel 匯入 GitHub repo。
3. Application Preset 可選 `FastAPI`；若沒有此選項，選 `Other`。
4. Environment Variables 設定：

```text
GEMINI_API_KEY = your_gemini_api_key_here
GEMINI_MODEL = gemini-2.5-flash
```

5. 按下 `Deploy`。

## 電影列表預覽

以下僅列出前 10 筆電影資料。完整資料請參考 `movies.json` 或網站頁面。

| # | 海報 | 中文片名 | 英文片名 | 類型 | 地區 | 片長 | 上映日期 | 評分 |
|---|------|----------|----------|------|------|------|----------|------|
| 1 | <img src="posters/1.png" width="70" alt="霸王别姬"> | 霸王别姬 | Farewell My Concubine | 剧情、爱情 | 中国内地、中国香港 | 171 分钟 | 1993-07-26 | 9.5 |
| 2 | <img src="posters/2.png" width="70" alt="这个杀手不太冷"> | 这个杀手不太冷 | Léon | 剧情、动作、犯罪 | 法国 | 110 分钟 | 1994-09-14 | 9.5 |
| 3 | <img src="posters/3.png" width="70" alt="肖申克的救赎"> | 肖申克的救赎 | The Shawshank Redemption | 剧情、犯罪 | 美国 | 142 分钟 | 1994-09-10 | 9.5 |
| 4 | <img src="posters/4.png" width="70" alt="泰坦尼克号"> | 泰坦尼克号 | Titanic | 剧情、爱情、灾难 | 美国 | 194 分钟 | 1998-04-03 | 9.5 |
| 5 | <img src="posters/5.png" width="70" alt="罗马假日"> | 罗马假日 | Roman Holiday | 剧情、喜剧、爱情 | 美国 | 118 分钟 | 1953-08-20 | 9.5 |
| 6 | <img src="posters/6.png" width="70" alt="唐伯虎点秋香"> | 唐伯虎点秋香 | Flirting Scholar | 喜剧、爱情、古装 | 中国香港 | 102 分钟 | 1993-07-01 | 9.5 |
| 7 | <img src="posters/7.png" width="70" alt="乱世佳人"> | 乱世佳人 | Gone with the Wind | 剧情、爱情、历史、战争 | 美国 | 238 分钟 | 1939-12-15 | 9.5 |
| 8 | <img src="posters/8.png" width="70" alt="喜剧之王"> | 喜剧之王 | The King of Comedy | 剧情、喜剧、爱情 | 中国香港 | 85 分钟 | 1999-02-13 | 9.5 |
| 9 | <img src="posters/9.png" width="70" alt="楚门的世界"> | 楚门的世界 | The Truman Show | 剧情、科幻 | 美国 | 103 分钟 |  | 9.0 |
| 10 | <img src="posters/10.png" width="70" alt="狮子王"> | 狮子王 | The Lion King | 动画、歌舞、冒险 | 美国 | 89 分钟 | 1995-07-15 | 9.0 |

## 注意事項

- README 的圖片使用相對路徑 `posters/*.png`，推送到 GitHub 後可以正常顯示。
- API key 請只放在 `.env` 或 Vercel Environment Variables，不要寫進程式碼或 README。
