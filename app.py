import json
import random
import time
from pathlib import Path

import streamlit as st
from streamlit_autorefresh import st_autorefresh

st.set_page_config(page_title="Word Match | English Game", page_icon="🎯", layout="wide")

DATA = json.loads(Path(__file__).with_name("vocabulary.json").read_text(encoding="utf-8"))

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800;900&display=swap');
html, body, [class*="css"] {font-family:'Nunito',sans-serif;}
.stApp {background:linear-gradient(135deg,#eef4ff 0%,#f8fbff 55%,#eaf2ff 100%);}
.block-container {max-width:1120px;padding-top:1.5rem;}
.hero {background:linear-gradient(120deg,#142d50,#2865a8);padding:28px 32px;border-radius:24px;color:white;margin-bottom:20px;box-shadow:0 12px 30px #173b641c;}
.hero h1 {color:white;font-size:2.3rem;margin:0;font-weight:900;}
.hero p {color:#dceaff;margin:.35rem 0 0 0;}
.metric {background:white;border:1px solid #dce7f4;border-radius:18px;padding:14px 18px;text-align:center;box-shadow:0 5px 18px #173b640b;}
.metric-label {font-size:.82rem;color:#6c7c90;font-weight:800;}
.metric-value {font-size:1.8rem;color:#17375f;font-weight:900;}
.word-card button {min-height:68px!important;border-radius:15px!important;border:1px solid #d6e2f0!important;background:white!important;color:#183657!important;font-weight:800!important;white-space:normal!important;}
.word-card button:hover {border:2px solid #3679bd!important;background:#f0f7ff!important;}
.selected button {background:#e4f1ff!important;border:2px solid #2d70b5!important;}
div.stButton > button[kind="primary"] {background:#2865a8;border-radius:12px;font-weight:800;}
.small-note {color:#718197;font-size:.85rem;text-align:center;}
</style>
""", unsafe_allow_html=True)

def init_state():
    defaults = {
        "screen": "levels", "level": None, "unit_index": None,
        "score": 0, "errors": 0, "correct": 0, "started_at": None,
        "pool": [], "tr_cards": [], "en_cards": [],
        "selected": None, "message": "Choose one Turkish word and one English word.",
        "finished": False, "game_id": 0
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()

def start_game(level, unit_index):
    words = DATA[level][unit_index]["words"][:]
    random.shuffle(words)
    first = words[:12]
    st.session_state.update({
        "screen": "game", "level": level, "unit_index": unit_index,
        "score": 0, "errors": 0, "correct": 0,
        "started_at": time.time(), "pool": words[12:],
        "tr_cards": first[:], "en_cards": first[:],
        "selected": None, "message": "Choose one Turkish word and one English word.",
        "finished": False, "game_id": st.session_state.game_id + 1
    })
    random.shuffle(st.session_state.tr_cards)
    random.shuffle(st.session_state.en_cards)

def elapsed_seconds():
    if st.session_state.started_at is None:
        return 0
    return int(time.time() - st.session_state.started_at)

def finish_game():
    st.session_state.finished = True
    st.session_state.screen = "result"

def choose_card(side, word_id):
    if st.session_state.finished:
        return
    selected = st.session_state.selected
    if selected is None:
        st.session_state.selected = (side, word_id)
        return
    old_side, old_id = selected
    if old_side == side:
        st.session_state.selected = (side, word_id)
        return

    if old_id == word_id:
        st.session_state.score += 50
        st.session_state.correct += 1
        st.session_state.message = "✅ Correct match! +50 points"
        st.session_state.tr_cards = [w for w in st.session_state.tr_cards if w["id"] != word_id]
        st.session_state.en_cards = [w for w in st.session_state.en_cards if w["id"] != word_id]

        if st.session_state.pool:
            new_word = st.session_state.pool.pop()
            st.session_state.tr_cards.append(new_word)
            st.session_state.en_cards.append(new_word)
            random.shuffle(st.session_state.tr_cards)
            random.shuffle(st.session_state.en_cards)

        if st.session_state.correct == 20:
            finish_game()
    else:
        st.session_state.score = max(0, st.session_state.score - 20)
        st.session_state.errors += 1
        st.session_state.message = "❌ Incorrect match! -20 points"
    st.session_state.selected = None

def show_metric(label, value):
    st.markdown(
        f'<div class="metric"><div class="metric-label">{label}</div>'
        f'<div class="metric-value">{value}</div></div>',
        unsafe_allow_html=True
    )

st.markdown('<div class="hero"><h1>🎯 WORD MATCH CHALLENGE</h1><p>Improve Your English Vocabulary!</p><p>Welcome to Word Match Challenge! Choose your level, select a unit and match the English words with their Turkish meanings. Earn 50 points for every correct match and lose 20 points for every incorrect match. Complete all 20 pairs and try to get the highest score!</p></div><div style="text-align:center;margin:8px 0 28px 0;"><div style="font-size:1.15rem;font-weight:900;color:#2865a8;letter-spacing:.04em;">MY FAVOURITE TEACHER</div><div style="font-size:1.55rem;font-weight:900;color:#e04b78;">RÜMEYSA SAĞIN ❤️</div></div>', unsafe_allow_html=True)

if st.session_state.screen == "levels":
    st.markdown("## Choose Your Level")
    st.write("Choose your level first, then select the unit you want to practise.")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("### 📘 Level 1")
        st.caption("WAYMARK YEAR 9 / B1.1")
        if st.button("Explore Level 1 Units", use_container_width=True):
            st.session_state.level = "waymark"
            st.session_state.screen = "units"
            st.rerun()
    with c2:
        st.markdown("### 📗 Level 2")
        st.caption("UPTONE YEAR 9 / B2.1")
        if st.button("Explore Level 2 Units", use_container_width=True):
            st.session_state.level = "uptone"
            st.session_state.screen = "units"
            st.rerun()

elif st.session_state.screen == "units":
    level = st.session_state.level
    st.button("← Back to Levels", on_click=lambda: st.session_state.update(screen="levels"))
    st.markdown("## Choose a Unit")
    st.caption("Select a unit to start the game.")
    for i, unit in enumerate(DATA[level]):
        if st.button(f"{i+1}. {unit['title']}", key=f"unit_{level}_{i}", use_container_width=True):
            start_game(level, i)
            st.rerun()

elif st.session_state.screen == "game":
    st_autorefresh(interval=1000, key=f"timer_{st.session_state.game_id}")
    unit = DATA[st.session_state.level][st.session_state.unit_index]
    st.markdown(f"### {unit['title']}")
    m1, m2, m3, m4 = st.columns(4)
    with m1: show_metric("SCORE", st.session_state.score)
    with m2: show_metric("CORRECT", f"{st.session_state.correct}/20")
    with m3: show_metric("INCORRECT", st.session_state.errors)
    with m4:
        mins, secs = divmod(elapsed_seconds(), 60)
        show_metric("TIME", f"{mins:02d}:{secs:02d}")

    st.progress(st.session_state.correct / 20)
    st.info(st.session_state.message)
    left, right = st.columns(2, gap="large")
    selected = st.session_state.selected
    with left:
        st.markdown("#### 🇹🇷 TURKISH")
        for word in st.session_state.tr_cards:
            is_selected = selected == ("tr", word["id"])
            label = ("🔹 " if is_selected else "") + word["tr"]
            if st.button(label, key=f"tr_{st.session_state.game_id}_{word['id']}", use_container_width=True):
                choose_card("tr", word["id"])
                st.rerun()
    with right:
        st.markdown("#### 🇬🇧 ENGLISH")
        for word in st.session_state.en_cards:
            is_selected = selected == ("en", word["id"])
            label = ("🔹 " if is_selected else "") + word["en"]
            if st.button(label, key=f"en_{st.session_state.game_id}_{word['id']}", use_container_width=True):
                choose_card("en", word["id"])
                st.rerun()

    st.caption("Correct match: +50 points  •  Incorrect match: -20 points  •  Your score cannot go below zero.")
    if st.button("Finish Game", type="secondary"):
        finish_game()
        st.rerun()

elif st.session_state.screen == "result":
    mins, secs = divmod(elapsed_seconds(), 60)
    st.markdown("## 🏆 Game Completed!")
    st.markdown("### Your Results")
    a,b,c = st.columns(3)
    with a: show_metric("TOTAL SCORE", st.session_state.score)
    with b: show_metric("CORRECT MATCHES", st.session_state.correct)
    with c: show_metric("TIME TAKEN", f"{mins:02d}:{secs:02d}")
    st.write(f"Incorrect matches: **{st.session_state.errors}**")
    if st.button("Play This Unit Again", use_container_width=True):
        start_game(st.session_state.level, st.session_state.unit_index)
        st.rerun()
    if st.button("Back to Unit Selection", use_container_width=True):
        st.session_state.screen = "units"
        st.rerun()
    if st.button("Main Menu", use_container_width=True):
        st.session_state.screen = "levels"
        st.rerun()
