import streamlit as st
import random
import time
from english_words import get_english_words_set

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="AI Word Chain Battle",
    page_icon="🔤",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# COMMON ENGLISH WORDS FOR AI
# ============================================================
# The player can use the large English dictionary.
# The AI uses only this curated common-word list so it
# does not generate words such as TERRAGE or THELIUM.

COMMON_AI_WORDS = set(
    (
        "apple animal answer airport aunt autumn artist"
        "baby ball banana beach bear beautiful bird birthday book"
        "boy bread brother brown bus business butterfly"
        "cake camera car cat chair chance child chocolate city class"
        "cloud coffee college computer country cousin cow"
        "dance day doctor dog door dream dress drink"
        "earth east egg elephant evening example eye"
        "family farmer father favorite field film fire fish flower"
        "food football forest friend fruit future"
        "game garden girl glass goat gold good grandmother grandfather"
        "grass great green group guitar"
        "hair hand happy hat head health heart hill history home honey"
        "horse hospital house human"
        "ice idea island image important internet"
        "jacket job juice jump"
        "key king kitchen kite knowledge"
        "lake language laptop large laugh leaf learning lemon life light"
        "lion little love lunch"
        "machine market math meal medicine memory milk money monkey moon"
        "morning mother mountain movie music"
        "name nature night number nurse"
        "ocean office orange outside"
        "paper parent park party people phone picture pizza place plant"
        "player police potato power present problem program"
        "queen question quick quiet"
        "rabbit radio rain rainbow reading river road room"
        "school science sea season second sister sky sleep small smile"
        "snake snow soccer song spring star station student summer sun"
        "table teacher team telephone television thing tiger time train"
        "tree trip truck"
        "umbrella uncle university useful"
        "valley vegetable video village violin voice"
        "waiter wall water weather week west window winter woman world"
        "xylophone"
        "year yellow young"
        "zebra zero zoo"
        "able about above across action actually address adult after again"
        "against age ago air all almost alone along already also always"
        "amazing among amount animal another anyone anything around arrive"
        "away"
        "back bad bank basic become before begin behind believe below best"
        "better between big black blue body both box bring build"
        "call can care carry change clean clear close cold come common"
        "complete control cool cost create"
        "dark data dead deal dear deep develop difference difficult dinner"
        "early easy enough even ever every exact"
        "face fact fall far fast father feel few final find first follow"
        "free fresh full"
        "general get give glad go great ground group grow"
        "half hard have help high hold hope hot huge"
        "if important inside instead into"
        "just keep kind know"
        "last late learn least leave less let level long look lose lot"
        "low"
        "main make many maybe mean meet member middle might more most move"
        "much must"
        "near need never new next nice nothing now"
        "often old once one only open order other over own"
        "part past pay peace perhaps personal place plan play point possible"
        "power pretty probably public put"
        "real reason red remember right run"
        "same save say school seem send several share short should show"
        "simple since single sit six slow small social special start stay"
        "still story strong such sure"
        "take talk tell than thank that their them then there these they"
        "thing think third this those three through together too true try"
        "turn two"
        "under understand until use usually"
        "very"
        "walk want warm watch way well white whole why win without work"
        "write wrong"
        "young"
        "zero"
    ).split()
)

COMMON_AI_WORDS = {
    word.lower()
    for word in COMMON_AI_WORDS
    if word.isalpha() and 2 <= len(word) <= 12
}

# ============================================================
# LARGE PLAYER DICTIONARY
# ============================================================

try:
    VALID_WORDS = get_english_words_set(
        ["web2"],
        lower=True
    )

    VALID_WORDS = {
        word.lower()
        for word in VALID_WORDS
        if word.isalpha() and 2 <= len(word) <= 20
    }

except Exception:
    VALID_WORDS = set(COMMON_AI_WORDS)

# Always make common AI words valid player words too.
VALID_WORDS.update(COMMON_AI_WORDS)

# ============================================================
# SESSION STATE
# ============================================================

