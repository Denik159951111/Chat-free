import os
import time
import streamlit as st
import streamlit.components.v1 as components

from openrouter_client import fetch_free_models, stream_chat_completion
from styles import TELEGRAM_DARK_MINIMAL_CSS
from history_manager import (
    load_user_store,
    save_user_store,
    create_new_chat,
    delete_chat,
    update_active_messages,
)

# Page Configuration
st.set_page_config(
    page_title="AI Chat // Workspace",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply Minimalist Dark CSS
st.markdown(TELEGRAM_DARK_MINIMAL_CSS, unsafe_allow_html=True)

# Client Controller: LocalStorage Sync, Auto-Scroll, Smart Header, Code Collapsing & Copy
CLIENT_CONTROLLER_JS = """
<script>
(function() {
    const parentDoc = window.parent.document;
    const parentWin = window.parent;

    // 1. Device ID LocalStorage Sync
    try {
        const key = 'chat_free_device_id';
        let storedId = localStorage.getItem(key);
        if (!storedId) {
            storedId = 'user_' + Math.random().toString(36).substring(2, 10) + Date.now().toString(36);
            localStorage.setItem(key, storedId);
        }
        const parentUrl = new URL(parentWin.location.href);
        const curParam = parentUrl.searchParams.get('dev_id');
        if (curParam !== storedId) {
            parentUrl.searchParams.set('dev_id', storedId);
            parentWin.location.replace(parentUrl.toString());
            return;
        }
    } catch (e) {}

    // 2. Floating Scroll-to-Top Button Injection
    let btnTop = parentDoc.getElementById('btnScrollTop');
    if (!btnTop) {
        btnTop = parentDoc.createElement('div');
        btnTop.id = 'btnScrollTop';
        btnTop.className = 'scroll-top-btn';
        btnTop.innerText = 'Вверх';
        btnTop.onclick = function() {
            parentWin.scrollTo({ top: 0, behavior: 'smooth' });
        };
        parentDoc.body.appendChild(btnTop);
    }

    // 3. Smart Header Reveal on Scroll Up & Scroll-Top Visibility
    let lastScrollY = parentWin.scrollY || 0;
    parentWin.onscroll = function() {
        const curY = parentWin.scrollY || 0;
        const header = parentDoc.getElementById('customStickyHeader');

        // Scroll to top button visibility
        if (btnTop) {
            if (curY > 260) {
                btnTop.classList.add('visible');
            } else {
                btnTop.classList.remove('visible');
            }
        }

        // Header slide down when scrolling UP
        if (header) {
            if (curY < 40) {
                header.classList.remove('header-hidden');
            } else if (curY < lastScrollY - 3) {
                // Scrolling UP: reveal header smoothly!
                header.classList.remove('header-hidden');
            } else if (curY > lastScrollY + 4) {
                // Scrolling DOWN: hide header smoothly!
                header.classList.add('header-hidden');
            }
        }
        lastScrollY = curY;
    };

    // 4. Auto-Scroll to Bottom on Chat Load
    setTimeout(function() {
        const chatContainer = parentDoc.querySelector('.stChatMessageContainer');
        if (chatContainer) {
            parentWin.scrollTo({ top: parentDoc.body.scrollHeight, behavior: 'smooth' });
        }
    }, 200);

    // 5. Enhance Code Blocks: Collapsible Large Snippets & 1-Click Copy
    function enhanceCodeBlocks() {
        const preBlocks = parentDoc.querySelectorAll('pre');
        preBlocks.forEach(function(pre) {
            if (pre.dataset.enhanced === 'true') return;
            pre.dataset.enhanced = 'true';

            // Add Copy Button
            const copyBtn = parentDoc.createElement('div');
            copyBtn.className = 'code-copy-btn';
            copyBtn.innerText = 'Копировать';
            copyBtn.onclick = function(e) {
                e.stopPropagation();
                const codeEl = pre.querySelector('code') || pre;
                const text = codeEl.innerText || codeEl.textContent;
                navigator.clipboard.writeText(text).then(function() {
                    copyBtn.innerText = 'Скопировано';
                    setTimeout(function() { copyBtn.innerText = 'Копировать'; }, 1500);
                });
            };
            pre.appendChild(copyBtn);

            // If large snippet (height > 260px), make it collapsible
            if (pre.scrollHeight > 260) {
                pre.classList.add('code-collapsed');

                const toggleBar = parentDoc.createElement('div');
                toggleBar.className = 'code-toggle-bar';
                toggleBar.innerText = 'Развернуть код';
                toggleBar.onclick = function() {
                    if (pre.classList.contains('code-collapsed')) {
                        pre.classList.remove('code-collapsed');
                        toggleBar.innerText = 'Свернуть код';
                    } else {
                        pre.classList.add('code-collapsed');
                        toggleBar.innerText = 'Развернуть код';
                        pre.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
                    }
                };
                pre.appendChild(toggleBar);
            }
        });
    }

    // Run enhancement and observe new messages
    enhanceCodeBlocks();
    const observer = new MutationObserver(enhanceCodeBlocks);
    observer.observe(parentDoc.body, { childList: true, subtree: true });

})();
</script>
"""

components.html(CLIENT_CONTROLLER_JS, height=0, width=0)

# Get current persistent device id
current_device_id = st.query_params.get("dev_id", "default_browser")

# Load full user store
user_store = load_user_store(current_device_id)

# Initialize Session State
if "current_page" not in st.session_state:
    st.session_state.current_page = "hub"

# Fetch Free Models (cached)
@st.cache_data(ttl=1800, show_spinner=False)
def load_models():
    return fetch_free_models()

free_models = load_models()
model_ids = [m["id"] for m in free_models]

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
        return f"{m_data['name']} - {ctx_tag}"
    return m_id


# ==========================================
# 1. SCREEN: HUB / LAUNCHER (4 Rectangles)
# ==========================================
if st.session_state.current_page == "hub":
    st.markdown('<div class="hub-container"><div class="hub-grid">', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        if st.button("ChatBot", key="hub_btn_chat", use_container_width=True):
            st.session_state.current_page = "chat"
            st.rerun()

        st.button("Code Studio", key="hub_btn_code", disabled=True, use_container_width=True)

    with col2:
        st.button("Analytics", key="hub_btn_analytics", disabled=True, use_container_width=True)
        st.button("Services", key="hub_btn_services", disabled=True, use_container_width=True)

    st.markdown('</div></div>', unsafe_allow_html=True)


# ==========================================
# 2. SCREEN: AI CHATBOT WITH HISTORY
# ==========================================
elif st.session_state.current_page == "chat":

    active_chat_id = user_store.get("active_chat_id")
    if not active_chat_id or active_chat_id not in user_store["chats"]:
        active_chat_id = next(iter(user_store["chats"].keys()))
        user_store["active_chat_id"] = active_chat_id

    active_chat = user_store["chats"][active_chat_id]
    current_messages = active_chat.get("messages", [])

    # --- SIDEBAR: CHAT HISTORY DRAWER ---
    with st.sidebar:
        st.markdown('<div class="btn-new-chat">', unsafe_allow_html=True)
        if st.button("+ Новый диалог", key="btn_new_chat", use_container_width=True):
            new_id = create_new_chat(current_device_id, user_store)
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="history-title">История диалогов</div>', unsafe_allow_html=True)

        # List all saved chats
        chat_ids = list(user_store["chats"].keys())
        for cid in reversed(chat_ids):
            c_info = user_store["chats"][cid]
            is_active = (cid == active_chat_id)
            btn_label = f"{c_info.get('title', 'Диалог')} ({c_info.get('created_at', '')})"

            col_ch1, col_ch2 = st.columns([5, 1])
            with col_ch1:
                if is_active:
                    st.markdown('<div class="active-chat-item">', unsafe_allow_html=True)
                if st.button(btn_label, key=f"sel_{cid}", use_container_width=True):
                    user_store["active_chat_id"] = cid
                    save_user_store(current_device_id, user_store)
                    st.rerun()
                if is_active:
                    st.markdown('</div>', unsafe_allow_html=True)

            with col_ch2:
                if len(chat_ids) > 1:
                    if st.button("x", key=f"del_{cid}", help="Удалить диалог"):
                        delete_chat(current_device_id, user_store, cid)
                        st.rerun()

    # --- SMART STICKY TOP BAR (Slides down when scrolling up) ---
    st.markdown('<div id="customStickyHeader">', unsafe_allow_html=True)
    top_col0, top_col1, top_col2, top_col3 = st.columns([0.9, 1.1, 2.2, 0.8])

    with top_col0:
        if st.button("Назад в хаб", help="Вернуться в Хаб сервисов", use_container_width=True):
            st.session_state.current_page = "hub"
            st.rerun()

    with top_col1:
        st.markdown("""
            <div style="display: flex; align-items: center; height: 38px;">
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
        if st.button("Очистить", help="Очистить сообщения в текущем диалоге", use_container_width=True):
            active_chat["messages"] = []
            update_active_messages(current_device_id, user_store, [])
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

    # --- CHAT CONTAINER ---
    st.markdown('<div class="stChatMessageContainer">', unsafe_allow_html=True)

    # Empty Chat Placeholder
    if not current_messages:
        cur_model_obj = next((m for m in free_models if m["id"] == selected_model_id), None)
        model_name = cur_model_obj["name"] if cur_model_obj else selected_model_id

        st.markdown(f"""
            <div class="empty-chat-placeholder">
                <div class="placeholder-title">Диалог пуст</div>
                <div class="placeholder-sub">
                    Подключена модель: {model_name}.<br>
                    История сохраняется в вашем браузере.
                </div>
            </div>
        """, unsafe_allow_html=True)

    # Render Messages
    for msg in current_messages:
        with st.chat_message(msg["role"]):
            if msg["role"] == "assistant" and msg.get("reasoning"):
                with st.expander("Рассуждения", expanded=False):
                    st.markdown(f"<div class='reasoning-text-minimal'>{msg['reasoning']}</div>", unsafe_allow_html=True)
            st.markdown(msg["content"])
            if msg["role"] == "assistant" and msg.get("gen_time"):
                st.markdown(f"<div class='msg-meta-time'>Время ответа: {msg['gen_time']}с</div>", unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # Chat Input & Streaming
    user_query = st.chat_input("Сообщение...")

    if user_query:
        # 1. Append User Message
        current_messages.append({"role": "user", "content": user_query})
        update_active_messages(current_device_id, user_store, current_messages)

        with st.chat_message("user"):
            st.markdown(user_query)

        # 2. Build Payload
        payload_messages = [
            {"role": m["role"], "content": m["content"]}
            for m in current_messages
        ]

        # 3. Stream Assistant Response with Timer
        with st.chat_message("assistant"):
            status_container = st.empty()
            reasoning_container = st.empty()
            content_container = st.empty()
            time_container = st.empty()

            status_container.markdown(
                '<div class="streaming-indicator-active"><span class="pulse-dot-mono"></span>Генерация ответа...</div>',
                unsafe_allow_html=True
            )

            start_time = time.time()
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
                        with st.expander("Рассуждения", expanded=True):
                            st.markdown(f"<div class='reasoning-text-minimal'>{full_reasoning}</div>", unsafe_allow_html=True)
                elif chunk_type == "content":
                    full_content += text
                    content_container.markdown(full_content + '<span class="streaming-cursor-mono"></span>', unsafe_allow_html=True)
                elif chunk_type == "error":
                    error_flag = True
                    content_container.error(text)
                    break

            gen_duration = round(time.time() - start_time, 1)
            status_container.empty()

            if not error_flag:
                if full_reasoning:
                    with reasoning_container.container():
                        with st.expander("Рассуждения", expanded=False):
                            st.markdown(f"<div class='reasoning-text-minimal'>{full_reasoning}</div>", unsafe_allow_html=True)

                content_container.markdown(full_content if full_content else "Ответ получен.")
                time_container.markdown(f"<div class='msg-meta-time'>Время ответа: {gen_duration}с</div>", unsafe_allow_html=True)

                assistant_msg = {
                    "role": "assistant",
                    "content": full_content,
                    "gen_time": gen_duration
                }
                if full_reasoning:
                    assistant_msg["reasoning"] = full_reasoning
                current_messages.append(assistant_msg)
                update_active_messages(current_device_id, user_store, current_messages)
