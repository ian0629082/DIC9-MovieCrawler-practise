import json
import os
import re
from pathlib import Path

import google.generativeai as genai
from dotenv import load_dotenv
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel


BASE_DIR = Path(__file__).resolve().parent.parent

# Local development reads .env. On Vercel, set these in Project Settings > Environment Variables.
load_dotenv(BASE_DIR / ".env")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash").strip()

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

app = FastAPI(title="Movie Chatbot API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    message: str


def load_movies() -> list[dict]:
    movies_path = BASE_DIR / "movies.json"
    with movies_path.open("r", encoding="utf-8") as f:
        return json.load(f)


movies = load_movies()

movie_context = json.dumps(
    [
        {
            "id": m["id"],
            "cn_name": m["cn_name"],
            "en_name": m["en_name"],
            "categories": m["categories"],
            "region": m["region"],
            "duration": m["duration"],
            "release_date": m["release_date"],
            "score": m["score"],
        }
        for m in movies
    ],
    ensure_ascii=False,
)


def normalize_id(value):
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def search_movies(keyword: str) -> list[dict]:
    kw = keyword.lower().strip()
    if not kw:
        return []
    return [
        movie
        for movie in movies
        if kw in movie["cn_name"].lower() or kw in movie["en_name"].lower()
    ]


def get_movie_by_id(movie_id: int) -> dict | None:
    for movie in movies:
        if normalize_id(movie.get("id")) == movie_id:
            return movie
    return None


def format_movie(movie: dict) -> str:
    return (
        f"{movie['cn_name']} ({movie['en_name']})\n"
        f"類型：{movie['categories']}\n"
        f"地區：{movie['region']}\n"
        f"片長：{movie['duration']}\n"
        f"上映：{movie['release_date'] or '未提供'}\n"
        f"評分：{movie['score']}"
    )


def fallback_reply(text: str) -> str:
    lowered = text.strip().lower()
    if lowered in {"hi", "hello", "你好", "嗨"}:
        return "你好！你可以問我電影名稱、類型，或輸入「編號 1」查看電影詳細資料。"

    id_match = re.search(r"(?:編號|id)?\s*(\d+)", text, re.IGNORECASE)
    if id_match:
        movie = get_movie_by_id(int(id_match.group(1)))
        if movie:
            return format_movie(movie)

    results = search_movies(text)
    if results:
        lines = [f"找到 {len(results)} 部相關電影："]
        for movie in results[:10]:
            lines.append(f"- {movie['cn_name']} ({movie['en_name']})，評分 {movie['score']}")
        if len(results) > 10:
            lines.append(f"還有 {len(results) - 10} 部，請用更精準的關鍵字搜尋。")
        return "\n".join(lines)

    return "目前沒有找到相關電影。你可以試試電影名稱、英文片名、類型，或輸入「編號 1」。"


def build_reply(message: str) -> str:
    text = message.strip()
    if not text:
        return "請輸入想查詢的電影問題。"

    if not GEMINI_API_KEY:
        return fallback_reply(text)

    try:
        model = genai.GenerativeModel(
            GEMINI_MODEL,
            system_instruction=(
                "你是一位電影資料查詢助理，只根據下列電影資料回答。"
                "回答請使用繁體中文，簡潔、友善，並優先推薦資料中存在的電影。\n\n"
                f"電影資料 JSON：\n{movie_context}"
            ),
        )
        response = model.generate_content(text)
        if response.text:
            return response.text.strip()
        return fallback_reply(text)
    except Exception as exc:
        return f"Gemini API 暫時無法回覆，先用本地資料查詢：\n\n{fallback_reply(text)}\n\n錯誤：{exc}"


@app.get("/api/movies")
def get_movies(
    category: str | None = Query(default=None),
    search: str | None = Query(default=None),
    limit: int = Query(default=100, ge=1, le=100),
):
    result = movies
    if category:
        result = [movie for movie in result if category in movie["categories"]]
    if search:
        kw = search.lower()
        result = [
            movie
            for movie in result
            if kw in movie["cn_name"].lower() or kw in movie["en_name"].lower()
        ]
    return result[:limit]


@app.get("/api/movies/{movie_id}")
def get_movie(movie_id: int):
    movie = get_movie_by_id(movie_id)
    if not movie:
        return {"error": "not found"}
    return movie


@app.get("/api/categories")
def get_categories():
    categories = set()
    for movie in movies:
        for category in movie["categories"].split("、"):
            category = category.strip()
            if category:
                categories.add(category)
    return sorted(categories)


@app.post("/api/chat")
def chat(req: ChatRequest):
    return {"reply": build_reply(req.message)}


if not os.getenv("VERCEL"):
    app.mount("/", StaticFiles(directory=str(BASE_DIR), html=True), name="static")