if "game_started" not in st.session_state:
    st.session_state.game_started = False

if "player_score" not in st.session_state:
    st.session_state.player_score = 0

if "ai_score" not in st.session_state:
    st.session_state.ai_score = 0

if "lives" not in st.session_state:
    st.session_state.lives = 3

if "round" not in st.session_state:
    st.session_state.round = 1

if "combo" not in st.session_state:
    st.session_state.combo = 0

if "max_combo" not in st.session_state:
    st.session_state.max_combo = 0

if "used_words" not in st.session_state:
    st.session_state.used_words = set()

if "history" not in st.session_state:
    st.session_state.history = []

if "current_letter" not in st.session_state:
    st.session_state.current_letter = ""

if "ai_last_word" not in st.session_state:
    st.session_state.ai_last_word = ""

if "player_last_word" not in st.session_state:
    st.session_state.player_last_word = ""

if "game_over" not in st.session_state:
    st.session_state.game_over = False

if "high_score" not in st.session_state:
    st.session_state.high_score = 0

if "start_time" not in st.session_state:
    st.session_state.start_time = None

if "last_turn_time" not in st.session_state:
    st.session_state.last_turn_time = None

if "total_moves" not in st.session_state:
    st.session_state.total_moves = 0

if "successful_moves" not in st.session_state:
    st.session_state.successful_moves = 0

if "message" not in st.session_state:
    st.session_state.message = ""

if "message_type" not in st.session_state:
    st.session_state.message_type = "info"

# ============================================================
# CSS
# ============================================================

st.markdown(
    "<style>"
    ".stApp {"
    "background: linear-gradient(135deg, #07111f 0%, #101b35 50%, #111827 100%);"
    "}"
    ".main-title {"
    "font-size: 48px;"
    "font-weight: 800;"
    "text-align: center;"
    "margin-top: 10px;"
    "margin-bottom: 5px;"
    "}"
    ".sub-title {"
    "font-size: 18px;"
    "text-align: center;"
    "margin-bottom: 25px;"
    "opacity: 0.8;"
    "}"
    ".word-card {"
    "padding: 25px;"
    "border-radius: 20px;"
    "background: rgba(255,255,255,0.08);"
    "border: 1px solid rgba(255,255,255,0.15);"
    "text-align: center;"
    "margin: 10px 0;"
    "}"
    ".big-word {"
    "font-size: 42px;"
    "font-weight: 800;"
    "margin: 10px;"
    "}"
    ".letter-box {"
    "font-size: 55px;"
    "font-weight: 900;"
    "text-align: center;"
    "padding: 15px;"
    "border-radius: 18px;"
    "background: rgba(255,255,255,0.10);"
    "}"
    ".stat-card {"
    "padding: 18px;"
    "border-radius: 16px;"
    "background: rgba(255,255,255,0.08);"
    "border: 1px solid rgba(255,255,255,0.10);"
    "text-align: center;"
    "}"
    ".stat-number {"
    "font-size: 30px;"
    "font-weight: 800;"
    "}"
    ".stat-label {"
    "font-size: 14px;"
    "opacity: 0.75;"
    "}"
    ".ai-badge {"
    "font-size: 15px;"
    "font-weight: 700;"
    "text-align: center;"
    "margin-bottom: 5px;"
    "}"
    ".success-box {"
    "padding: 15px;"
    "border-radius: 12px;"
    "background: rgba(34,197,94,0.15);"
    "border: 1px solid rgba(34,197,94,0.35);"
    "}"
    ".warning-box {"
    "padding: 15px;"
    "border-radius: 12px;"
    "background: rgba(234,179,8,0.15);"
    "border: 1px solid rgba(234,179,8,0.35);"
    "}"
    ".danger-box {"
    "padding: 15px;"
    "border-radius: 12px;"
    "background: rgba(239,68,68,0.15);"
    "border: 1px solid rgba(239,68,68,0.35);"
    "}"
    "</style>",
    unsafe_allow_html=True
)

# ============================================================
# FUNCTIONS
# ============================================================

