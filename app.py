import os
import json
import streamlit as st
import streamlit.components.v1 as components

from openrouter_client import fetch_free_models, stream_chat_completion
from styles import TELEGRAM_DARK_MINIMAL_CSS

# Page Configuration
st.set_page_config(
    page_title="AI Chat // Workspace",
    page_icon="💬",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Apply Minimalist Dark CSS
st.markdown(TELEGRAM_DARK_MINIMAL_CSS, unsafe_allow_html=True)

# Persistent History Directory
HISTORY_DIR = os.path.join(os.path.dirname(__file__), "data_history")
os.makedirs(HISTORY_DIR, exist_ok=True)

def load_history(device_id: str) -> list:
    if not device_id:
        return []
    safe_id = "".join(c for c in device_id if c.isalnum() or c in ("-", "_"))
    path = os.path.join(HISTORY_DIR, f"{safe_id}.json")
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
    return []

def save_history(device_id: str, messages: list):
    if not device_id:
        return
    safe_id = "".join(c for c in device_id if c.isalnum() or c in ("-", "_"))
    path = os.path.join(HISTORY_DIR, f"{safe_id}.json")
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(messages, f, ensure_ascii=False, indent=2)
    except Exception:
        pass

def clear_history(device_id: str):
    if not device_id:
        return
    safe_id = "".join(c for c in device_id if c.isalnum() or c in ("-", "_"))
    path = os.path.join(HISTORY_DIR, f"{safe_id}.json")
    if os.path.exists(path):
        try:
            os.remove(path)
        except Exception:
            pass

# Browser LocalStorage Synchronization Bridge
components.html("""
<script>
(function() {
    try {
        const key = 'chat_free_device_id';
        let storedId = localStorage.getItem(key);
        if (!storedId) {
            storedId = 'user_' + Math.random().toString(36).substring(2, 10) + Date.now().toString(36);
            localStorage.setItem(key, storedId);
        }
        const parentUrl = new URL(window.parent.location.href);
        const curParam = parentUrl.searchParams.get('dev_id');
        if (curParam !== storedId) {
            parentUrl.searchParams.set('dev_id', storedId);
            window.parent.location.replace(parentUrl.toString());
        }
    } catch (e) {}
})();
</script>
""", height=0, width=0)

# Get current persistent device id
current_device_id = st.query_params.get("dev_id", "default_browser")

# Initialize session state with persisted history
if "current_page" not in st.session_state:
    st.session_state.current_page = "hub"

if "history_loaded" not in st.session_state:
    st.session_state.messages = load_history(current_device_id)
    st.session_state.history_loaded = True

# Fetch Free Models (cached)
@st.cache_data(ttl=1800, show_spinner=False)
def load_models():
    return fetch_free_models()

free_models = load_models()
model_ids = [m["id"] for m in free_models]

# Default to NVIDIA Nemotron 3 Ultra (free)
default_index = 0
for idx, m in enumerate(free_models):
    if "nemotron-3-ultra" in m["id"].lower():
        default_index = idx
        break

def format_model(m_id):
    m_data = next((item for item in free_models if item["id"] == m_id), None)
    if m_data:
        ctx = m_data.get("context_length", 0)
        ctx_tag = f"{ctx // 1000}k" if ctx >= 1000 else f"{ctx}"
        return f"{m_data['name']} • {ctx_tag}"
    return m_id


# ==========================================
# 1. SCREEN: HUB / LAUNCHER (4 Minimal Rectangles)
# ==========================================
if st.session_state.current_page == "hub":
    st.markdown('<div class="hub-container"><div class="hub-grid">', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        if st.button("💬 ChatBot", key="hub_btn_chat", use_container_width=True):
            st.session_state.current_page = "chat"
            st.rerun()

        st.button("⚡ Code Studio", key="hub_btn_code", disabled=True, use_container_width=True)

    with col2:
        st.button("📊 Analytics", key="hub_btn_analytics", disabled=True, use_container_width=True)
        st.button("🌐 Services", key="hub_btn_services", disabled=True, use_container_width=True)

    st.markdown('</div></div>', unsafe_allow_html=True)


# ==========================================
# 2. SCREEN: AI CHATBOT (Telegram-style)
# ==========================================
elif st.session_state.current_page == "chat":

    # Top Navigation Bar with Return to Hub and Clear buttons
    top_col0, top_col1, top_col2, top_col3 = st.columns([0.8, 1.0, 2.2, 0.4])

    with top_col0:
        if st.button("← Хаб", help="Вернуться в Хаб сервисов", use_container_width=True):
            st.session_state.current_page = "hub"
            st.rerun()

    with top_col1:
        st.markdown("""
            <div style="display: flex; align-items: center; gap: 7px; height: 38px;">
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
            clear_history(current_device_id)
            st.rerun()

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
                    История сохраняется в вашем браузере автоматически.
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

    # Chat Input & Streaming
    user_query = st.chat_input("Сообщение...")

    if user_query:
        # 1. User Message (Telegram Right Bubble)
        st.session_state.messages.append({"role": "user", "content": user_query})
        save_history(current_device_id, st.session_state.messages)
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
                save_history(current_device_id, st.session_state.messages)
