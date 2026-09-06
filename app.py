import streamlit as st
from openrouter_client import fetch_free_models, stream_chat_completion
from styles import TELEGRAM_DARK_MINIMAL_CSS

# Page Configuration (Centered Telegram-like layout)
st.set_page_config(
    page_title="AI Chat",
    page_icon="💬",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Apply Minimalist Dark Telegram CSS
st.markdown(TELEGRAM_DARK_MINIMAL_CSS, unsafe_allow_html=True)

# Session State
if "messages" not in st.session_state:
    st.session_state.messages = []

# Fetch Free Models (cached)
@st.cache_data(ttl=1800, show_spinner=False)
def load_models():
    return fetch_free_models()

free_models = load_models()
model_ids = [m["id"] for m in free_models]

# Default model preference: NVIDIA Nemotron 3 Ultra (free)
default_index = 0
for idx, m in enumerate(free_models):
    if "nemotron-3-ultra" in m["id"].lower():
        default_index = idx
        break

# Format model label for dropdown
def format_model(m_id):
    m_data = next((item for item in free_models if item["id"] == m_id), None)
    if m_data:
        ctx = m_data.get("context_length", 0)
        ctx_tag = f"{ctx // 1000}k" if ctx >= 1000 else f"{ctx}"
        # Return clean concise name
        return f"{m_data['name']} • {ctx_tag}"
    return m_id

# --- MINIMAL TOP BAR ---
top_col1, top_col2, top_col3 = st.columns([1.1, 2.3, 0.4])

with top_col1:
    st.markdown("""
        <div style="display: flex; align-items: center; gap: 8px; height: 38px;">
            <div class="tg-brand-dot"></div>
            <span class="tg-brand-title">AI Chat</span>
        </div>
    """, unsafe_allow_html=True)

with top_col2:
    selected_model_id = st.selectbox(
        label="Модель:",
        options=model_ids,
        index=default_index,
        format_func=format_model,
        label_visibility="collapsed"
    )

with top_col3:
    if st.button("🗑️", help="Очистить диалог", use_container_width=True):
        st.session_state.messages = []
        st.rerun()


# --- CHAT STREAM ---

# Empty Chat Placeholder (Minimalist)
if not st.session_state.messages:
    cur_model_obj = next((m for m in free_models if m["id"] == selected_model_id), None)
    model_name = cur_model_obj["name"] if cur_model_obj else selected_model_id
    
    st.markdown(f"""
        <div class="empty-chat-placeholder">
            <div class="placeholder-icon">💬</div>
            <div class="placeholder-title">Диалог пуст</div>
            <div class="placeholder-sub">
                Подключена модель <b>{model_name}</b>.<br>
                Напишите сообщение в поле внизу для начала диалога.
            </div>
        </div>
    """, unsafe_allow_html=True)

# Render Existing Messages (Telegram Bubbles)
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        if msg["role"] == "assistant" and msg.get("reasoning"):
            with st.expander("🧠 Рассуждения", expanded=False):
                st.markdown(f"<div class='reasoning-text-minimal'>{msg['reasoning']}</div>", unsafe_allow_html=True)
        st.markdown(msg["content"])


# --- CHAT INPUT & STREAMING ---
user_query = st.chat_input("Сообщение...")

if user_query:
    # 1. User Message (Telegram Right Bubble)
    st.session_state.messages.append({"role": "user", "content": user_query})
    with st.chat_message("user"):
        st.markdown(user_query)

    # 2. Build Payload
    payload_messages = [
        {"role": m["role"], "content": m["content"]}
        for m in st.session_state.messages
    ]

    # 3. Stream Assistant Response (Telegram Left Bubble)
    with st.chat_message("assistant"):
        reasoning_container = st.empty()
        content_container = st.empty()

        full_content = ""
        full_reasoning = ""
        error_flag = False

        stream = stream_chat_completion(
            model=selected_model_id,
            messages=payload_messages,
            temperature=0.7
        )

        for chunk_type, text in stream:
            if chunk_type == "reasoning":
                full_reasoning += text
                with reasoning_container.container():
                    with st.expander("🧠 Рассуждения", expanded=True):
                        st.markdown(f"<div class='reasoning-text-minimal'>{full_reasoning}</div>", unsafe_allow_html=True)
            elif chunk_type == "content":
                full_content += text
                content_container.markdown(full_content + '<span class="streaming-cursor-mono"></span>', unsafe_allow_html=True)
            elif chunk_type == "error":
                error_flag = True
                content_container.error(text)
                break

        if not error_flag:
            if full_reasoning:
                with reasoning_container.container():
                    with st.expander("🧠 Рассуждения", expanded=False):
                        st.markdown(f"<div class='reasoning-text-minimal'>{full_reasoning}</div>", unsafe_allow_html=True)

            content_container.markdown(full_content if full_content else "_Ответ получен._")

            assistant_msg = {"role": "assistant", "content": full_content}
            if full_reasoning:
                assistant_msg["reasoning"] = full_reasoning
            st.session_state.messages.append(assistant_msg)