def reset_game():
    st.session_state.game_started = True
    st.session_state.player_score = 0
    st.session_state.ai_score = 0
    st.session_state.lives = 3
    st.session_state.round = 1
    st.session_state.combo = 0
    st.session_state.max_combo = 0
    st.session_state.used_words = set()
    st.session_state.history = []
    st.session_state.current_letter = ""
    st.session_state.ai_last_word = ""
    st.session_state.player_last_word = ""
    st.session_state.game_over = False
    st.session_state.message = ""
    st.session_state.message_type = "info"
    st.session_state.start_time = time.time()
    st.session_state.last_turn_time = time.time()
    st.session_state.total_moves = 0
    st.session_state.successful_moves = 0


def get_ai_words(letter):
    words = [
        word
        for word in COMMON_AI_WORDS
        if word.startswith(letter)
        and word not in st.session_state.used_words
    ]
    return words


def future_choices(word):
    next_letter = word[-1]
    choices = get_ai_words(next_letter)
    return len(choices)


def choose_ai_word(letter, difficulty):
    candidates = get_ai_words(letter)

    if not candidates:
        return None

    if difficulty == "Easy":
        return random.choice(candidates)

    if difficulty == "Medium":
        scored = []

        for word in candidates:
            score = future_choices(word)
            scored.append((word, score))

        max_future = max(score for _, score in scored)

        best_words = [
            word
            for word, score in scored
            if score >= max_future * 0.6
        ]

        return random.choice(best_words)

    # Hard mode:
    # AI tries to choose a word that gives the opponent
    # fewer possible responses.
    scored = []

    for word in candidates:
        score = future_choices(word)
        scored.append((word, score))

    min_future = min(score for _, score in scored)

    best_words = [
        word
        for word, score in scored
        if score <= min_future + 2
    ]

    return random.choice(best_words)


def calculate_rank(score):
    if score >= 500:
        return "🏆 Word Master"
    elif score >= 300:
        return "🥇 Word Expert"
    elif score >= 200:
        return "🥈 Word Champion"
    elif score >= 100:
        return "🥉 Word Player"
    return "🌱 Beginner"


