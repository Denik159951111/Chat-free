import streamlit as st
from openrouter_client import fetch_free_models, stream_chat_completion
from styles import TELEGRAM_DARK_MINIMAL_CSS

# Page Configuration (Centered Telegram / Hub layout)
st.set_page_config(
    page_title="Workspace Hub // AI Chat",
    page_icon="⚡",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Apply Minimalist Dark CSS
st.markdown(TELEGRAM_DARK_MINIMAL_CSS, unsafe_allow_html=True)

# State Management
if "current_page" not in st.session_state:
    st.session_state.current_page = "hub"  # 'hub' or 'chat'

if "messages" not in st.session_state:
    st.session_state.messages = []

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

# Format model label for dropdown
def format_model(m_id):
    m_data = next((item for item in free_models if item["id"] == m_id), None)
    if m_data:
        ctx = m_data.get("context_length", 0)
        ctx_tag = f"{ctx // 1000}k" if ctx >= 1000 else f"{ctx}"
        return f"{m_data['name']} • {ctx_tag}"
    return m_id


# ==========================================
# 1. SCREEN: HUB / LAUNCHER (Default start)
# ==========================================
if st.session_state.current_page == "hub":
    st.markdown("""
        <div class="hub-header">
            <div style="display: inline-flex; align-items: center; gap: 7px; margin-bottom: 0.5rem;">
                <div class="tg-brand-dot"></div>
                <span style="font-family: var(--font-mono); font-size: 0.72rem; color: #7a8094; letter-spacing: 0.1em; text-transform: uppercase;">WORKSPACE // PORTAL</span>
            </div>
            <div class="hub-title">Выберите сервис для запуска</div>
            <div class="hub-subtitle">Единая точка доступа к вашим модулям и инструментам</div>
        </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        # Card 1: AI Chatbot (Active)
        st.markdown("""
            <div class="hub-card">
                <div class="hub-card-top">
                    <div class="hub-card-icon-title">
                        <span style="font-size: 1.2rem;">💬</span>
                        <span class="hub-card-title">AI Chatbot</span>
                    </div>
                    <span class="hub-status-active">АКТИВЕН</span>
                </div>
                <div class="hub-card-desc">
                    Минималистичный чат-бот с бесплатными нейросетями: NVIDIA Nemotron 3 Ultra, Gemma 4, MiniMax.
                </div>
            </div>
        """, unsafe_allow_html=True)

        if st.button("Запустить чат →", key="launch_chat", use_container_width=True):
            st.session_state.current_page = "chat"
            st.rerun()

        st.markdown("<div style='margin-bottom: 1.2rem;'></div>", unsafe_allow_html=True)

        # Card 3: Analytics & Data (Coming Soon)
        st.markdown("""
            <div class="hub-card">
                <div class="hub-card-top">
                    <div class="hub-card-icon-title">
                        <span style="font-size: 1.2rem;">📊</span>
                        <span class="hub-card-title">Data & Analytics</span>
                    </div>
                    <span class="hub-status-soon">СКОРО</span>
                </div>
                <div class="hub-card-desc">
                    Модуль визуализации метрик, анализа больших данных и RAG-индексации документов.
                </div>
            </div>
        """, unsafe_allow_html=True)
        st.button("В разработке", key="launch_analytics", disabled=True, use_container_width=True)

    with col2:
        # Card 2: Code Studio (Coming Soon)
        st.markdown("""
            <div class="hub-card">
                <div class="hub-card-top">
                    <div class="hub-card-icon-title">
                        <span style="font-size: 1.2rem;">⚡</span>
                        <span class="hub-card-title">Code Studio</span>
                    </div>
                    <span class="hub-status-soon">СКОРО</span>
                </div>
                <div class="hub-card-desc">
                    Интерактивная среда для генерации, аудита алгоритмов и тестирования скриптов.
                </div>
            </div>
        """, unsafe_allow_html=True)
        st.button("В разработке", key="launch_code", disabled=True, use_container_width=True)

        st.markdown("<div style='margin-bottom: 1.2rem;'></div>", unsafe_allow_html=True)

        # Card 4: Web Services (Coming Soon)
        st.markdown("""
            <div class="hub-card">
                <div class="hub-card-top">
                    <div class="hub-card-icon-title">
                        <span style="font-size: 1.2rem;">🌐</span>
                        <span class="hub-card-title">Web Services</span>
                    </div>
                    <span class="hub-status-soon">СКОРО</span>
                </div>
                <div class="hub-card-desc">
                    Шлюз управления микросервисами, webhook-интеграциями и серверной автоматизацией.
                </div>
            </div>
        """, unsafe_allow_html=True)
        st.button("В разработке", key="launch_web", disabled=True, use_container_width=True)


# ==========================================
# 2. SCREEN: AI CHATBOT (Telegram-style)
# ==========================================
elif st.session_state.current_page == "chat":

    # Minimal Top Bar with Return to Hub button
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

    # Chat Input & Streaming
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
