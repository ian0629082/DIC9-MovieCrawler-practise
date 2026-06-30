# Vercel 部署說明

這個專案可以直接部署到 Vercel：

1. 到 Vercel 建立新專案，匯入這個資料夾或 GitHub repo。
2. 在 Vercel Project Settings > Environment Variables 新增：
   - `GEMINI_API_KEY`：你的 Gemini API key
   - `GEMINI_MODEL`：`gemini-2.5-flash`
3. 部署完成後：
   - 網站首頁：`/`
   - 電影 API：`/api/movies`
   - 分類 API：`/api/categories`
   - 聊天 API：`/api/chat`

本機測試可以執行：

```bash
python main.py
```

然後打開：

```text
http://127.0.0.1:8000
```