def process_player_word(word, difficulty, game_mode):
    word = word.strip().lower()

    if not word:
        st.session_state.message = "Please enter a word."
        st.session_state.message_type = "warning"
        return

    st.session_state.total_moves += 1

    # Basic validation
    if not word.isalpha():
        st.session_state.message = "Please enter letters only."
        st.session_state.message_type = "warning"
        return

    if len(word) < 2:
        st.session_state.message = "Enter a word with at least 2 letters."
        st.session_state.message_type = "warning"
        return

    # Check dictionary
    if word not in VALID_WORDS:
        st.session_state.lives -= 1
        st.session_state.combo = 0

        st.session_state.message = (
            f"❌ '{word.upper()}' is not recognized as an English word. "
            f"You lost 1 life."
        )
        st.session_state.message_type = "danger"

        if st.session_state.lives <= 0:
            st.session_state.game_over = True

        return

    # First word
    if st.session_state.current_letter == "":
        pass

    else:
        required_letter = st.session_state.current_letter

        if not word.startswith(required_letter):
            st.session_state.lives -= 1
            st.session_state.combo = 0

            st.session_state.message = (
                f"❌ Your word must start with '{required_letter.upper()}'. "
                f"You lost 1 life."
            )
            st.session_state.message_type = "danger"

            if st.session_state.lives <= 0:
                st.session_state.game_over = True

            return

    # Repeated word
    if word in st.session_state.used_words:
        st.session_state.lives -= 1
        st.session_state.combo = 0

        st.session_state.message = (
            f"🔁 '{word.upper()}' was already used. You lost 1 life."
        )
        st.session_state.message_type = "danger"

        if st.session_state.lives <= 0:
            st.session_state.game_over = True

        return

    # Add player word
    st.session_state.used_words.add(word)
    st.session_state.player_last_word = word
    st.session_state.player_score += 10
    st.session_state.combo += 1
    st.session_state.successful_moves += 1

    if st.session_state.combo > st.session_state.max_combo:
        st.session_state.max_combo = st.session_state.combo

    # Combo bonus
    if st.session_state.combo >= 3:
        bonus = st.session_state.combo * 2
        st.session_state.player_score += bonus

    # AI needs to start with player's last letter
    next_letter = word[-1]

    ai_difficulty = difficulty

    if game_mode == "Survival":
        if st.session_state.round >= 8:
            ai_difficulty = "Hard"
        elif st.session_state.round >= 4:
            ai_difficulty = "Medium"

    ai_word = choose_ai_word(next_letter, ai_difficulty)

    # AI cannot continue
    if ai_word is None:
        st.session_state.player_score += 50
        st.session_state.message = (
            f"🎉 Amazing! AI could not find a common word starting with "
            f"'{next_letter.upper()}'. You won this round!"
        )
        st.session_state.message_type = "success"

        st.session_state.round += 1
        st.session_state.current_letter = ""
        st.session_state.ai_last_word = ""
        st.session_state.last_turn_time = time.time()

        if st.session_state.player_score > st.session_state.high_score:
            st.session_state.high_score = st.session_state.player_score

        return

    # Add AI word
    st.session_state.used_words.add(ai_word)
    st.session_state.ai_last_word = ai_word
    st.session_state.ai_score += 5

    st.session_state.current_letter = ai_word[-1]
    st.session_state.round += 1
    st.session_state.last_turn_time = time.time()

    st.session_state.history.append(
        {
            "Round": st.session_state.round - 1,
            "Player": word.upper(),
            "AI": ai_word.upper(),
            "Next Letter": ai_word[-1].upper()
        }
    )

    st.session_state.message = (
        f"🤖 AI played '{ai_word.upper()}'. "
        f"Your next letter is '{ai_word[-1].upper()}'."
    )
    st.session_state.message_type = "success"

    if st.session_state.player_score > st.session_state.high_score:
        st.session_state.high_score = st.session_state.player_score


def display_message():
    if not st.session_state.message:
        return

    if st.session_state.message_type == "success":
        st.markdown(
            f"<div class='success-box'>{st.session_state.message}</div>",
            unsafe_allow_html=True
        )

    elif st.session_state.message_type == "danger":
        st.markdown(
            f"<div class='danger-box'>{st.session_state.message}</div>",
            unsafe_allow_html=True
        )

    else:
        st.markdown(
            f"<div class='warning-box'>{st.session_state.message}</div>",
            unsafe_allow_html=True
        )


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:
    st.markdown("## 🎮 Game Control")

    game_mode = st.selectbox(
        "Game Mode",
        ["Classic", "Survival", "Time Attack"]
    )

    difficulty = st.selectbox(
        "AI Difficulty",
        ["Easy", "Medium", "Hard"]
    )

    st.markdown("---")

    if st.button("🚀 Start New Game", use_container_width=True):
        reset_game()
        st.rerun()

    if st.button("🔄 Reset Game", use_container_width=True):
        reset_game()
        st.rerun()

    st.markdown("---")

    st.markdown("### 🤖 AI Information")
    st.write("AI vocabulary: Common English words")
    st.write(f"AI vocabulary size: {len(COMMON_AI_WORDS):,}")
    st.write("Player dictionary: Large English dictionary")

    st.markdown("---")

    st.markdown("### 📖 How To Play")
    st.write("1. Enter an English word.")
    st.write("2. AI gives a word starting with your last letter.")
    st.write("3. Your next word must start with AI's last letter.")
    st.write("4. Repeated words are not allowed.")
    st.write("5. Keep your lives safe.")

# ============================================================
# HEADER
# ============================================================

st.markdown(
    "<div class='main-title'>🔤 AI WORD CHAIN BATTLE</div>",
    unsafe_allow_html=True
)

st.markdown(
    "<div class='sub-title'>Challenge the AI • Build word chains • Beat your high score</div>",
    unsafe_allow_html=True
)

