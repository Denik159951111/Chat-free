import streamlit as st
from typing import List, Dict

from openrouter_client import fetch_free_models, stream_chat_completion
from styles import ASAP_EDITORIAL_CSS

# Configure Streamlit Page
st.set_page_config(
    page_title="ASAP // AI Intelligence Suite",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inject Cyber-Editorial CSS (ASAP Legal Aesthetic)
st.markdown(ASAP_EDITORIAL_CSS, unsafe_allow_html=True)

# System Presets
SYSTEM_PRESETS = {
    "⚡ Инновационный ассистент": (
        "Ты — высокоинтеллектуальный AI-ассистент экстра-класса. "
        "Твои ответы отличаются исключительной точностью, глубиной, структурностью и практической пользой. "
        "Пиши на безупречном русском языке, используя профессиональный тон и логическую ясность."
    ),
    "💻 IT & Software Architect": (
        "Ты — ведущий инженер и системный архитектор. Пиши production-ready, безопасный и масштабируемый код. "
        "Обязательно анализируй временную и пространственную сложность (Big O) и архитектурные компромиссы."
    ),
    "🧠 Deep Reasoning & Logic": (
        "Ты — эксперт по глубокому аналитическому, математическому и логическому анализу. "
        "Перед выдачей ответа сформулируй и протестируй гипотезы, покажи ход мысли и дай неопровержимый вывод."
    ),
    "📊 FinTech & Инвестиции": (
        "Ты — эксперт по инвестициям, финансовому анализу и FinTech. "
        "Структурируй выкладки, оценивай риски, предоставляй четкие метрики и расчеты."
    ),
    "🎯 Предельная лаконичность": (
        "Отвечай максимально кратко, ёмко и прямо в суть вопроса, без воды и вводных фраз."
    )
}

# Quick Topic Prompts (Matching the categories in the reference image)
EDITORIAL_TOPICS = {
    "IT разработка": "Разработай архитектуру распределенного сервиса с высокой отказоустойчивостью и минимальной задержкой. Опиши выбор технологий и паттернов.",
    "Blockchain": "Объясни принципы консенсуса Zero-Knowledge Rollups и их влияние на масштабируемость современных сетей.",
    "Инвестиции": "Сделай сравнительный анализ методов DCF (дисконтированных денежных потоков) и мультипликаторов для оценки технологических компаний.",
    "FinTech": "Спроектируй протокол безопасной обработки транзакций с защитой от фрода и соблюдением стандартов PCI DSS.",
    "Онлайн-сервисы": "Как построить масштабируемую систему персонализированных рекомендаций для SaaS-сервиса на миллион пользователей?",
    "GameDev": "Опиши реализацию сетевой синхронизации (клиент-серверное предсказание и интерполяция) для мультиплеерной игры.",
    "E-commerce": "Составь стратегию оптимизации воронки конверсии и архитектуру корзины заказов с учетом пиковых нагрузок.",
    "Киберспорт": "Разработай алгоритм подбора игроков (matchmaking) на основе модифицированного рейтинга Эло и скрытого MMR.",
    "Архитектура систем": "Опиши переход от монолита к событийной архитектуре (Event-Driven) с использованием Apache Kafka и CDC."
}

# Session State Initialization
if "messages" not in st.session_state:
    st.session_state.messages = []

if "quick_prompt" not in st.session_state:
    st.session_state.quick_prompt = None

if "selected_model_idx" not in st.session_state:
    st.session_state.selected_model_idx = 0

# Fetch free models (cached)
@st.cache_data(ttl=1800, show_spinner=False)
def get_cached_models():
    return fetch_free_models()

free_models = get_cached_models()

# Ensure default is NVIDIA Nemotron 3 Ultra (free)
default_idx = 0
for i, m in enumerate(free_models):
    if "nemotron-3-ultra" in m["id"].lower():
        default_idx = i
        break

if "selected_model_idx" not in st.session_state or st.session_state.selected_model_idx >= len(free_models):
    st.session_state.selected_model_idx = default_idx

current_model = free_models[st.session_state.selected_model_idx]

# --- SIDEBAR (Editorial Category Selector) ---
with st.sidebar:
    st.markdown("""
        <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 1.5rem;">
            <div class="asap-logo-badge">ASAP // AI</div>
            <div style="font-family: var(--font-mono); font-size: 0.7rem; color: #838896;">FREE SUITE</div>
        </div>
        <div style="font-family: var(--font-heading); font-size: 0.82rem; font-weight: 700; color: #ffffff; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 0.6rem;">
            Выбор нейросети
        </div>
    """, unsafe_allow_html=True)

    # Model selector radio with custom labels
    model_names = [f"{m['name']} ({m.get('provider', 'AI')})" for m in free_models]
    
    selected_name = st.radio(
        label="Нейросети:",
        options=model_names,
        index=st.session_state.selected_model_idx,
        label_visibility="collapsed"
    )

    # Update index if changed
    new_idx = model_names.index(selected_name)
    if new_idx != st.session_state.selected_model_idx:
        st.session_state.selected_model_idx = new_idx
        st.rerun()

    # Active Model Metadata Card
    cur_m = free_models[st.session_state.selected_model_idx]
    ctx_val = cur_m.get("context_length", 0)
    ctx_str = f"{ctx_val:,} токенов" if ctx_val else "Стандартный"

    st.markdown(f"""
        <div style="background: rgba(14, 16, 22, 0.9); border-left: 2px solid var(--acid-lime); padding: 0.8rem 1rem; margin: 1rem 0; border-radius: 0 4px 4px 0;">
            <div style="display: flex; justify-content: space-between; font-size: 0.72rem; color: var(--text-muted); margin-bottom: 0.3rem;">
                <span>ПРОВАЙДЕР: <b style="color: #fff;">{cur_m.get('provider', 'NVIDIA')}</b></span>
                <span>КОНТЕКСТ: <b style="color: var(--acid-lime);">{ctx_str}</b></span>
            </div>
            <div style="font-size: 0.75rem; color: #787e91; line-height: 1.4;">
                {cur_m.get('description', '')[:130]}...
            </div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("<hr style='border-color: rgba(255,255,255,0.06); margin: 1.2rem 0;'>", unsafe_allow_html=True)

    # Presets Selection
    st.markdown("<div style='font-family: var(--font-heading); font-size: 0.8rem; font-weight: 700; color: #fff; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 0.5rem;'>Режим диалога</div>", unsafe_allow_html=True)
    preset_key = st.selectbox(
        "Пресет:",
        options=list(SYSTEM_PRESETS.keys()),
        label_visibility="collapsed"
    )

    system_prompt = st.text_area(
        "Системные инструкции:",
        value=SYSTEM_PRESETS[preset_key],
        height=85
    )

    with st.expander("🎚️ Параметры генерации", expanded=False):
        temperature = st.slider("Температура (Creative)", 0.0, 1.5, 0.7, 0.05)
        max_tokens = st.slider("Максимум токенов", 256, 8192, 4096, 256)

    st.markdown("<hr style='border-color: rgba(255,255,255,0.06); margin: 1.2rem 0;'>", unsafe_allow_html=True)

    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        if st.button("🗑️ Очистить", use_container_width=True):
            st.session_state.messages = []
            st.session_state.quick_prompt = None
            st.rerun()

    with col_btn2:
        export_text = f"# ASAP // AI Chat Export\n\nМодель: {cur_m['id']}\n\n---\n\n"
        for msg in st.session_state.messages:
            role = "Пользователь" if msg["role"] == "user" else "ASAP AI"
            export_text += f"### {role}:\n{msg['content']}\n\n"

        st.download_button(
            label="📥 Экспорт",
            data=export_text,
            file_name="asap_ai_chat.md",
            mime="text/markdown",
            use_container_width=True
        )

    st.markdown("""
        <div style="margin-top: 1.5rem; font-family: var(--font-mono); font-size: 0.68rem; color: #525866; display: flex; align-items: center; gap: 6px;">
            <span style="width: 6px; height: 6px; background: var(--acid-lime); border-radius: 50%; box-shadow: 0 0 6px var(--acid-lime);"></span>
            <span>OPENROUTER GATEWAY // ONLINE</span>
        </div>
    """, unsafe_allow_html=True)


# --- TOP NAVIGATION BAR (Exact reference aesthetic) ---
st.markdown(f"""
    <div class="asap-navbar">
        <div class="asap-logo-badge">ASAP // AI</div>
        <div class="asap-nav-links">
            <span class="asap-nav-item active">Нейросети</span>
            <span class="asap-nav-item">Для кого</span>
            <span class="asap-nav-item">О моделях</span>
            <span class="asap-nav-item">API Статус</span>
        </div>
        <div class="asap-top-actions">
            <span style="font-family: var(--font-mono); font-size: 0.8rem; color: #8e94a4; margin-right: 0.6rem;">
                +7 (950) 033-02-20
            </span>
            <div class="asap-action-btn">💬</div>
            <div class="asap-action-btn">✈️</div>
            <div class="asap-action-btn">✉️</div>
        </div>
    </div>
    <div class="asap-side-tab">Напишите нам</div>
""", unsafe_allow_html=True)


# --- MAIN VIEW ---

if not st.session_state.messages:
    # HERO SECTION IN EXACT REFERENCE STYLE
    hero_col_left, hero_col_right = st.columns([1.3, 0.9])

    with hero_col_left:
        st.markdown("""
            <div class="editorial-hero">
                <div class="editorial-hero-tag">
                    <span style="display:inline-block; width:6px; height:6px; background:var(--acid-lime); border-radius:50%;"></span>
                    NVIDIA NEMOTRON 3 ULTRA // 550B MoE
                </div>
                <h1 class="editorial-hero-title">
                    Инновационный<br>подход для бизнеса
                </h1>
                <p class="editorial-hero-desc">
                    Доступ к нейросетям высокого класса: передовые алгоритмы рассуждений,
                    глубокий аудит кода, разработка архитектуры и бизнес-аналитика без ограничений.
                </p>
                <div class="hero-meta-strip">
                    <div class="meta-number">01</div>
                    <div class="meta-line"></div>
                    <div class="meta-number">05</div>
                    <span class="meta-label">← Выберите направление справа или введите запрос внизу</span>
                </div>
            </div>
        """, unsafe_allow_html=True)

    with hero_col_right:
        st.markdown("<div style='margin-top: 1.2rem;'>", unsafe_allow_html=True)
        # Category buttons matching the reference image vertical stack
        for topic_name, prompt_content in EDITORIAL_TOPICS.items():
            # Highlight 'Онлайн-сервисы' or active topic in yellow/lime style
            is_highlighted = (topic_name == "Онлайн-сервисы")
            btn_label = f"⚡ {topic_name}" if is_highlighted else topic_name
            
            if st.button(btn_label, key=f"topic_{topic_name}", use_container_width=True):
                st.session_state.quick_prompt = prompt_content
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    # 4 Bottom Editorial Feature Cards
    st.markdown("""
        <div class="starter-grid-editorial">
            <div class="starter-editorial-card">
                <div class="card-num">01 // CODE ARCHITECTURE</div>
                <div class="card-title">Оптимизация и аудит алгоритмов</div>
                <div class="card-sub">Асимптотический анализ Big-O, поиск узких мест и рефакторинг высоконагруженных систем.</div>
            </div>
            <div class="starter-editorial-card">
                <div class="card-num">02 // DEEP REASONING</div>
                <div class="card-title">Пошаговое логическое рассуждение</div>
                <div class="card-sub">Анализ сложных логических парадоксов, математических теорем и бизнес-гипотез.</div>
            </div>
            <div class="starter-editorial-card">
                <div class="card-num">03 // SYSTEM DESIGN</div>
                <div class="card-title">Проектирование микросервисов</div>
                <div class="card-sub">Отказоустойчивость, распределенные базы данных, шардинг и шины событий.</div>
            </div>
            <div class="starter-editorial-card">
                <div class="card-num">04 // LEGAL & SPECS</div>
                <div class="card-title">Составление ТЗ и спецификаций</div>
                <div class="card-sub">Формирование документации, технических требований и архитектурных планов.</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

else:
    # Minimal active chat header
    st.markdown(f"""
        <div style="display: flex; align-items: center; justify-content: space-between; padding: 0.6rem 0; margin-bottom: 1.5rem; border-bottom: 1px solid var(--border-subtle);">
            <div style="display: flex; align-items: center; gap: 10px;">
                <span style="font-family: var(--font-mono); font-size: 0.74rem; color: var(--acid-lime);">ДИАЛОГ АКТИВЕН //</span>
                <span style="font-family: var(--font-heading); font-size: 0.95rem; font-weight: 700; color: #ffffff;">{cur_m['name']}</span>
            </div>
            <div style="font-family: var(--font-mono); font-size: 0.72rem; color: #767c8d;">
                СООБЩЕНИЙ: <span style="color: var(--acid-lime);">{len(st.session_state.messages)}</span>
            </div>
        </div>
    """, unsafe_allow_html=True)


# Render Chat History
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        if msg["role"] == "assistant" and msg.get("reasoning"):
            with st.expander("🧠 Ход рассуждений (Reasoning)", expanded=False):
                st.markdown(f"<div class='reasoning-text-block'>{msg['reasoning']}</div>", unsafe_allow_html=True)
        st.markdown(msg["content"])


# Handle Chat Input (Field or Topic Click)
chat_input_val = st.chat_input("Напишите ваш вопрос или задачу...")

active_prompt = None
if st.session_state.quick_prompt:
    active_prompt = st.session_state.quick_prompt
    st.session_state.quick_prompt = None
elif chat_input_val:
    active_prompt = chat_input_val

if active_prompt:
    # 1. User Message
    st.session_state.messages.append({"role": "user", "content": active_prompt})
    with st.chat_message("user"):
        st.markdown(active_prompt)

    # 2. Build Payload
    messages_payload = []
    if system_prompt and system_prompt.strip():
        messages_payload.append({"role": "system", "content": system_prompt.strip()})

    for m in st.session_state.messages:
        messages_payload.append({"role": m["role"], "content": m["content"]})

    # 3. Stream Assistant Response
    with st.chat_message("assistant"):
        reasoning_box = st.empty()
        content_box = st.empty()

        accumulated_content = ""
        accumulated_reasoning = ""
        has_error = False

        stream = stream_chat_completion(
            model=cur_m["id"],
            messages=messages_payload,
            temperature=temperature,
            max_tokens=max_tokens
        )

        for chunk_type, text in stream:
            if chunk_type == "reasoning":
                accumulated_reasoning += text
                with reasoning_box.container():
                    with st.expander("🧠 Ход рассуждений (Reasoning)", expanded=True):
                        st.markdown(f"<div class='reasoning-text-block'>{accumulated_reasoning}</div>", unsafe_allow_html=True)
            elif chunk_type == "content":
                accumulated_content += text
                content_box.markdown(accumulated_content + '<span class="streaming-cursor"></span>', unsafe_allow_html=True)
            elif chunk_type == "error":
                has_error = True
                content_box.error(text)
                break

        if not has_error:
            if accumulated_reasoning:
                with reasoning_box.container():
                    with st.expander("🧠 Ход рассуждений (Reasoning)", expanded=False):
                        st.markdown(f"<div class='reasoning-text-block'>{accumulated_reasoning}</div>", unsafe_allow_html=True)

            content_box.markdown(accumulated_content if accumulated_content else "_Ответ получен._")

            assistant_record = {"role": "assistant", "content": accumulated_content}
            if accumulated_reasoning:
                assistant_record["reasoning"] = accumulated_reasoning
            st.session_state.messages.append(assistant_record)
