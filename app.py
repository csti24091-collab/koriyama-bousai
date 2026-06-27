"""
郡山市マイ・タイムラインDX
福島県河川流域総合情報システム（HTML）から阿武隈川・郡山エリアの
水位をスクレイピングで取得するリアルタイム連携版。

【取得戦略】
  1. 福島県河川システム（kaseninf.pref.fukushima.jp）
     - 全県水位一覧表（ページ3）から「阿久津(国)」または「御代田(国)」の水位を取得
     - 郡山市の洪水予報基準は阿武隈川上流「阿久津」観測所
  2. 国交省 川の防災情報 HTMLページ（フォールバック）
  3. 完全取得失敗時 → 手動フォールバックUIへ
"""

import re
import os
import json
import requests
import streamlit as st
from datetime import datetime

# ── 多言語対応モジュール ──────────────────────────────────
from i18n import LANGUAGES, UI, PHASES, TASKS as I18N_TASKS
from i18n import t as tr
from i18n import t_phase as tr_phase
from i18n import t_task as tr_task
from i18n import google_translate_url

# ── BeautifulSoup のインポート（存在確認） ──────────────────
try:
    from bs4 import BeautifulSoup
    BS4_AVAILABLE = True
except ImportError:
    BS4_AVAILABLE = False

# ─────────────────────────────────────────
# ページ設定
# ─────────────────────────────────────────
st.set_page_config(
    page_title="郡山市マイ・タイムラインDX",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────
# グローバルCSS：シンプル・すっきりデザイン
# ─────────────────────────────────────────
st.markdown("""
<style>
/* ── フォント ── */
html, body, [class*="css"] {
    font-family: 'Hiragino Sans', 'Meiryo', 'Yu Gothic', sans-serif;
}

/* ── メインの余白を詰める ── */
.block-container {
    padding-top: 1.5rem;
    padding-bottom: 1rem;
    max-width: 1100px;
}

/* ── タイトル ── */
h1 { font-size: 1.6rem !important; font-weight: 700; color: #1a237e; }
h2 { font-size: 1.2rem !important; font-weight: 600; color: #283593; border-bottom: 2px solid #e8eaf6; padding-bottom: 4px; }
h3 { font-size: 1.05rem !important; font-weight: 600; color: #37474f; }

/* ── メトリクスカード ── */
[data-testid="metric-container"] {
    background: #f8f9ff;
    border: 1px solid #e8eaf6;
    border-radius: 10px;
    padding: 12px 16px !important;
}
[data-testid="metric-container"] label { color: #78909c !important; font-size: 0.8rem !important; }
[data-testid="metric-container"] [data-testid="stMetricValue"] { font-size: 1.3rem !important; color: #1a237e !important; font-weight: 700; }

/* ── ボタン（プライマリ） ── */
.stButton > button[kind="primary"] {
    background: #1a237e;
    color: white;
    border: none;
    border-radius: 8px;
    padding: 8px 20px;
    font-weight: 600;
    transition: background 0.2s;
}
.stButton > button[kind="primary"]:hover { background: #283593; }

/* ── ボタン（セカンダリ） ── */
.stButton > button {
    border-radius: 8px;
    border: 1px solid #c5cae9;
    color: #3949ab;
    font-weight: 500;
    transition: all 0.2s;
}
.stButton > button:hover { background: #e8eaf6; border-color: #3949ab; }

/* ── ラジオボタン ── */
[data-testid="stRadio"] label { font-size: 0.95rem; }

/* ── チェックボックス ── */
[data-testid="stCheckbox"] label { font-size: 0.95rem; color: #37474f; }

/* ── info/success/warning/error ── */
[data-testid="stAlert"] { border-radius: 8px; border-left-width: 4px; }

/* ── expander ── */
[data-testid="stExpander"] { border: 1px solid #e8eaf6; border-radius: 8px; }
[data-testid="stExpander"] summary { font-weight: 500; color: #37474f; }

/* ── プログレスバー ── */
[data-testid="stProgressBar"] > div > div { background: #3949ab; border-radius: 4px; }

/* ── タブ ── */
[data-testid="stTabs"] [role="tab"] { font-weight: 500; color: #546e7a; }
[data-testid="stTabs"] [role="tab"][aria-selected="true"] { color: #1a237e; border-bottom: 2px solid #1a237e; }

/* ── サイドバー ── */
[data-testid="stSidebar"] {
    background: #f8f9ff;
    border-right: 1px solid #e8eaf6;
}
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: #1a237e;
    border-bottom: none;
    font-size: 0.95rem !important;
}

/* ── 区切り線 ── */
hr { border: none; border-top: 1px solid #e8eaf6; margin: 1rem 0; }

/* ── テーブル ── */
table { border-collapse: collapse; width: 100%; font-size: 0.9rem; }
th { background: #e8eaf6; color: #1a237e; padding: 8px 12px; text-align: left; }
td { padding: 7px 12px; border-bottom: 1px solid #f0f0f0; }

/* ── download_button ── */
[data-testid="stDownloadButton"] > button {
    border-radius: 8px;
    border: 1px solid #c5cae9;
    color: #3949ab;
    font-weight: 500;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────
# サイドバー
# ─────────────────────────────────────────
st.sidebar.markdown(
    '<div style="font-size:1.05rem;font-weight:700;color:#1a237e;padding:4px 0;">🛡️ Koriyama Timeline DX</div>',
    unsafe_allow_html=True,
)
st.sidebar.markdown("---")

# ── 言語選択 ──────────────────────────────────
if "lang" not in st.session_state:
    st.session_state.lang = "ja"

lang_codes  = list(LANGUAGES.keys())
lang_labels = [LANGUAGES[c] for c in lang_codes]

selected_label = st.sidebar.selectbox(
    "🌐 Language / 言語",
    lang_labels,
    index=lang_codes.index(st.session_state.lang),
)
st.session_state.lang = lang_codes[lang_labels.index(selected_label)]
lang = st.session_state.lang

# ── 文字サイズ選択 ──────────────────────────────
if "font_size" not in st.session_state:
    st.session_state.font_size = "normal"

font_size_options = ["normal", "large"]
font_size_labels  = [tr(lang, "font_size_normal"), tr(lang, "font_size_large")]

selected_font_label = st.sidebar.radio(
    tr(lang, "font_size_select"),
    font_size_labels,
    index=font_size_options.index(st.session_state.font_size),
    horizontal=True,
)
st.session_state.font_size = font_size_options[font_size_labels.index(selected_font_label)]
font_size = st.session_state.font_size

# 文字サイズに応じたCSSを注入（「大きい」選択時に全体のフォントを拡大）
if font_size == "large":
    st.markdown("""
    <style>
    /* ── 文字サイズ「大」モード ── */
    html, body, [class*="css"] { font-size: 1.25rem !important; }
    h1 { font-size: 2rem !important; }
    h2 { font-size: 1.55rem !important; }
    h3 { font-size: 1.35rem !important; }
    p, li, span, div, label { font-size: 1.15rem !important; line-height: 1.7 !important; }

    /* チェックボックス・ラジオのラベルを大きく */
    [data-testid="stCheckbox"] label, [data-testid="stRadio"] label {
        font-size: 1.2rem !important;
    }
    [data-testid="stCheckbox"] svg, [data-testid="stRadio"] svg {
        width: 1.4em !important; height: 1.4em !important;
    }

    /* メトリクス値を大きく */
    [data-testid="metric-container"] [data-testid="stMetricValue"] {
        font-size: 1.7rem !important;
    }
    [data-testid="metric-container"] label { font-size: 1rem !important; }

    /* ボタン文字を大きく */
    .stButton > button, [data-testid="stDownloadButton"] > button {
        font-size: 1.15rem !important;
        padding: 10px 24px !important;
    }

    /* サイドバーのラベルも大きく */
    [data-testid="stSidebar"] label, [data-testid="stSidebar"] div {
        font-size: 1.1rem !important;
    }

    /* キャプション・小文字も視認性確保 */
    [data-testid="stCaptionContainer"], small, .stCaption {
        font-size: 0.95rem !important;
    }
    </style>
    """, unsafe_allow_html=True)

st.sidebar.markdown("---")
st.sidebar.markdown(f"**{tr(lang, 'household_status')}**")
has_elderly = st.sidebar.checkbox(tr(lang, "has_elderly"))
has_car     = st.sidebar.checkbox(tr(lang, "has_car"))
st.sidebar.markdown("---")
st.sidebar.markdown(f"**{tr(lang, 'mode_label')}**")

MODE_KEYS = ["mode_normal", "mode_realtime", "mode_weather", "mode_task_manage"]
mode_labels = [tr(lang, k) for k in MODE_KEYS]
selected_mode_label = st.sidebar.radio(
    "Mode",
    mode_labels,
    label_visibility="collapsed",
)
# 内部処理用に日本語モードキーへマッピング
MODE_JA = {
    "mode_normal":      "通常（手動選択）",
    "mode_realtime":    "📡 リアルタイム水位連携",
    "mode_weather":     "🌤️ 郡山市天気",
    "mode_task_manage": "✏️ タスク管理",
}
mode = MODE_JA[MODE_KEYS[mode_labels.index(selected_mode_label)]]

# ── ヘッダー（言語選択後に表示するため位置調整）──────────
st.markdown(f"""
<div style="display:flex;align-items:center;gap:12px;margin-bottom:4px;">
  <div style="font-size:2rem;">🛡️</div>
  <div>
    <div style="font-size:1.4rem;font-weight:700;color:#1a237e;line-height:1.2;">
      {tr(lang, 'app_title')}
    </div>
    <div style="font-size:0.8rem;color:#78909c;">
      {tr(lang, 'app_subtitle')}
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────
# タスクデータ（tasks.json がなければ内蔵データ）
# ─────────────────────────────────────────
BUILTIN_TASKS = [
    # 平時
    {"phase": "平時（備えの期間）",           "condition": "all",         "text": "ハザードマップで自宅・職場の浸水想定区域を確認する"},
    {"phase": "平時（備えの期間）",           "condition": "all",         "text": "避難場所・避難経路を家族で確認しておく"},
    {"phase": "平時（備えの期間）",           "condition": "all",         "text": "非常用持ち出し袋（3日分）を準備する"},
    {"phase": "平時（備えの期間）",           "condition": "all",         "text": "緊急連絡先を家族全員で共有する"},
    {"phase": "平時（備えの期間）",           "condition": "has_elderly", "text": "【高齢者等】福祉避難所の場所と利用方法を確認する"},
    {"phase": "平時（備えの期間）",           "condition": "has_car",     "text": "【車避難】渋滞を避けた避難ルートを複数確認しておく"},
    # 3日前
    {"phase": "台風上陸の3日前（準備開始）",  "condition": "all",         "text": "気象情報・台風進路予報を確認し、今後の動向に注意する"},
    {"phase": "台風上陸の3日前（準備開始）",  "condition": "all",         "text": "非常用持ち出し袋の内容を点検・補充する"},
    {"phase": "台風上陸の3日前（準備開始）",  "condition": "all",         "text": "食料・飲料水（3〜7日分）の備蓄を確認・補充する"},
    {"phase": "台風上陸の3日前（準備開始）",  "condition": "all",         "text": "スマートフォンのモバイルバッテリーを充電しておく"},
    {"phase": "台風上陸の3日前（準備開始）",  "condition": "has_car",     "text": "【車避難】ガソリンを満タンにしておく"},
    {"phase": "台風上陸の3日前（準備開始）",  "condition": "has_elderly", "text": "【高齢者等】要介護者の状態と避難介助方法を事前に確認する"},
    # 注意報
    {"phase": "大雨・洪水注意報発表 (-24h)", "condition": "all",         "text": "郡山市・気象庁の最新情報を継続的に確認する"},
    {"phase": "大雨・洪水注意報発表 (-24h)", "condition": "all",         "text": "避難場所の開設状況を市公式SNS・防災メールで確認する"},
    {"phase": "大雨・洪水注意報発表 (-24h)", "condition": "all",         "text": "浴槽・ポリタンクに生活用水を確保する"},
    {"phase": "大雨・洪水注意報発表 (-24h)", "condition": "has_car",     "text": "【車避難】車を浸水しにくい高台の駐車場に移動させる"},
    {"phase": "大雨・洪水注意報発表 (-24h)", "condition": "has_elderly", "text": "【高齢者等】避難に時間がかかるため、早めの避難開始を検討する"},
    # 水防団待機水位
    {"phase": "水防団待機水位到達 (4.00m)",  "condition": "all",         "text": "阿武隈川の水位情報を10分ごとに確認する"},
    {"phase": "水防団待機水位到達 (4.00m)",  "condition": "all",         "text": "避難の準備を整え、いつでも出発できる状態にする"},
    {"phase": "水防団待機水位到達 (4.00m)",  "condition": "all",         "text": "隣近所・地域の要配慮者に声がけを開始する"},
    {"phase": "水防団待機水位到達 (4.00m)",  "condition": "has_elderly", "text": "【高齢者等】早期避難を開始する（次のフェーズを待たない）"},
    # 氾濫注意水位
    {"phase": "はん濫注意水位到達 (5.50m)",  "condition": "all",         "text": "郡山市の避難情報（避難指示・緊急安全確保）を随時確認する"},
    {"phase": "はん濫注意水位到達 (5.50m)",  "condition": "all",         "text": "外出は極力控え、自宅待機または避難先で待機する"},
    {"phase": "はん濫注意水位到達 (5.50m)",  "condition": "all",         "text": "非常用持ち出し袋を玄関に置き、すぐ持ち出せるようにする"},
    {"phase": "はん濫注意水位到達 (5.50m)",  "condition": "has_car",     "text": "【車避難】この段階以降の車避難は浸水リスクあり、徒歩避難も検討"},
    # 警戒レベル3
    {"phase": "警戒レベル3：高齢者等避難 発令 (5.70m)", "condition": "all",         "text": "📢 高齢者等避難 発令！高齢者・障がい者・乳幼児は直ちに避難する"},
    {"phase": "警戒レベル3：高齢者等避難 発令 (5.70m)", "condition": "all",         "text": "避難場所に向かう。安全が確認できない場合は2階以上へ垂直避難"},
    {"phase": "警戒レベル3：高齢者等避難 発令 (5.70m)", "condition": "has_elderly", "text": "【高齢者等】直ちに避難を開始する。介助者は最優先で行動する"},
    {"phase": "警戒レベル3：高齢者等避難 発令 (5.70m)", "condition": "has_car",     "text": "【車避難】冠水した道路への進入は絶対に避ける（30cm超で車が流される）"},
    # 警戒レベル4
    {"phase": "警戒レベル4：避難指示 発令 (6.80m)",     "condition": "all",         "text": "🚨 避難指示 発令！全員が直ちに避難を開始する"},
    {"phase": "警戒レベル4：避難指示 発令 (6.80m)",     "condition": "all",         "text": "避難場所への移動が困難な場合は近隣の頑丈な建物の上層階へ垂直避難"},
    {"phase": "警戒レベル4：避難指示 発令 (6.80m)",     "condition": "all",         "text": "家族の安否確認・集合場所を確認し、連絡手段を確保する"},
    {"phase": "警戒レベル4：避難指示 発令 (6.80m)",     "condition": "has_elderly", "text": "【高齢者等】介助者と合流し、福祉避難所への移動を優先する"},
    # 最大水位
    {"phase": "最大水位到達 (10.01m)",        "condition": "all",         "text": "⛔ 屋外への移動は生命の危険があります。今いる場所で安全確保"},
    {"phase": "最大水位到達 (10.01m)",        "condition": "all",         "text": "建物の上層階・屋根など、最も高い場所へ移動する（垂直避難）"},
    {"phase": "最大水位到達 (10.01m)",        "condition": "all",         "text": "救助要請：171（災害用伝言ダイヤル）、119番または110番に連絡"},
    {"phase": "最大水位到達 (10.01m)",        "condition": "all",         "text": "窓やドアを開けず、水位上昇に備え常に上方向への逃げ場を確保する"},
]

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
json_path = os.path.join(BASE_DIR, "tasks.json")


def load_tasks() -> list:
    """tasks.json を読み込む。なければ内蔵データを返す。"""
    if os.path.exists(json_path):
        with open(json_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return [t.copy() for t in BUILTIN_TASKS]


def save_tasks(tasks: list) -> None:
    """tasks.json に保存する。"""
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(tasks, f, ensure_ascii=False, indent=2)


# ── チェック記録（action_log.json）────────────────────────
log_path = os.path.join(BASE_DIR, "action_log.json")


def load_log() -> list:
    """action_log.json を読み込む。なければ空リストを返す。"""
    if os.path.exists(log_path):
        with open(log_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def save_log(log: list) -> None:
    """action_log.json に保存する。"""
    with open(log_path, "w", encoding="utf-8") as f:
        json.dump(log, f, ensure_ascii=False, indent=2)


def append_log_entry(phase: str, checked_tasks: list, mode: str) -> None:
    """チェック済みタスクを記録に追記する。"""
    log = load_log()
    log.append({
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "mode":      mode,
        "phase":     phase,
        "tasks":     checked_tasks,
    })
    save_log(log)


# セッションにタスクを保持（編集操作の反映のため）
if "all_tasks" not in st.session_state:
    st.session_state.all_tasks = load_tasks()

all_tasks = st.session_state.all_tasks

# ─────────────────────────────────────────
# 定数
# ─────────────────────────────────────────
SIM_PHASES = [
    "平時（備えの期間）",
    "台風上陸の3日前（準備開始）",
    "大雨・洪水注意報発表 (-24h)",
    "水防団待機水位到達 (4.00m)",
    "はん濫注意水位到達 (5.50m)",
    "警戒レベル3：高齢者等避難 発令 (5.70m)",
    "警戒レベル4：避難指示 発令 (6.80m)",
    "最大水位到達 (10.01m)",
]

PHASE_COLORS = {
    "平時（備えの期間）":                               "#4caf50",
    "台風上陸の3日前（準備開始）":                      "#8bc34a",
    "大雨・洪水注意報発表 (-24h)":                      "#f9a825",
    "水防団待機水位到達 (4.00m)":                       "#ff9800",
    "はん濫注意水位到達 (5.50m)":                       "#ff5722",
    "警戒レベル3：高齢者等避難 発令 (5.70m)":           "#f44336",
    "警戒レベル4：避難指示 発令 (6.80m)":              "#9c27b0",
    "最大水位到達 (10.01m)":                            "#212121",
}

# ── 観測所設定 ────────────────────────────────────────────
# 【阿武隈川本川】郡山市の洪水予報基準観測所（阿武隈川上流「阿久津」）
ABUKUMA_STATIONS = ["阿久津(国)"]

# 【逢瀬川】備前舘地区（逢瀬川左岸）の最寄り観測所
# 御代田(国) = 郡山市御代田・逢瀬川の国管理観測所
OSEGAWA_STATIONS = ["御代田(国)", "成山"]  # いずれかが見つかれば採用

# 逢瀬川の警戒基準水位（御代田観測所・暫定値 ※要実環境確認）
OSEGAWA_THRESHOLDS = {
    "水防団待機": 1.20,
    "氾濫注意":   2.00,
    "避難判断":   2.80,
    "氾濫危険":   3.20,
}

# 福島県システム URLテンプレート（ページ 1〜9 まで存在）
FUKUSHIMA_URL_TMPL = (
    "https://kaseninf.pref.fukushima.jp"
    "/web_pub/stageState/010301_10_{page}_0.html"
)
# ページ2に御代田(国)、ページ3に阿久津(国) が存在
ABUKUMA_PAGES  = [3, 4, 1]   # 阿武隈川系（阿久津）優先ページ
OSEGAWA_PAGES  = [2, 3, 4]   # 逢瀬川系（御代田）優先ページ


def level_to_phase(level: float) -> str:
    if level >= 10.01:
        return "最大水位到達 (10.01m)"
    elif level >= 6.80:
        return "警戒レベル4：避難指示 発令 (6.80m)"
    elif level >= 5.70:
        return "警戒レベル3：高齢者等避難 発令 (5.70m)"
    elif level >= 5.50:
        return "はん濫注意水位到達 (5.50m)"
    elif level >= 4.00:
        return "水防団待機水位到達 (4.00m)"
    else:
        return "平時（備えの期間）"


# ─────────────────────────────────────────
# 水位取得関数
# ─────────────────────────────────────────

def _parse_level_from_html(html: str, target_stations: list[str]) -> tuple[float | None, str | None]:
    """
    福島県システムの水位一覧表HTMLから指定観測局の水位を抽出。
    戻り値: (水位[m], 観測局名) or (None, None)
    """
    if not BS4_AVAILABLE:
        return None, None
    soup = BeautifulSoup(html, "html.parser")
    for row in soup.select("table tr"):
        cells = row.find_all("td")
        if len(cells) < 5:
            continue
        station_name = cells[2].get_text(strip=True)
        # リンクタグの中のテキストも考慮
        if not station_name:
            a = cells[2].find("a")
            if a:
                station_name = a.get_text(strip=True)
        for target in target_stations:
            if target in station_name:
                raw = cells[4].get_text(strip=True)
                # "2.34  →" や "**"（欠測）や "--"（未収集）
                match = re.search(r"-?\d+\.?\d*", raw)
                if match:
                    return float(match.group()), station_name
    return None, None


@st.cache_data(ttl=300)
def get_water_level_fukushima(stations: tuple, pages: tuple) -> tuple[float | None, str | None, str | None]:
    """
    福島県河川流域総合情報システムから指定観測局の水位を取得。
    stations: 検索対象観測局名のタプル
    pages:    優先して検索するページ番号のタプル
    戻り値: (水位[m], 観測局名, エラー文字列)
    """
    if not BS4_AVAILABLE:
        return None, None, "beautifulsoup4 が未インストールです。`pip install beautifulsoup4` を実行してください。"

    headers = {"User-Agent": "Mozilla/5.0 (compatible; DisasterApp/1.0)"}
    last_error = "観測局が見つかりませんでした"

    for page in pages:
        url = FUKUSHIMA_URL_TMPL.format(page=page)
        try:
            res = requests.get(url, timeout=12, headers=headers)
            res.raise_for_status()
            res.encoding = "utf-8"
            level, station = _parse_level_from_html(res.text, list(stations))
            if level is not None:
                return level, station, None
        except requests.Timeout:
            last_error = f"タイムアウト（ページ{page}）"
        except requests.ConnectionError:
            last_error = "接続エラー：ネットワークまたはサーバーが応答しません"
            break
        except requests.HTTPError as e:
            last_error = f"HTTPエラー {e.response.status_code}（ページ{page}）"
        except Exception as e:
            last_error = f"予期しないエラー: {e}"

    return None, None, last_error


@st.cache_data(ttl=300)
def get_water_level_mlit_html() -> tuple[float | None, str | None, str | None]:
    """
    国交省 福島河川国道事務所の阿武隈川概況ページから
    郡山観測所の水位をフォールバック取得。
    （ページがJavaScript依存のため取得できない場合は None を返す）
    戻り値: (水位[m], 観測局名, エラー文字列)
    """
    if not BS4_AVAILABLE:
        return None, None, "beautifulsoup4 未インストール"

    url = "https://www.thr.mlit.go.jp/fukushima/abukuma_gaikyou/suii.html"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        res = requests.get(url, timeout=10, headers=headers)
        res.raise_for_status()
        res.encoding = "utf-8"
        soup = BeautifulSoup(res.text, "html.parser")
        # テーブルまたはテキストから「郡山」付近の数値を探索
        text = soup.get_text()
        # 「郡山 X.XX m」パターン
        match = re.search(r"郡山[^\d]{0,10}(-?\d+\.\d+)\s*m", text)
        if match:
            return float(match.group(1)), "郡山(国交省概況)", None
        return None, None, "郡山の水位値がページ内に見つかりません（JS動的ページの可能性）"
    except requests.Timeout:
        return None, None, "タイムアウト（国交省概況ページ）"
    except requests.ConnectionError:
        return None, None, "接続エラー（国交省概況ページ）"
    except Exception as e:
        return None, None, f"エラー: {e}"


def _river_result(level, station, source, source_url, timestamp, fallback=False, error=None):
    return {
        "level": level, "station": station,
        "source": source, "source_url": source_url,
        "timestamp": timestamp, "error": error, "fallback_used": fallback,
    }


def get_water_level() -> dict:
    """阿武隈川（阿久津）水位を取得して返す。"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    src = "福島県河川流域総合情報システム"
    src_url = "https://kaseninf.pref.fukushima.jp/"

    level, station, err1 = get_water_level_fukushima(
        tuple(ABUKUMA_STATIONS), tuple(ABUKUMA_PAGES)
    )
    if level is not None:
        return _river_result(level, station, src, src_url, timestamp)

    level2, station2, err2 = get_water_level_mlit_html()
    if level2 is not None:
        return _river_result(level2, station2,
            "国交省 福島河川国道事務所（フォールバック）",
            "https://www.thr.mlit.go.jp/fukushima/abukuma_gaikyou/suii.html",
            timestamp, fallback=True)

    combined_error = f"【県システム】{err1}　/　【国交省】{err2}"
    return {
        "level": None,
        "station": None,
        "source": None,
        "source_url": None,
        "timestamp": timestamp,
        "error": combined_error,
        "fallback_used": True,
    }



def get_osegawa_level() -> dict:
    """逢瀬川（御代田観測所）水位を取得して返す。備前舘地区向け。"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    src = "福島県河川流域総合情報システム"
    src_url = "https://kaseninf.pref.fukushima.jp/"

    level, station, err = get_water_level_fukushima(
        tuple(OSEGAWA_STATIONS), tuple(OSEGAWA_PAGES)
    )
    if level is not None:
        return _river_result(level, station, src, src_url, timestamp)
    return {
        "level": None, "station": None, "source": None, "source_url": None,
        "timestamp": timestamp, "error": err, "fallback_used": False,
    }


def osegawa_level_to_alert(level: float) -> tuple[str, str]:
    """逢瀬川水位から警戒段階と色を返す。"""
    thr = OSEGAWA_THRESHOLDS
    if level >= thr["氾濫危険"]:
        return "氾濫危険水位超過 ⛔", "#9c27b0"
    elif level >= thr["避難判断"]:
        return "避難判断水位超過 🚨", "#f44336"
    elif level >= thr["氾濫注意"]:
        return "氾濫注意水位超過 ⚠️", "#ff5722"
    elif level >= thr["水防団待機"]:
        return "水防団待機水位超過 🔶", "#ff9800"
    else:
        return "通常 ✅", "#4caf50"


# ─────────────────────────────────────────
# 郡山AMeDAS 実況データ取得
# ─────────────────────────────────────────

# 郡山AMeDAS観測所コード
KORIYAMA_AMEDAS_CODE = "36476"

# 最新観測時刻URL
AMEDAS_LATEST_TIME_URL = "https://www.jma.go.jp/bosai/amedas/data/latest_time.txt"
# 全国一括マップURL（最新時刻指定）
AMEDAS_MAP_URL = "https://www.jma.go.jp/bosai/amedas/data/map/{timestamp}.json"

# 風向16方位
WIND_DIR = [
    "北","北北東","北東","東北東","東","東南東","南東","南南東",
    "南","南南西","南西","西南西","西","西北西","北西","北北西",
]


def _amedas_val(entry: dict, key: str):
    """AMeDASの [値, 品質コード] から値を取り出す。なければ None。"""
    v = entry.get(key)
    if isinstance(v, list) and len(v) >= 1:
        return v[0]
    return None


@st.cache_data(ttl=600)
def get_koriyama_amedas() -> dict:
    """
    郡山AMeDAS観測所（36661）の最新実況データを取得。
    戻り値: {
        "temp":           float | None,   # 気温(℃)
        "precipitation1h":float | None,   # 1時間降水量(mm)
        "precipitation10m":float | None,  # 10分降水量(mm)
        "wind":           float | None,   # 風速(m/s)
        "wind_dir":       str  | None,    # 風向
        "humidity":       float | None,   # 湿度(%)
        "pressure":       float | None,   # 現地気圧(hPa)
        "obs_time":       str,            # 観測時刻
        "timestamp":      str,            # 取得時刻
        "error":          str | None,
    }
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    headers   = {"User-Agent": "Mozilla/5.0"}

    try:
        # ① 最新観測時刻を取得（例: "20260607143000"）
        tr = requests.get(AMEDAS_LATEST_TIME_URL, timeout=8, headers=headers)
        tr.raise_for_status()
        latest_time = tr.text.strip()  # "2026-06-07T14:30:00+09:00" など

        # ISO形式 → yyyymmddHHMMSS 形式に変換
        from datetime import datetime as dt, timezone, timedelta
        JST = timezone(timedelta(hours=9))
        try:
            obs_dt = dt.fromisoformat(latest_time)
        except ValueError:
            # すでに数値形式の場合
            obs_dt = dt.strptime(latest_time[:14], "%Y%m%d%H%M%S")
        obs_dt_jst = obs_dt.astimezone(JST)
        ts_str     = obs_dt_jst.strftime("%Y%m%d%H%M%S")  # "20260607143000"
        obs_time   = obs_dt_jst.strftime("%H:%M")

        # ② 全国マップJSONから郡山の実況を取得
        map_url = AMEDAS_MAP_URL.format(timestamp=ts_str)
        mr = requests.get(map_url, timeout=10, headers=headers)
        mr.raise_for_status()
        map_data = mr.json()

        entry = map_data.get(KORIYAMA_AMEDAS_CODE, {})
        if not entry:
            return {"error": f"郡山観測所（{KORIYAMA_AMEDAS_CODE}）のデータが見つかりません",
                    "timestamp": timestamp, "obs_time": "--"}

        # 風向を文字列に変換（1〜16の整数）
        wind_dir_idx = _amedas_val(entry, "windDirection")
        wind_dir_str = WIND_DIR[wind_dir_idx - 1] if wind_dir_idx and 1 <= wind_dir_idx <= 16 else None

        return {
            "temp":            _amedas_val(entry, "temp"),
            "precipitation1h": _amedas_val(entry, "precipitation1h"),
            "precipitation10m":_amedas_val(entry, "precipitation10m"),
            "wind":            _amedas_val(entry, "wind"),
            "wind_dir":        wind_dir_str,
            "humidity":        _amedas_val(entry, "humidity"),
            "pressure":        _amedas_val(entry, "normalPressure"),
            "obs_time":        obs_time,
            "timestamp":       timestamp,
            "error":           None,
        }

    except requests.Timeout:
        return {"error": "タイムアウト", "timestamp": timestamp, "obs_time": "--"}
    except requests.ConnectionError:
        return {"error": "接続エラー", "timestamp": timestamp, "obs_time": "--"}
    except Exception as e:
        return {"error": str(e), "timestamp": timestamp, "obs_time": "--"}


# ─────────────────────────────────────────
# 気象庁警報取得
# ─────────────────────────────────────────

# 気象庁 防災気象情報 XML（福島県：area_code=070000）
# 警報・注意報フィード（Atom）
JMA_FEED_URL = "https://www.jma.go.jp/bosai/warning/data/warning/070000.json"

# 警報種別 → フェーズへのマッピング
JMA_ALERT_PHASE = {
    "大雨特別警報":   "警戒レベル4：避難指示 発令 (6.80m)",
    "洪水特別警報":   "警戒レベル4：避難指示 発令 (6.80m)",
    "大雨警報":       "警戒レベル3：高齢者等避難 発令 (5.70m)",
    "洪水警報":       "警戒レベル3：高齢者等避難 発令 (5.70m)",
    "大雨注意報":     "大雨・洪水注意報発表 (-24h)",
    "洪水注意報":     "大雨・洪水注意報発表 (-24h)",
}

# 郡山市の市区町村コード（気象庁）
KORIYAMA_CITY_CODE = "0721300"


@st.cache_data(ttl=300)
def get_jma_warning() -> dict:
    """
    気象庁 警報・注意報JSON（福島県）から郡山市の警報情報を取得。
    戻り値: {
        "alerts":    発令中の警報リスト（最高レベル順）,
        "phase":     最も重い警報に対応するフェーズ,
        "color":     フェーズ色,
        "timestamp": 取得時刻,
        "error":     エラー文字列 or None,
    }
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    try:
        res = requests.get(JMA_FEED_URL, timeout=10,
                           headers={"User-Agent": "Mozilla/5.0"})
        res.raise_for_status()
        data = res.json()

        # 郡山市のエリア情報を探す
        found_alerts = []
        areas = data.get("areaTypes", [])
        for area_type in areas:
            for area in area_type.get("areas", []):
                if area.get("code", "") == KORIYAMA_CITY_CODE:
                    for warning in area.get("warnings", []):
                        status = warning.get("status", "")
                        name   = warning.get("name", "")
                        # 発令中（"発表"または"継続"）のみ取得
                        if status in ("発表", "継続") and name:
                            found_alerts.append(name)

        if not found_alerts:
            return {
                "alerts": [], "phase": None, "color": "#4caf50",
                "timestamp": timestamp, "error": None,
            }

        # 最も重い警報に対応するフェーズを決定
        best_phase = None
        best_idx   = len(SIM_PHASES)  # 大きいほど重い
        for alert in found_alerts:
            mapped = JMA_ALERT_PHASE.get(alert)
            if mapped and SIM_PHASES.index(mapped) > best_idx - 1:
                # SIM_PHASESは後ろに行くほど重大
                if SIM_PHASES.index(mapped) > (len(SIM_PHASES) - best_idx - 1):
                    best_phase = mapped
                    best_idx   = len(SIM_PHASES) - SIM_PHASES.index(mapped)

        # シンプルに：最もインデックスが大きいフェーズを採用
        best_phase = None
        for alert in found_alerts:
            mapped = JMA_ALERT_PHASE.get(alert)
            if mapped:
                if best_phase is None:
                    best_phase = mapped
                elif SIM_PHASES.index(mapped) > SIM_PHASES.index(best_phase):
                    best_phase = mapped

        color = PHASE_COLORS.get(best_phase, "#607d8b") if best_phase else "#4caf50"
        return {
            "alerts": found_alerts, "phase": best_phase, "color": color,
            "timestamp": timestamp, "error": None,
        }

    except requests.Timeout:
        return {"alerts": [], "phase": None, "color": "#607d8b",
                "timestamp": timestamp, "error": "タイムアウト"}
    except requests.ConnectionError:
        return {"alerts": [], "phase": None, "color": "#607d8b",
                "timestamp": timestamp, "error": "接続エラー"}
    except Exception as e:
        return {"alerts": [], "phase": None, "color": "#607d8b",
                "timestamp": timestamp, "error": str(e)}


# ─────────────────────────────────────────
# 気象庁 天気予報・現況取得
# ─────────────────────────────────────────

# 福島県予報区コード・中通りエリアコード
JMA_FORECAST_URL  = "https://www.jma.go.jp/bosai/forecast/data/forecast/070000.json"
JMA_OVERVIEW_URL  = "https://www.jma.go.jp/bosai/forecast/data/overview_forecast/070000.json"
# 中通り（郡山含む）のエリアコード
KORIYAMA_AREA_CODE = "070010"

# 天気コード → 絵文字マッピング
WEATHER_EMOJI = {
    "1": "☀️", "2": "☀️", "3": "☀️",   # 快晴・晴れ
    "4": "🌤️", "5": "🌤️", "6": "🌤️",  # 晴れ時々くもり
    "7": "⛅", "8": "⛅", "9": "⛅",     # 晴れ一時くもり
    "10": "🌥️","11": "🌥️","12": "🌥️", # くもり
    "13": "🌦️","14": "🌦️","15": "🌦️", # くもり時々雨
    "16": "🌧️","17": "🌧️","18": "🌧️", # 雨
    "19": "⛈️","20": "⛈️",              # 雷雨
    "21": "🌨️","22": "🌨️",              # 雪
}

def _weather_emoji(code: str) -> str:
    """天気コードから絵文字を返す。"""
    if not code:
        return "🌡️"
    # コード先頭1〜2桁で判定
    for length in (3, 2, 1):
        key = code[:length].lstrip("0") or "0"
        if key in WEATHER_EMOJI:
            return WEATHER_EMOJI[key]
    c = int(code)
    if c < 200:   return "☀️"
    elif c < 300: return "⛅"
    elif c < 400: return "🌧️"
    elif c < 500: return "🌨️"
    return "🌡️"


@st.cache_data(ttl=600)
def get_jma_forecast() -> dict:
    """
    気象庁 天気予報JSON（福島県）から郡山（中通り）の情報を取得。
    戻り値: {
        "overview":   str,          # 天気概況テキスト
        "today":      dict,         # 今日の予報
        "tomorrow":   dict,         # 明日の予報
        "weekly":     list[dict],   # 週間予報リスト
        "timestamp":  str,
        "error":      str | None,
    }
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        # ── 天気概況テキスト ──────────────────────────
        ov_res  = requests.get(JMA_OVERVIEW_URL, timeout=10, headers=headers)
        ov_res.raise_for_status()
        ov_data = ov_res.json()
        overview = ov_data.get("text", "")

        # ── 天気予報JSON ──────────────────────────────
        fc_res  = requests.get(JMA_FORECAST_URL, timeout=10, headers=headers)
        fc_res.raise_for_status()
        fc_data = fc_res.json()

        # 直近予報（fc_data[0]）と週間予報（fc_data[1]）
        short  = fc_data[0]  # 今日〜明後日
        weekly = fc_data[1]  # 週間

        # 中通りエリアを検索
        def find_area(time_series_list, code):
            for ts in time_series_list:
                for area in ts.get("areas", []):
                    if area.get("area", {}).get("code") == code:
                        return ts, area
            return None, None

        # 天気（weatherCodes）
        ts_w, area_w = find_area(short.get("timeSeries", []), KORIYAMA_AREA_CODE)
        # 気温
        ts_t, area_t = find_area(short.get("timeSeries", []), KORIYAMA_AREA_CODE)
        # 降水確率
        ts_p, area_p = find_area(short.get("timeSeries", []), KORIYAMA_AREA_CODE)

        def safe_list(d, key):
            return d.get(key, []) if d else []

        # timeSeries[0] = 天気・風・波, [1] = 降水確率, [2] = 気温
        time_series = short.get("timeSeries", [])

        weather_ts  = time_series[0] if len(time_series) > 0 else {}
        pop_ts      = time_series[1] if len(time_series) > 1 else {}
        temp_ts     = time_series[2] if len(time_series) > 2 else {}

        def get_area_data(ts, code):
            for area in ts.get("areas", []):
                if area.get("area", {}).get("code") == code:
                    return area
            return {}

        w_area = get_area_data(weather_ts, KORIYAMA_AREA_CODE)
        p_area = get_area_data(pop_ts,     KORIYAMA_AREA_CODE)
        t_area = get_area_data(temp_ts,    KORIYAMA_AREA_CODE)

        weather_times  = weather_ts.get("timeDefines", [])
        weather_codes  = w_area.get("weatherCodes", [])
        weathers       = w_area.get("weathers",     [])
        winds          = w_area.get("winds",        [])
        pop_times      = pop_ts.get("timeDefines",  [])
        pops           = p_area.get("pops",         [])
        temp_times     = temp_ts.get("timeDefines", [])
        temps          = t_area.get("temps",        [])

        def fmt_date(iso):
            try:
                from datetime import datetime as dt
                d = dt.fromisoformat(iso.replace("Z", "+00:00"))
                return d.strftime("%m/%d(%a)").replace(
                    "Mon","月").replace("Tue","火").replace("Wed","水"
                    ).replace("Thu","木").replace("Fri","金"
                    ).replace("Sat","土").replace("Sun","日")
            except Exception:
                return iso[:10]

        # 今日・明日を構築
        days = []
        for i, t in enumerate(weather_times[:3]):
            days.append({
                "date":    fmt_date(t),
                "code":    weather_codes[i] if i < len(weather_codes) else "",
                "weather": weathers[i]      if i < len(weathers)      else "",
                "wind":    winds[i]         if i < len(winds)         else "",
            })

        # 降水確率を日付ごとにまとめる（6h単位 → 日単位）
        pop_by_date: dict[str, list] = {}
        for i, t in enumerate(pop_times):
            date_key = t[:10]
            pop_by_date.setdefault(date_key, [])
            if i < len(pops) and pops[i] != "":
                pop_by_date[date_key].append(pops[i])

        for day in days:
            date_key = ""
            for t in weather_times:
                if fmt_date(t) == day["date"]:
                    for orig_t in weather_times:
                        if fmt_date(orig_t) == day["date"]:
                            date_key = orig_t[:10]
                            break
                    break
            pops_today = pop_by_date.get(date_key, [])
            day["pops"] = pops_today  # 例: ["20", "30", "40", "10"]

        # 気温（最低・最高）
        temp_by_date: dict[str, dict] = {}
        for i, t in enumerate(temp_times):
            date_key = t[:10]
            temp_by_date.setdefault(date_key, {})
            val = temps[i] if i < len(temps) else ""
            # 偶数インデックス=最低気温, 奇数=最高気温（気象庁の仕様）
            if i % 2 == 0:
                temp_by_date[date_key]["min"] = val
            else:
                temp_by_date[date_key]["max"] = val

        for day in days:
            for orig_t in weather_times:
                if fmt_date(orig_t) == day["date"]:
                    date_key = orig_t[:10]
                    day["temp"] = temp_by_date.get(date_key, {})
                    break
            if "temp" not in day:
                day["temp"] = {}

        # 週間予報
        weekly_ts   = weekly.get("timeSeries", [])
        wk_weather  = weekly_ts[0] if len(weekly_ts) > 0 else {}
        wk_temp     = weekly_ts[1] if len(weekly_ts) > 1 else {}

        wk_times    = wk_weather.get("timeDefines", [])
        wk_area_w   = get_area_data(wk_weather, KORIYAMA_AREA_CODE)
        wk_area_t   = get_area_data(wk_temp,    KORIYAMA_AREA_CODE)

        wk_codes    = wk_area_w.get("weatherCodes", [])
        wk_pops     = wk_area_w.get("pops",         [])
        wk_reliabilities = wk_area_w.get("reliabilities", [])
        wk_temps_min = wk_area_t.get("tempsMin",    [])
        wk_temps_max = wk_area_t.get("tempsMax",    [])

        weekly_days = []
        for i, t in enumerate(wk_times):
            weekly_days.append({
                "date":        fmt_date(t),
                "code":        wk_codes[i]           if i < len(wk_codes)    else "",
                "pop":         wk_pops[i]            if i < len(wk_pops)     else "",
                "reliability": wk_reliabilities[i]   if i < len(wk_reliabilities) else "",
                "temp_min":    wk_temps_min[i]        if i < len(wk_temps_min) else "",
                "temp_max":    wk_temps_max[i]        if i < len(wk_temps_max) else "",
            })

        return {
            "overview":  overview,
            "days":      days,
            "weekly":    weekly_days,
            "timestamp": timestamp,
            "error":     None,
        }

    except requests.Timeout:
        return {"overview":"","days":[],"weekly":[],"timestamp":timestamp,"error":"タイムアウト"}
    except requests.ConnectionError:
        return {"overview":"","days":[],"weekly":[],"timestamp":timestamp,"error":"接続エラー"}
    except Exception as e:
        return {"overview":"","days":[],"weekly":[],"timestamp":timestamp,"error":str(e)}


# ─────────────────────────────────────────
# PDF出力（印刷用タイムライン）
# ─────────────────────────────────────────
def _find_japanese_font() -> tuple[str, str]:
    """
    OS問わず利用可能な日本語フォントパスを返す。
    戻り値: (通常フォントパス, 太字フォントパス)
    優先順: Windows(Meiryo/Yu Gothic) → IPA → Noto(TTF) → 見つからない場合は空文字
    """
    import os, platform
    candidates = []
    if platform.system() == "Windows":
        win_fonts = os.environ.get("WINDIR", "C:\\Windows") + "\\Fonts\\"
        candidates = [
            # Yu Gothic
            (win_fonts + "yugothic.ttf",  win_fonts + "yugothicb.ttf"),
            (win_fonts + "YuGothR.ttc",   win_fonts + "YuGothB.ttc"),
            # Meiryo
            (win_fonts + "meiryo.ttc",    win_fonts + "meiryob.ttc"),
            # MS Gothic
            (win_fonts + "msgothic.ttc",  win_fonts + "msgothic.ttc"),
        ]
    else:
        candidates = [
            ('/usr/share/fonts/opentype/ipafont-gothic/ipag.ttf',
             '/usr/share/fonts/opentype/ipafont-gothic/ipagp.ttf'),
            ('/usr/share/fonts/truetype/fonts-japanese-gothic.ttf',
             '/usr/share/fonts/truetype/fonts-japanese-gothic.ttf'),
        ]
    for reg, bold in candidates:
        if os.path.exists(reg):
            return reg, (bold if os.path.exists(bold) else reg)
    return "", ""


FONT_PATH, FONT_PATH_BOLD = _find_japanese_font()

try:
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.lib.pagesizes import A4
    from reportlab.platypus import (
        SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
    )
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.lib import colors as rl_colors
    from reportlab.lib.units import mm
    import io as _io

    if not FONT_PATH:
        raise FileNotFoundError("日本語フォントが見つかりません")

    pdfmetrics.registerFont(TTFont('IPAGothic',  FONT_PATH))
    pdfmetrics.registerFont(TTFont('IPAGothicP', FONT_PATH_BOLD))
    REPORTLAB_OK = True
except Exception as _rl_err:
    REPORTLAB_OK = False
    _REPORTLAB_ERR = str(_rl_err)


# フェーズ色（HEX→reportlab Color変換）
def _hex_to_rl(hex_color: str):
    from reportlab.lib import colors as c
    h = hex_color.lstrip("#")
    r, g, b = int(h[0:2],16)/255, int(h[2:4],16)/255, int(h[4:6],16)/255
    return c.Color(r, g, b)


CONDITION_LABELS_SHORT = {
    "all":         "",
    "has_elderly": "【高齢者等】",
    "has_car":     "【車避難】",
}


def build_timeline_pdf(
    tasks: list,
    has_elderly: bool,
    has_car: bool,
    selected_phases: list | None = None,
) -> bytes | None:
    """
    マイ・タイムラインのPDFを生成して bytes で返す。
    selected_phases が None の場合は全フェーズを出力。
    """
    if not REPORTLAB_OK:
        return None

    buf = _io.BytesIO()
    doc = SimpleDocTemplate(
        buf, pagesize=A4,
        leftMargin=15*mm, rightMargin=15*mm,
        topMargin=12*mm, bottomMargin=12*mm,
        title="郡山市マイ・タイムライン",
    )

    # スタイル定義
    s_title = ParagraphStyle("s_title", fontName="IPAGothicP", fontSize=16,
                              spaceAfter=2*mm, textColor=rl_colors.HexColor("#1a237e"))
    s_sub   = ParagraphStyle("s_sub",   fontName="IPAGothic",  fontSize=8,
                              spaceAfter=4*mm, textColor=rl_colors.grey)
    s_phase = ParagraphStyle("s_phase", fontName="IPAGothicP", fontSize=10,
                              textColor=rl_colors.white, leading=14)
    s_task  = ParagraphStyle("s_task",  fontName="IPAGothic",  fontSize=9,
                              leading=14, leftIndent=4*mm)
    s_empty = ParagraphStyle("s_empty", fontName="IPAGothic",  fontSize=8,
                              textColor=rl_colors.grey, leftIndent=4*mm)
    s_foot  = ParagraphStyle("s_foot",  fontName="IPAGothic",  fontSize=7,
                              textColor=rl_colors.grey)

    story = []

    # タイトル
    story.append(Paragraph("郡山市 マイ・タイムライン（印刷用）", s_title))
    attrs = []
    if has_elderly: attrs.append("高齢者・乳幼児がいる世帯")
    if has_car:     attrs.append("車で避難する世帯")
    attr_str = "　".join(attrs) if attrs else "一般世帯"
    story.append(Paragraph(
        f"出力日時：{datetime.now().strftime('%Y年%m月%d日 %H:%M')}　対象：{attr_str}",
        s_sub
    ))
    story.append(HRFlowable(width="100%", thickness=1,
                             color=rl_colors.HexColor("#1a237e"), spaceAfter=3*mm))

    phases_to_print = selected_phases if selected_phases else SIM_PHASES

    for phase in phases_to_print:
        # フェーズヘッダー（色帯）
        phase_color = _hex_to_rl(PHASE_COLORS.get(phase, "#607d8b"))
        phase_table = Table(
            [[Paragraph(phase, s_phase)]],
            colWidths=[180*mm],
        )
        phase_table.setStyle(TableStyle([
            ("BACKGROUND", (0,0), (-1,-1), phase_color),
            ("TOPPADDING",    (0,0), (-1,-1), 3),
            ("BOTTOMPADDING", (0,0), (-1,-1), 3),
            ("LEFTPADDING",   (0,0), (-1,-1), 6),
            ("ROUNDEDCORNERS", [4]),
        ]))
        story.append(phase_table)
        story.append(Spacer(1, 1.5*mm))

        # タスク一覧
        phase_tasks = [
            t for t in tasks
            if t["phase"] == phase and (
                t["condition"] == "all"
                or (t["condition"] == "has_car"     and has_car)
                or (t["condition"] == "has_elderly" and has_elderly)
            )
        ]

        if phase_tasks:
            for t in phase_tasks:
                prefix = CONDITION_LABELS_SHORT.get(t["condition"], "")
                # チェックボックス□ + テキスト
                story.append(Paragraph(f"□　{prefix}{t['text']}", s_task))
        else:
            story.append(Paragraph("（このフェーズに該当タスクはありません）", s_empty))

        story.append(Spacer(1, 3*mm))

    # フッター
    story.append(HRFlowable(width="100%", thickness=0.5,
                             color=rl_colors.grey, spaceBefore=2*mm))
    story.append(Paragraph(
        "■ 緊急連絡先　災害用伝言ダイヤル：171　　"
        "郡山市防災：024-924-2231　　消防・救急：119　　警察：110",
        s_foot
    ))
    story.append(Paragraph(
        "■ 情報確認先　福島県河川情報：kaseninf.pref.fukushima.jp　　"
        "郡山市防災情報：city.koriyama.lg.jp/site/bosai/",
        s_foot
    ))

    doc.build(story)
    return buf.getvalue()


# ─────────────────────────────────────────
# ユーティリティ：フェーズ色帯
# ─────────────────────────────────────────
def phase_badge(phase: str, lang: str = "ja") -> None:
    color = PHASE_COLORS.get(phase, "#607d8b")
    # 白文字が読みやすい色かどうかで文字色を切り替え
    dark_phases = ["平時（備えの期間）", "台風上陸の3日前（準備開始）"]
    text_color = "#1a237e" if phase in dark_phases else "white"
    bg = color if phase not in dark_phases else "#e8eaf6"
    label = tr_phase(lang, phase)
    prefix = tr(lang, "current_phase")
    st.markdown(
        f'<div style="background:{bg};padding:10px 18px;border-radius:8px;'
        f'color:{text_color};font-size:0.95rem;font-weight:600;'
        f'letter-spacing:0.02em;margin:8px 0;border-left:4px solid {color};">'
        f'{prefix}{label}</div>',
        unsafe_allow_html=True,
    )


def water_gauge(level: float, max_level: float = 11.0,
                thresholds_override: list | None = None,
                label: str = "現在水位") -> None:
    """簡易水位ゲージを描画。thresholds_override で基準水位を上書き可能。"""
    thresholds = thresholds_override or [
        (4.00, "待機水位",   "#ff9800"),
        (5.50, "氾濫注意",   "#ff5722"),
        (5.70, "避難判断",   "#f44336"),
        (6.80, "氾濫危険",   "#9c27b0"),
        (10.01,"台風最大値", "#212121"),
    ]
    cur_pct = min(level / max_level * 100, 100)

    lines = ""
    for thr, thr_label, col in thresholds:
        pct = thr / max_level * 100
        lines += (
            f'<div style="position:absolute;left:{pct:.1f}%;top:0;bottom:0;'
            f'border-left:2px dashed {col};z-index:2;"></div>'
            f'<div style="position:absolute;left:{pct:.1f}%;top:-18px;'
            f'font-size:0.58rem;color:{col};white-space:nowrap;">{thr_label}</div>'
        )

    gauge = (
        '<div style="position:relative;margin-top:22px;">'
        f'<div style="background:#e0e0e0;border-radius:6px;height:28px;position:relative;">'
        f'<div style="background:#2196f3;height:100%;width:{cur_pct:.1f}%;'
        f'border-radius:6px 0 0 6px;"></div>'
        f'{lines}'
        f'</div></div>'
    )
    st.markdown(gauge, unsafe_allow_html=True)
    st.caption(f"青バー = {label} {level:.2f} m")


# ─────────────────────────────────────────
# メインコンテンツ：モード分岐
# ─────────────────────────────────────────
phase = SIM_PHASES[0]

# ══════════════════════════════════════════
# 通常モード
# ══════════════════════════════════════════
if mode == "通常（手動選択）":
    phase = st.radio(
        tr(lang, "select_phase"),
        SIM_PHASES,
        format_func=lambda p: tr_phase(lang, p),
    )

# ══════════════════════════════════════════
# リアルタイム水位連携
# ══════════════════════════════════════════
elif mode == "📡 リアルタイム水位連携":

    # ── 気象庁警報パネル（常に最上部に表示）────────────────
    jma = get_jma_warning()
    with st.container():
        st.subheader(tr(lang, "weather_warning_header"))
        if jma["error"]:
            st.warning(f"⚠️ {tr(lang, 'fetch_failed')}：{jma['error']}")
        elif not jma["alerts"]:
            st.success(tr(lang, "no_warnings"))
        else:
            # 発令中の警報をバッジ表示（原文＋自動翻訳リンク）
            badges = "　".join([
                f'<span style="background:{PHASE_COLORS.get(JMA_ALERT_PHASE.get(a,""), "#607d8b")};'
                f'color:white;padding:4px 10px;border-radius:4px;font-weight:bold;'
                f'font-size:0.9rem;">{a}</span>'
                for a in jma["alerts"]
            ])
            st.markdown(badges, unsafe_allow_html=True)

            if lang != "ja":
                gt_links = "　".join([
                    f"[{a} → {LANGUAGES.get(lang,'')}]({google_translate_url(a, lang)})"
                    for a in jma["alerts"]
                ])
                st.caption(f"{tr(lang, 'google_translate_note')}：{gt_links}")

            # 警報に対応するフェーズを自動提案
            if jma["phase"]:
                phase_label = tr_phase(lang, jma["phase"])
                arrow_text = (
                    f"⚡ {tr(lang,'current_phase')}{phase_label}"
                    if lang != "ja"
                    else f"⚡ 警報から判定されるフェーズ：{phase_label}"
                )
                st.markdown(
                    f'<div style="background:{jma["color"]};padding:10px 18px;'
                    f'border-radius:8px;color:white;font-weight:bold;margin:8px 0;">'
                    f'{arrow_text}</div>',
                    unsafe_allow_html=True,
                )
                # 水位取得失敗時に警報フェーズを自動適用するかを選択
                if st.button("🔗 このフェーズをタイムラインに適用する", key="apply_jma_phase"):
                    st.session_state["manual_phase_override"] = jma["phase"]
                    st.rerun()

        st.caption(f"気象庁データ取得時刻：{jma['timestamp']}　更新間隔：5分")
        st.markdown("---")

    # BeautifulSoup チェック
    if not BS4_AVAILABLE:
        st.error(
            "⚠️ `beautifulsoup4` がインストールされていません。\n\n"
            "ターミナルで以下を実行してください：\n```\npip install beautifulsoup4\n```"
        )
        phase = st.radio("手動でフェーズを選択（暫定）：", SIM_PHASES, key="no_bs4_phase")
    else:
        result = get_water_level()

        # ── 取得成功 ────────────────────────────────
        if result["level"] is not None:
            level = result["level"]
            phase = level_to_phase(level)

            # フォールバック使用時は注意表示
            if result["fallback_used"]:
                st.warning(
                    f"⚠️ 第1ソース取得失敗。フォールバックソース「{result['source']}」を使用中です。"
                )

            # ── 河川切り替えラジオボタン ──────────────────────
            river_choice = st.radio(
                tr(lang, "river_select"),
                ["🌊 阿武隈川本川（阿久津観測所）", "🏘️ 逢瀬川・備前舘地区（御代田観測所）"],
                horizontal=True,
                key="river_select",
            )

            st.markdown("---")

            # ▼ 阿武隈川表示
            if river_choice == "🌊 阿武隈川本川（阿久津観測所）":
                st.subheader("🌊 阿武隈川本川")
                st.caption(f"観測局：{result['station']}　郡山市の洪水予報基準観測所")

                m1, m2, m3 = st.columns(3)
                m1.metric(tr(lang, "current_water_level"), f"{level:.2f} m")
                m2.metric("判定フェーズ", phase.split(" (")[0])
                m3.metric("取得時刻", result["timestamp"])

                water_gauge(level, label="阿武隈川水位")
                phase_badge(phase, lang)
                st.caption(
                    f"データソース：[{result['source']}]({result['source_url']})"
                )

            # ▼ 逢瀬川（備前舘地区）表示
            else:
                st.subheader("🏘️ 逢瀬川（備前舘地区）")
                ose = get_osegawa_level()

                if ose["level"] is not None:
                    ose_level = ose["level"]
                    ose_alert, ose_color = osegawa_level_to_alert(ose_level)

                    st.caption(f"観測局：{ose['station']}　逢瀬川左岸・備前舘地区近傍")

                    om1, om2, om3 = st.columns(3)
                    om1.metric(tr(lang, "current_water_level"), f"{ose_level:.2f} m")
                    om2.metric("警戒段階", ose_alert.split(" ")[0])
                    om3.metric("取得時刻", ose["timestamp"])

                    thr = OSEGAWA_THRESHOLDS
                    water_gauge(
                        ose_level,
                        max_level=5.0,
                        thresholds_override=[
                            (thr["水防団待機"], "待機水位", "#ff9800"),
                            (thr["氾濫注意"],   "氾濫注意", "#ff5722"),
                            (thr["避難判断"],   "避難判断", "#f44336"),
                            (thr["氾濫危険"],   "氾濫危険", "#9c27b0"),
                        ],
                        label="逢瀬川水位",
                    )

                    # 警戒バッジ
                    st.markdown(
                        f'<div style="background:{ose_color};padding:10px 18px;'
                        f'border-radius:8px;color:white;font-weight:bold;'
                        f'font-size:1rem;margin:8px 0;">'
                        f'逢瀬川（備前舘地区）：{ose_alert}</div>',
                        unsafe_allow_html=True,
                    )

                    # 備前舘地区向け行動メッセージ
                    if ose_level >= thr["避難判断"]:
                        st.error("🚨 備前舘地区：逢瀬川が避難判断水位を超えています。直ちに避難を開始してください。")
                    elif ose_level >= thr["氾濫注意"]:
                        st.warning("⚠️ 備前舘地区：逢瀬川が氾濫注意水位を超えています。避難の準備を始めてください。")
                    elif ose_level >= thr["水防団待機"]:
                        st.info("🔶 備前舘地区：逢瀬川が水防団待機水位を超えています。引き続き情報に注意してください。")
                    else:
                        st.success("✅ 備前舘地区：逢瀬川は現在通常水位です。")

                    st.caption(
                        f"データソース：[{ose['source']}]({ose['source_url']})"
                    )

                else:
                    st.warning(f"⚠️ 逢瀬川の水位を取得できませんでした。\n原因：{ose['error']}")
                    st.markdown(
                        "直接確認 → [福島県河川情報システム](https://kaseninf.pref.fukushima.jp/)"
                    )
                    if st.button("🔄 再取得", key="ose_retry"):
                        st.cache_data.clear()
                        st.rerun()

        # ── 全ソース失敗 ─────────────────────────────
        else:
            st.error("❌ すべてのデータソースからの水位取得に失敗しました")

            with st.expander("🔍 エラー詳細（クリックで展開）", expanded=True):
                st.code(result["error"], language=None)
                st.markdown("""
**考えられる原因：**
- サーバーが一時的に停止中（メンテナンス・障害）
- ネットワーク接続の問題
- スクレイピング対象ページの構造変更
- `beautifulsoup4` がインストールされていない

**対処方法：**
1. 5分後に「🔄 再取得を試みる」を押す
2. 手動フォールバックモードで操作を継続する
3. 直接サイトを確認 → [福島県河川情報システム](https://kaseninf.pref.fukushima.jp/)
                """)

            col_retry, col_manual = st.columns([1, 3])
            with col_retry:
                if st.button("🔄 再取得を試みる"):
                    st.cache_data.clear()
                    st.rerun()

            st.markdown("---")
            st.subheader("🖐️ 手動フォールバック")
            st.info(
                "水位データを取得できないため、現在の状況を手動で選択してください。"
                "データ取得が復旧次第、自動で切り替わります（5分キャッシュ）。"
            )

            # 水位を数値入力して自動判定する補助UI
            with st.expander("💧 水位（m）を直接入力してフェーズを自動判定"):
                manual_level = st.number_input(
                    "水位を入力（m）", min_value=0.0, max_value=15.0,
                    value=0.0, step=0.01, format="%.2f",
                    help="サイトで確認した水位を入力するとフェーズを自動判定します"
                )
                if manual_level > 0:
                    auto_phase = level_to_phase(manual_level)
                    st.success(f"判定フェーズ：**{auto_phase}**")
                    if st.button("このフェーズを適用する"):
                        phase = auto_phase
                        st.session_state["manual_phase_override"] = phase
                        st.rerun()

            # セッションに保存されたフェーズがあれば使う
            if "manual_phase_override" in st.session_state:
                phase = st.session_state["manual_phase_override"]
                st.success(f"✅ 手動設定フェーズ「{phase}」を適用中")
            else:
                phase = st.radio(
                    "フェーズを選択：",
                    SIM_PHASES,
                    key="fallback_phase_radio",
                )

    # データソース情報パネル
    st.markdown("---")
    with st.expander("📡 データソース・取得仕様"):
        st.markdown(f"""
| 優先順位 | ソース | URL | 取得方法 | 対象 |
|:---:|---|---|:---:|---|
| **1** | 福島県河川流域総合情報システム | `kaseninf.pref.fukushima.jp` | HTMLスクレイプ | 阿久津(国)・御代田(国) |
| **2** | 国交省 福島河川国道事務所 | `thr.mlit.go.jp/fukushima` | HTMLスクレイプ | 郡山（フォールバック） |
| **3** | 気象庁 警報・注意報JSON | `www.jma.go.jp/bosai/warning` | **JSON API（無料・公式）** | 郡山市（全警報種別） |

> **気象庁API** = 公式・無料・認証不要。5分ごとに更新。水位取得失敗時のフェーズ判定バックアップとして機能。
> **bs4インストール確認** = `{"✅ 利用可能" if BS4_AVAILABLE else "❌ 未インストール"}`
        """)

# ══════════════════════════════════════════
# 🌤️ 郡山市天気モード
# ══════════════════════════════════════════
if mode == "🌤️ 郡山市天気":
    st.header(tr(lang, "mode_weather"))

    # ══ AMeDAS 実況パネル（郡山限定） ═══════════════════════
    st.subheader(tr(lang, "weather_realtime_panel"))
    amd = get_koriyama_amedas()

    if amd.get("error"):
        st.warning(f"⚠️ AMeDASデータ取得失敗：{amd['error']}")
        if st.button("🔄 再取得", key="amedas_retry"):
            st.cache_data.clear()
            st.rerun()
    else:
        # 実況メトリクスを横並びで表示
        c1, c2, c3, c4, c5 = st.columns(5)

        def _fmt(val, unit, decimals=1):
            return f"{val:.{decimals}f} {unit}" if val is not None else "--"

        c1.metric(tr(lang, "temperature"),     _fmt(amd["temp"], "℃"))
        c2.metric(tr(lang, "precipitation_1h"), _fmt(amd["precipitation1h"], "mm"))
        c3.metric(tr(lang, "wind_speed"),       _fmt(amd["wind"], "m/s"))
        c4.metric(tr(lang, "wind_direction"),   amd["wind_dir"] or "--")
        c5.metric(tr(lang, "humidity"),         _fmt(amd["humidity"], "%", 0))

        # 10分降水量・気圧を補助表示
        sub_cols = st.columns(3)
        sub_cols[0].caption(f"10分降水量：{_fmt(amd['precipitation10m'], 'mm')}")
        sub_cols[1].caption(f"現地気圧：{_fmt(amd['pressure'], 'hPa', 1)}")
        sub_cols[2].caption(f"観測時刻：{amd['obs_time']}　（郡山AMeDAS / 観測所コード：{KORIYAMA_AMEDAS_CODE}）")

        # 1時間降水量による雨の強さ表示
        prec = amd.get("precipitation1h")
        if prec is not None:
            if prec >= 50:
                st.error(f"🚨 非常に激しい雨：{prec}mm/h　土砂災害・河川氾濫に警戒！")
            elif prec >= 30:
                st.warning(f"⛈️ 激しい雨：{prec}mm/h　河川水位の上昇に注意！")
            elif prec >= 10:
                st.info(f"🌧️ やや強い雨：{prec}mm/h")
            elif prec > 0:
                st.info(f"🌦️ 弱い雨：{prec}mm/h")

    st.markdown("---")
    st.caption("以下は中通り地方（郡山市含む）の天気予報です。")

    fc = get_jma_forecast()

    if fc["error"]:
        st.error(f"⚠️ 天気データの取得に失敗しました：{fc['error']}")
        if st.button("🔄 再取得"):
            st.cache_data.clear()
            st.rerun()
    else:
        # ── 今日〜明後日カード ──────────────────────────
        st.subheader("📅 今後3日間の天気")
        days = fc.get("days", [])
        if days:
            cols = st.columns(len(days))
            for col, day in zip(cols, days):
                emoji  = _weather_emoji(day.get("code", ""))
                t_min  = day["temp"].get("min", "--")
                t_max  = day["temp"].get("max", "--")
                pops   = day.get("pops", [])
                pop_str = "／".join([f"{p}%" for p in pops if p != ""]) or "--"
                weather_short = day.get("weather", "").replace("\u3000", " ")[:20]

                col.markdown(
                    f'<div style="background:#ffffff;border:1px solid #e8eaf6;'
                    f'border-radius:10px;padding:14px 10px;text-align:center;'
                    f'box-shadow:0 1px 4px rgba(0,0,0,0.06);">'
                    f'<div style="font-weight:600;font-size:0.9rem;color:#546e7a;">{day["date"]}</div>'
                    f'<div style="font-size:2.4rem;margin:6px 0;">{emoji}</div>'
                    f'<div style="font-size:0.72rem;color:#78909c;margin-bottom:8px;min-height:2.5em;">{weather_short}</div>'
                    f'<div style="font-size:0.95rem;font-weight:600;">'
                    f'<span style="color:#e53935;">{t_max}°</span>'
                    f'<span style="color:#bdbdbd;margin:0 3px;">/</span>'
                    f'<span style="color:#1e88e5;">{t_min}°</span></div>'
                    f'<div style="font-size:0.8rem;color:#5c6bc0;margin-top:4px;">☔ {pop_str}</div>'
                    f'</div>',
                    unsafe_allow_html=True,
                )
                # 風
                wind = day.get("wind", "")
                if wind:
                    col.caption(f"🌬️ {wind[:30]}")

        st.markdown("---")

        # ── 週間予報テーブル ───────────────────────────
        st.subheader("📆 週間天気予報（中通り）")
        weekly = fc.get("weekly", [])
        if weekly:
            header_cols = st.columns(len(weekly))
            for col, day in zip(header_cols, weekly):
                emoji   = _weather_emoji(day.get("code",""))
                t_min   = day.get("temp_min","--")
                t_max   = day.get("temp_max","--")
                pop     = day.get("pop","--")
                rel     = day.get("reliability","")
                rel_html = f'<div style="font-size:0.68rem;color:#bdbdbd;">{rel}</div>' if rel else ""
                col.markdown(
                    f'<div style="background:#ffffff;border:1px solid #e8eaf6;'
                    f'border-radius:8px;padding:10px 6px;text-align:center;'
                    f'box-shadow:0 1px 3px rgba(0,0,0,0.05);">'
                    f'<div style="font-weight:600;font-size:0.78rem;color:#546e7a;">{day["date"]}</div>'
                    f'<div style="font-size:1.6rem;margin:4px 0;">{emoji}</div>'
                    f'<div style="font-size:0.78rem;font-weight:600;">'
                    f'<span style="color:#e53935;">{t_max}°</span>'
                    f'<span style="color:#bdbdbd;margin:0 2px;">/</span>'
                    f'<span style="color:#1e88e5;">{t_min}°</span></div>'
                    f'<div style="font-size:0.72rem;color:#5c6bc0;">☔{pop}%</div>'
                    f'{rel_html}'
                    f'</div>',
                    unsafe_allow_html=True,
                )

        st.markdown("---")

        # ── 天気概況テキスト ──────────────────────────
        st.subheader("📝 天気概況")
        overview = fc.get("overview","")
        if overview:
            st.info(overview)
        else:
            st.caption("概況テキストはありません。")

        # ── 警報・注意報（再掲） ──────────────────────
        st.markdown("---")
        st.subheader(tr(lang, "weather_warning_header"))
        jma_w = get_jma_warning()
        if jma_w["error"]:
            st.warning(f"{tr(lang,'fetch_failed')}：{jma_w['error']}")
        elif not jma_w["alerts"]:
            st.success(tr(lang, "no_warnings"))
        else:
            badges = "　".join([
                f'<span style="background:{PHASE_COLORS.get(JMA_ALERT_PHASE.get(a,""),"#607d8b")};'
                f'color:white;padding:4px 10px;border-radius:4px;font-weight:bold;">{a}</span>'
                for a in jma_w["alerts"]
            ])
            st.markdown(badges, unsafe_allow_html=True)

        st.caption(
            f"データ取得時刻：{fc['timestamp']}　"
            f"[気象庁 天気予報](https://www.jma.go.jp/bosai/forecast/#area_type=offices&area_code=070000)"
        )

        if st.button("🔄 天気情報を更新"):
            st.cache_data.clear()
            st.rerun()

# ══════════════════════════════════════════
# タスク管理モード
# ══════════════════════════════════════════
CONDITION_LABELS = {
    "all":         "全員",
    "has_elderly": "高齢者・乳幼児がいる世帯",
    "has_car":     "車で避難する世帯",
}

if mode == "✏️ タスク管理":
    st.header("✏️ マイ・タイムライン タスク管理")
    st.info("ここで追加・編集したタスクは tasks.json に保存され、次回起動時も反映されます。")

    tab_add, tab_edit, tab_export = st.tabs(["➕ タスク追加", "📝 編集・削除", "📤 エクスポート"])

    # ── タスク追加タブ ────────────────────────────────────
    with tab_add:
        st.subheader("新しいタスクを追加")
        col1, col2 = st.columns(2)
        with col1:
            new_phase = st.selectbox(
                "フェーズ *",
                SIM_PHASES,
                key="new_phase",
            )
        with col2:
            new_condition = st.selectbox(
                "対象条件 *",
                list(CONDITION_LABELS.keys()),
                format_func=lambda k: CONDITION_LABELS[k],
                key="new_condition",
            )
        new_text = st.text_area(
            "タスク内容 *",
            placeholder="例：避難経路の安全を確認して出発する",
            key="new_text",
            height=80,
        )

        if st.button("➕ 追加する", type="primary", key="btn_add"):
            if new_text.strip() == "":
                st.error("タスク内容を入力してください。")
            else:
                new_task = {
                    "phase":     new_phase,
                    "condition": new_condition,
                    "text":      new_text.strip(),
                }
                st.session_state.all_tasks.append(new_task)
                save_tasks(st.session_state.all_tasks)
                st.success(f"✅ タスクを追加しました：「{new_text.strip()}」")
                st.rerun()

    # ── 編集・削除タブ ────────────────────────────────────
    with tab_edit:
        st.subheader("既存タスクの編集・削除")

        # フェーズで絞り込み
        filter_phase = st.selectbox(
            "フェーズで絞り込み",
            ["すべて"] + SIM_PHASES,
            key="edit_filter_phase",
        )

        tasks = st.session_state.all_tasks
        display_tasks = [
            (i, t) for i, t in enumerate(tasks)
            if filter_phase == "すべて" or t["phase"] == filter_phase
        ]

        if not display_tasks:
            st.info("このフェーズにタスクはありません。")
        else:
            st.caption(f"{len(display_tasks)} 件表示中")

            # 削除予定インデックスを管理
            if "delete_confirm" not in st.session_state:
                st.session_state.delete_confirm = None

            for idx, (orig_i, task) in enumerate(display_tasks):
                cond_label = CONDITION_LABELS.get(task["condition"], task["condition"])
                with st.expander(
                    f"[{task['phase']}]　{cond_label}　｜　{task['text'][:30]}{'…' if len(task['text']) > 30 else ''}",
                    expanded=False,
                ):
                    col_f, col_c = st.columns(2)
                    with col_f:
                        # フェーズ名がSIM_PHASESにない場合は先頭を選択
                        phase_index = (
                            SIM_PHASES.index(task["phase"])
                            if task["phase"] in SIM_PHASES else 0
                        )
                        # タスクのフェーズが既存リストにない場合は警告表示
                        if task["phase"] not in SIM_PHASES:
                            st.warning(f"⚠️ 未知のフェーズ名：「{task['phase']}」→ 先頭フェーズに補正しました")
                        edit_phase = st.selectbox(
                            "フェーズ",
                            SIM_PHASES,
                            index=phase_index,
                            key=f"ep_{orig_i}",
                        )
                    with col_c:
                        cond_keys = list(CONDITION_LABELS.keys())
                        edit_condition = st.selectbox(
                            "対象条件",
                            cond_keys,
                            format_func=lambda k: CONDITION_LABELS[k],
                            index=cond_keys.index(task["condition"]) if task["condition"] in cond_keys else 0,
                            key=f"ec_{orig_i}",
                        )
                    edit_text = st.text_area(
                        "タスク内容",
                        value=task["text"],
                        key=f"et_{orig_i}",
                        height=80,
                    )

                    col_save, col_del = st.columns([1, 1])
                    with col_save:
                        if st.button("💾 保存", key=f"save_{orig_i}"):
                            if edit_text.strip() == "":
                                st.error("タスク内容を入力してください。")
                            else:
                                st.session_state.all_tasks[orig_i] = {
                                    "phase":     edit_phase,
                                    "condition": edit_condition,
                                    "text":      edit_text.strip(),
                                }
                                save_tasks(st.session_state.all_tasks)
                                st.success("✅ 保存しました")
                                st.rerun()
                    with col_del:
                        if st.session_state.delete_confirm == orig_i:
                            st.warning("本当に削除しますか？")
                            cc1, cc2 = st.columns(2)
                            with cc1:
                                if st.button("🗑️ 削除確定", key=f"delok_{orig_i}"):
                                    st.session_state.all_tasks.pop(orig_i)
                                    save_tasks(st.session_state.all_tasks)
                                    st.session_state.delete_confirm = None
                                    st.success("🗑️ 削除しました")
                                    st.rerun()
                            with cc2:
                                if st.button("キャンセル", key=f"delcancel_{orig_i}"):
                                    st.session_state.delete_confirm = None
                                    st.rerun()
                        else:
                            if st.button("🗑️ 削除", key=f"del_{orig_i}"):
                                st.session_state.delete_confirm = orig_i
                                st.rerun()

    # ── エクスポートタブ ──────────────────────────────────
    with tab_export:
        st.subheader("📄 印刷用タイムライン（PDF出力）")

        if not REPORTLAB_OK:
            st.error(
                "⚠️ PDF生成ライブラリの初期化に失敗しました。\n\n"
                f"原因：`{_REPORTLAB_ERR}`"
            )
            st.info("コマンドプロンプトで以下を実行後、アプリを再起動してください：\n"
                    "```\npython -m pip install reportlab\n```")
        else:
            st.info("現在のタスク設定をA4一枚にまとめたPDFを出力します。印刷して手元に置いてください。")

            col_a, col_b = st.columns(2)
            with col_a:
                pdf_elderly = st.checkbox("高齢者・乳幼児がいる世帯として出力", value=has_elderly)
            with col_b:
                pdf_car = st.checkbox("車で避難する世帯として出力", value=has_car)

            pdf_phases = st.multiselect(
                "出力するフェーズを選択（未選択=全フェーズ）",
                SIM_PHASES,
                default=[],
                key="pdf_phases",
            )

            if st.button("📄 PDFを生成する", type="primary"):
                with st.spinner("PDF生成中..."):
                    phases = pdf_phases if pdf_phases else None
                    pdf_bytes = build_timeline_pdf(
                        st.session_state.all_tasks,
                        pdf_elderly, pdf_car,
                        selected_phases=phases,
                    )
                if pdf_bytes:
                    fname = f"koriyama_timeline_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf"
                    st.download_button(
                        label="⬇️ PDFをダウンロード",
                        data=pdf_bytes,
                        file_name=fname,
                        mime="application/pdf",
                        type="primary",
                    )
                    st.success("✅ PDF生成完了！「PDFをダウンロード」ボタンで保存してください。")
                else:
                    st.error("PDF生成に失敗しました。")

        st.markdown("---")
        st.subheader("📤 タスクデータのエクスポート／リセット")

        # JSONダウンロード
        export_json = json.dumps(st.session_state.all_tasks, ensure_ascii=False, indent=2)
        st.download_button(
            label="📥 tasks.json をダウンロード",
            data=export_json.encode("utf-8"),
            file_name="tasks.json",
            mime="application/json",
        )

        st.markdown("---")

        # ── 行動記録（action_log.json）────────────────
        st.subheader("📋 チェック済みタスクの記録")
        log_data = load_log()

        if not log_data:
            st.info("まだ記録がありません。タイムライン画面でタスクをチェックして「📝 チェック内容を記録する」ボタンを押すと記録されます。")
        else:
            st.caption(f"記録件数：{len(log_data)} 件　保存先：action_log.json")

            # 記録一覧を新しい順に表示
            for entry in reversed(log_data):
                ts    = entry.get("timestamp", "")
                ph    = entry.get("phase", "")
                tasks = entry.get("tasks", [])
                md    = entry.get("mode", "")
                color = PHASE_COLORS.get(ph, "#607d8b")
                with st.expander(f"🕐 {ts}　｜　{ph}　（{len(tasks)}件）"):
                    st.markdown(
                        f'<span style="background:{color};color:white;padding:2px 8px;'
                        f'border-radius:4px;font-size:0.85rem;">{ph}</span>'
                        f'　モード：{md}',
                        unsafe_allow_html=True,
                    )
                    for t in tasks:
                        st.markdown(f"- ✅ {t}")

            # 記録のダウンロード
            log_json = json.dumps(log_data, ensure_ascii=False, indent=2)
            col_dl, col_clear = st.columns(2)
            with col_dl:
                st.download_button(
                    label="📥 記録をダウンロード（JSON）",
                    data=log_json.encode("utf-8"),
                    file_name=f"action_log_{datetime.now().strftime('%Y%m%d')}.json",
                    mime="application/json",
                )
            with col_clear:
                with st.expander("🗑️ 記録をすべて削除"):
                    st.warning("すべての記録が消えます。元に戻せません。")
                    if st.button("🗑️ 記録を削除する", key="clear_log"):
                        save_log([])
                        st.success("✅ 記録を削除しました。")
                        st.rerun()

        st.markdown("---")
        st.caption(f"現在のタスク総数：{len(st.session_state.all_tasks)} 件")

        # 内蔵データへのリセット
        with st.expander("⚠️ 内蔵タスクにリセット（追加・編集内容がすべて消えます）"):
            st.warning("追加・編集したカスタムタスクはすべて削除されます。元に戻せません。")
            if st.button("🔄 内蔵タスクにリセットする", type="secondary"):
                st.session_state.all_tasks = [t.copy() for t in BUILTIN_TASKS]
                save_tasks(st.session_state.all_tasks)
                st.success("✅ 内蔵タスクにリセットしました。")
                st.rerun()

# ─────────────────────────────────────────
# マイ・タイムライン（タスク管理以外のモード共通）
# ─────────────────────────────────────────
if mode not in ("✏️ タスク管理", "🌤️ 郡山市天気"):
    st.markdown("---")
    st.header(tr(lang, "timeline_header"))

    if mode != "📡 リアルタイム水位連携":
        phase_badge(phase, lang)

    filtered_tasks = [
        task["text"]
        for task in all_tasks
        if task["phase"] == phase
        and (
            task["condition"] == "all"
            or (task["condition"] == "has_car"     and has_car)
            or (task["condition"] == "has_elderly" and has_elderly)
        )
    ]

    if filtered_tasks:
        st.write(f"**{tr(lang, 'tasks_for_phase', phase=tr_phase(lang, phase))}**")

        # 多言語対応の注記（原文＋自動翻訳リンク）
        if lang != "ja":
            st.caption(
                f"🇯🇵→{LANGUAGES.get(lang,'')}　"
                f"({tr(lang, 'google_translate_note')}: "
                f"[{LANGUAGES.get(lang,'')}]({google_translate_url(phase, lang)}))"
            )

        checked_texts = []
        for i, task_text in enumerate(filtered_tasks):
            display_text = tr_task(lang, task_text)
            checked = st.checkbox(display_text, key=f"task_{i}_{phase}")
            if checked:
                checked_texts.append(task_text)  # 記録は日本語原文で保存

        completed = len(checked_texts)
        st.progress(
            completed / len(filtered_tasks),
            text=tr(lang, "progress_done", done=completed, total=len(filtered_tasks))
        )

        # 記録保存ボタン
        if checked_texts:
            st.markdown("")
            col_rec, col_info = st.columns([1, 3])
            with col_rec:
                if st.button(tr(lang, "record_button"), type="primary", key="btn_record"):
                    append_log_entry(phase, checked_texts, mode)
                    st.success(
                        tr(lang, "record_saved",
                           count=len(checked_texts),
                           time=datetime.now().strftime('%H:%M'))
                    )
            with col_info:
                st.caption("記録は `action_log.json` に保存されます。「✏️ タスク管理」→「📤 エクスポート」から確認できます。")
    else:
        st.info(tr(lang, "no_tasks"))

# ─────────────────────────────────────────
# フッター
# ─────────────────────────────────────────
st.markdown("---")
with st.expander(tr(lang, "footer_links")):
    if lang == "ja":
        st.markdown("""
- 🌊 [福島県河川流域総合情報システム](https://kaseninf.pref.fukushima.jp/)
- 🗾 [国土交通省 川の防災情報](https://www.river.go.jp/)
- 🏙️ [郡山市 防災情報](https://www.city.koriyama.lg.jp/site/bosai/)
- 🌦️ [気象庁 警報・注意報（福島県）](https://www.jma.go.jp/bosai/warning/#area_type=offices&area_code=070000)
- 📱 **郡山市防災メール登録** を強く推奨します
- ☎️ 災害用伝言ダイヤル: **171**
        """)
    else:
        st.markdown(f"""
- 🌊 [Fukushima River Information System](https://kaseninf.pref.fukushima.jp/)
- 🗾 [MLIT River Disaster Info](https://www.river.go.jp/)
- 🏙️ [Koriyama City Disaster Info](https://www.city.koriyama.lg.jp/site/bosai/)
- 🌦️ [JMA Warnings (Fukushima)](https://www.jma.go.jp/bosai/warning/#area_type=offices&area_code=070000)
- ☎️ Disaster Message Dial: **171** / 🚑 119 / 👮 110
        """)
        st.caption(tr(lang, "emergency_contacts_text"))