# ============================================================
# TOP STATS
# ============================================================

col1, col2, col3, col4, col5, col6 = st.columns(6)

with col1:
    st.markdown(
        "<div class='stat-card'>"
        "<div class='stat-number'>"
        + str(st.session_state.player_score)
        + "</div>"
        "<div class='stat-label'>YOUR SCORE</div>"
        "</div>",
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        "<div class='stat-card'>"
        "<div class='stat-number'>"
        + str(st.session_state.ai_score)
        + "</div>"
        "<div class='stat-label'>AI SCORE</div>"
        "</div>",
        unsafe_allow_html=True
    )

with col3:
    st.markdown(
        "<div class='stat-card'>"
        "<div class='stat-number'>"
        + ("❤️ " * st.session_state.lives)
        + "</div>"
        "<div class='stat-label'>LIVES</div>"
        "</div>",
        unsafe_allow_html=True
    )

with col4:
    st.markdown(
        "<div class='stat-card'>"
        "<div class='stat-number'>"
        + str(st.session_state.round)
        + "</div>"
        "<div class='stat-label'>ROUND</div>"
        "</div>",
        unsafe_allow_html=True
    )

with col5:
    st.markdown(
        "<div class='stat-card'>"
        "<div class='stat-number'>"
        + str(st.session_state.combo)
        + "</div>"
        "<div class='stat-label'>COMBO</div>"
        "</div>",
        unsafe_allow_html=True
    )

with col6:
    st.markdown(
        "<div class='stat-card'>"
        "<div class='stat-number'>"
        + str(st.session_state.high_score)
        + "</div>"
        "<div class='stat-label'>HIGH SCORE</div>"
        "</div>",
        unsafe_allow_html=True
    )

st.divider()

# ============================================================
# GAME START SCREEN
# ============================================================

if not st.session_state.game_started:

    st.markdown(
        "<div class='word-card'>"
        "<div class='big-word'>🎯 Ready?</div>"
        "<p>Start a new game and challenge the AI.</p>"
        "</div>",
        unsafe_allow_html=True
    )

    st.info(
        "Click **Start New Game** from the sidebar to begin."
    )

    st.stop()

# ============================================================
# GAME OVER
# ============================================================

if st.session_state.game_over:

    st.error("💀 GAME OVER")

    rank = calculate_rank(st.session_state.player_score)

    st.markdown(
        "<div class='word-card'>"
        "<div class='big-word'>"
        + rank
        + "</div>"
        "<p>Final Score: "
        + str(st.session_state.player_score)
        + "</p>"
        "<p>Maximum Combo: "
        + str(st.session_state.max_combo)
        + "</p>"
        "</div>",
        unsafe_allow_html=True
    )

    if st.button("🎮 Play Again", use_container_width=True):
        reset_game()
        st.rerun()

    st.stop()

# ============================================================
# MESSAGE
# ============================================================

display_message()

st.divider()

# ============================================================
# CURRENT LETTER
# ============================================================

if st.session_state.current_letter:

    st.markdown(
        "<div class='ai-badge'>YOUR NEXT LETTER</div>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<div class='letter-box'>"
        + st.session_state.current_letter.upper()
        + "</div>",
        unsafe_allow_html=True
    )

else:

    st.markdown(
        "<div class='letter-box'>START</div>",
        unsafe_allow_html=True
    )

# ============================================================
# AI LAST WORD
# ============================================================

if st.session_state.ai_last_word:

    st.markdown(
        "<div class='word-card'>"
        "<div class='ai-badge'>🤖 AI LAST WORD</div>"
        "<div class='big-word'>"
        + st.session_state.ai_last_word.upper()
        + "</div>"
        "<p>Your next word must start with "
        + st.session_state.current_letter.upper()
        + "</p>"
        "</div>",
        unsafe_allow_html=True
    )

# ============================================================
# PLAYER INPUT
# ============================================================

st.markdown("### ✍️ Your Turn")

