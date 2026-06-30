import json

with open("movies.json", "r", encoding="utf-8") as f:
    movies = json.load(f)

all_categories = set()
for m in movies:
    for c in m["categories"].split("、"):
        if c:
            all_categories.add(c)
all_categories = sorted(all_categories)

html = r"""<!DOCTYPE html>
<html lang="zh-TW">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>電影資訊</title>
<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: #f0f2f5; color: #333; }
.header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: #fff; padding: 30px 20px; text-align: center; }
.header h1 { font-size: 28px; margin-bottom: 6px; }
.header p { opacity: .85; font-size: 14px; }
.controls { max-width: 1200px; margin: 20px auto 0; padding: 0 20px; display: flex; flex-wrap: wrap; gap: 12px; align-items: center; }
.search-box { flex: 1; min-width: 200px; }
.search-box input { width: 100%; padding: 10px 16px; border: 2px solid #ddd; border-radius: 8px; font-size: 15px; outline: none; transition: border .2s; }
.search-box input:focus { border-color: #667eea; }
.categories { display: flex; flex-wrap: wrap; gap: 8px; }
.categories button { padding: 6px 16px; border: 2px solid #ddd; border-radius: 20px; background: #fff; cursor: pointer; font-size: 13px; transition: all .2s; }
.categories button:hover { border-color: #667eea; color: #667eea; }
.categories button.active { background: #667eea; color: #fff; border-color: #667eea; }
.count { font-size: 14px; color: #888; margin-left: auto; }
.grid { max-width: 1200px; margin: 20px auto; padding: 0 20px; display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 20px; }
.card { background: #fff; border-radius: 12px; overflow: hidden; box-shadow: 0 2px 12px rgba(0,0,0,.08); transition: transform .2s, box-shadow .2s; }
.card:hover { transform: translateY(-4px); box-shadow: 0 8px 24px rgba(0,0,0,.12); }
.card-img { width: 100%; height: 380px; object-fit: cover; background: #eee; display: block; }
.card-body { padding: 14px 16px 16px; }
.card-body h3 { font-size: 16px; margin-bottom: 2px; }
.card-body .en-name { font-size: 12px; color: #999; margin-bottom: 8px; }
.card-tags { display: flex; flex-wrap: wrap; gap: 4px; margin-bottom: 8px; }
.card-tags span { padding: 2px 10px; border-radius: 10px; font-size: 11px; background: #eef1ff; color: #667eea; cursor: pointer; transition: background .2s; }
.card-tags span:hover { background: #667eea; color: #fff; }
.card-info { font-size: 13px; color: #666; line-height: 1.8; }
.card-info .label { color: #999; }
.card-footer { display: flex; justify-content: space-between; align-items: center; margin-top: 10px; padding-top: 10px; border-top: 1px solid #f0f0f0; }
.score { font-size: 20px; font-weight: 700; color: #f5a623; }
.no-result { grid-column: 1 / -1; text-align: center; padding: 60px 20px; color: #999; font-size: 16px; }

/* Chat */
.chat-toggle { position: fixed; bottom: 24px; right: 24px; width: 56px; height: 56px; border-radius: 50%; background: linear-gradient(135deg, #667eea, #764ba2); color: #fff; border: none; font-size: 24px; cursor: pointer; box-shadow: 0 4px 16px rgba(102,126,234,.4); z-index: 999; transition: transform .2s; }
.chat-toggle:hover { transform: scale(1.1); }
.chat-panel { position: fixed; bottom: 90px; right: 24px; width: 380px; height: 520px; background: #fff; border-radius: 16px; box-shadow: 0 8px 32px rgba(0,0,0,.15); display: none; flex-direction: column; z-index: 999; overflow: hidden; }
.chat-panel.open { display: flex; }
.chat-header { background: linear-gradient(135deg, #667eea, #764ba2); color: #fff; padding: 14px 18px; font-weight: 600; font-size: 15px; }
.chat-msgs { flex: 1; overflow-y: auto; padding: 14px; display: flex; flex-direction: column; gap: 10px; background: #f8f9fb; }
.chat-msgs .msg { max-width: 85%; padding: 10px 14px; border-radius: 12px; font-size: 13px; line-height: 1.6; white-space: pre-wrap; word-break: break-word; }
.chat-msgs .msg.user { align-self: flex-end; background: #667eea; color: #fff; border-bottom-right-radius: 4px; }
.chat-msgs .msg.bot { align-self: flex-start; background: #fff; color: #333; border-bottom-left-radius: 4px; box-shadow: 0 1px 4px rgba(0,0,0,.06); }
.chat-input-area { display: flex; padding: 10px 14px; gap: 8px; border-top: 1px solid #eee; background: #fff; }
.chat-input-area input { flex: 1; padding: 10px 14px; border: 2px solid #ddd; border-radius: 24px; font-size: 13px; outline: none; }
.chat-input-area input:focus { border-color: #667eea; }
.chat-input-area button { padding: 10px 18px; border-radius: 24px; border: none; background: #667eea; color: #fff; font-size: 13px; cursor: pointer; font-weight: 600; }
.chat-input-area button:hover { background: #5a6fd6; }
.chat-input-area button:disabled { opacity: .5; cursor: not-allowed; }
</style>
</head>
<body>

<div class="header">
  <h1>🎬 電影資訊</h1>
  <p>共 <span id="total">0</span> 部電影</p>
</div>

<div class="controls">
  <div class="search-box">
    <input type="text" id="search" placeholder="搜尋電影名稱…" oninput="render()">
  </div>
  <div class="categories" id="categories"></div>
  <div class="count" id="count"></div>
</div>

<div class="grid" id="grid"></div>

<button class="chat-toggle" id="chatToggle" onclick="toggleChat()">💬</button>
<div class="chat-panel" id="chatPanel">
  <div class="chat-header">🤖 電影小幫手</div>
  <div class="chat-msgs" id="chatMsgs"></div>
  <div class="chat-input-area">
    <input type="text" id="chatInput" placeholder="輸入訊息…" onkeydown="if(event.key==='Enter') sendChat()">
    <button id="chatSend" onclick="sendChat()">傳送</button>
  </div>
</div>

<script>
const movies = """ + json.dumps(movies, ensure_ascii=False) + r""";

const allCategories = """ + json.dumps(all_categories, ensure_ascii=False) + r""";

let activeCategory = null;
let searchText = '';

function initCategories() {
  const container = document.getElementById('categories');
  const allBtn = document.createElement('button');
  allBtn.textContent = '全部';
  allBtn.className = 'active';
  allBtn.onclick = () => { activeCategory = null; document.querySelectorAll('#categories button').forEach(b => b.classList.remove('active')); allBtn.classList.add('active'); render(); };
  container.appendChild(allBtn);
  allCategories.forEach(cat => {
    const btn = document.createElement('button');
    btn.textContent = cat;
    btn.onclick = () => { activeCategory = cat; document.querySelectorAll('#categories button').forEach(b => b.classList.remove('active')); btn.classList.add('active'); render(); };
    container.appendChild(btn);
  });
}

function render() {
  searchText = document.getElementById('search').value.trim().toLowerCase();
  const filtered = movies.filter(m => {
    if (activeCategory && !m.categories.includes(activeCategory)) return false;
    if (searchText) {
      const match = m.cn_name.toLowerCase().includes(searchText) ||
                    m.en_name.toLowerCase().includes(searchText);
      if (!match) return false;
    }
    return true;
  });
  document.getElementById('total').textContent = movies.length;
  document.getElementById('count').textContent = `顯示 ${filtered.length} / ${movies.length} 部`;
  const grid = document.getElementById('grid');
  if (filtered.length === 0) {
    grid.innerHTML = '<div class="no-result">沒有符合條件的電影</div>';
    return;
  }
  grid.innerHTML = filtered.map(m => `
    <div class="card">
      <img class="card-img" src="${m.cover}" alt="${m.cn_name}" loading="lazy" onerror="this.src='data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 width=%22280%22 height=%22380%22><rect fill=%22%23eee%22 width=%22280%22 height=%22380%22/><text x=%22140%22 y=%22190%22 text-anchor=%22middle%22 fill=%22%23999%22 font-size=%2216%22>無海報</text></svg>'">
      <div class="card-body">
        <h3>${m.cn_name}</h3>
        <div class="en-name">${m.en_name}</div>
        <div class="card-tags">${m.categories.split('、').map(c => `<span onclick="filterCategory('${c}')">${c}</span>`).join('')}</div>
        <div class="card-info">
          <div><span class="label">地區</span> ${m.region}</div>
          <div><span class="label">時長</span> ${m.duration}</div>
          <div><span class="label">上映</span> ${m.release_date || '未知'}</div>
        </div>
        <div class="card-footer">
          <span class="score">${m.score}</span>
          <span style="font-size:12px;color:#999;">#${m.id}</span>
        </div>
      </div>
    </div>
  `).join('');
}

function filterCategory(cat) {
  activeCategory = cat;
  document.querySelectorAll('#categories button').forEach(b => {
    b.classList.toggle('active', b.textContent === cat);
  });
  render();
}

initCategories();
render();

/* Chat */
let chatOpen = false;
function toggleChat() {
  chatOpen = !chatOpen;
  document.getElementById('chatPanel').classList.toggle('open', chatOpen);
  if (chatOpen && document.getElementById('chatMsgs').children.length === 0) {
    addMsg('bot', '你好！我可以幫你查電影 🤗\n\n試試打：\n• 「霸王別姬」— 搜尋電影\n• 「分類 劇情」— 依類別找\n• 「推薦 喜劇」— 推薦電影\n• 「編號 1」— 查詳細資訊');
  }
}
function addMsg(role, text) {
  const div = document.createElement('div');
  div.className = 'msg ' + role;
  div.textContent = text;
  document.getElementById('chatMsgs').appendChild(div);
  div.scrollIntoView({ behavior: 'smooth', block: 'end' });
}
async function sendChat() {
  const input = document.getElementById('chatInput');
  const btn = document.getElementById('chatSend');
  const text = input.value.trim();
  if (!text) return;
  input.value = '';
  addMsg('user', text);
  btn.disabled = true;
  try {
    const resp = await fetch('/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: text })
    });
    const data = await resp.json();
    addMsg('bot', data.reply);
  } catch {
    addMsg('bot', '⚠️ 連線失敗，請確認後端伺服器已啟動（python main.py）');
  }
  btn.disabled = false;
}
</script>
</body>
</html>"""

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("index.html 已產生")