if st.session_state.current_letter:
    st.write(
        "Enter a word beginning with "
        + st.session_state.current_letter.upper()
        + "."
    )
else:
    st.write("Enter any English word to start the chain.")

player_word = st.text_input(
    "Enter your word",
    placeholder="Example: apple",
    key="player_word_input"
)

if st.button(
    "⚔️ PLAY WORD",
    use_container_width=True,
    type="primary"
):

    process_player_word(
        player_word,
        difficulty,
        game_mode
    )

    st.rerun()

# ============================================================
# GAME INFORMATION
# ============================================================

st.divider()

info1, info2, info3 = st.columns(3)

with info1:
    st.markdown("### 📊 Performance")

    if st.session_state.total_moves > 0:
        accuracy = (
            st.session_state.successful_moves
            / st.session_state.total_moves
        ) * 100
    else:
        accuracy = 0

    st.metric(
        "Accuracy",
        f"{accuracy:.1f}%"
    )

    st.metric(
        "Max Combo",
        st.session_state.max_combo
    )

with info2:
    st.markdown("### 🏅 Rank")

    st.markdown(
        "<div class='word-card'>"
        "<div class='big-word' style='font-size:28px;'>"
        + calculate_rank(st.session_state.player_score)
        + "</div>"
        "</div>",
        unsafe_allow_html=True
    )

with info3:
    st.markdown("### 🔤 Used Words")

    st.metric(
        "Words Used",
        len(st.session_state.used_words)
    )

# ============================================================
# WORD HISTORY
# ============================================================

st.divider()

st.markdown("### 📜 Word Chain History")

if st.session_state.history:

    for item in reversed(st.session_state.history):

        st.markdown(
            "<div class='word-card'>"
            "<b>Round "
            + str(item["Round"])
            + "</b> &nbsp;&nbsp; "
            "👤 "
            + item["Player"]
            + " → 🤖 "
            + item["AI"]
            + " → 🔤 "
            + item["Next Letter"]
            + "</div>",
            unsafe_allow_html=True
        )

else:
    st.info("Your word chain will appear here.")

# ============================================================
# USED WORDS
# ============================================================

with st.expander("📚 View Used Words"):

    if st.session_state.used_words:

        words = sorted(
            st.session_state.used_words
        )

        st.write(
            ", ".join(
                word.upper()
                for word in words
            )
        )

    else:
        st.write("No words used yet.")

# ============================================================
# AI STRATEGY
# ============================================================

with st.expander("🧠 How the AI Works"):

    st.markdown(
        "The AI uses **word-chain search** to select its response."
    )

    st.write(
        "• Easy: chooses a random common English word."
    )

    st.write(
        "• Medium: looks at future possible responses."
    )

    st.write(
        "• Hard: tries to leave fewer choices for the player."
    )

    st.write(
        "• Survival mode increases AI difficulty as rounds increase."
    )

    st.write(
        "• AI output is restricted to a curated common-English vocabulary."
    )

# ============================================================
# TIME ATTACK
# ============================================================

if game_mode == "Time Attack" and st.session_state.start_time:

    elapsed = int(
        time.time() - st.session_state.last_turn_time
    )

    remaining = max(0, 10 - elapsed)

    st.markdown(
        "### ⏱️ Time Attack"
    )

    st.progress(
        remaining / 10
    )

    st.write(
        "Time remaining: "
        + str(remaining)
        + " seconds"
    )

    if remaining == 0:

        st.session_state.lives -= 1
        st.session_state.combo = 0
        st.session_state.last_turn_time = time.time()

        if st.session_state.lives <= 0:
            st.session_state.game_over = True

        st.warning(
            "⏰ Time's up! You lost one life."
        )

# ============================================================
# FOOTER
# ============================================================

st.divider()

st.markdown(
    "<div style='text-align:center; opacity:0.65;'>"
    "🔤 AI Word Chain Battle • Built with Python + Streamlit"
    "</div>",
    unsafe_allow_html=True
)