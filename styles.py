"""
Styles module: Hyper-minimalist Telegram-style dark interface.
Strictly monochromatic black, charcoal, and dark graphite palette (Zero neon).
Smooth spring-physics animations for messages, dropdown, and inputs.
"""

TELEGRAM_DARK_MINIMAL_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

:root {
    --bg-main: #090a0d;
    --bg-header: rgba(9, 10, 13, 0.85);
    --bg-user-bubble: #252a37;
    --bg-bot-bubble: #13161f;
    --bg-input: #12141c;
    --bg-dropdown: #151822;
    --bg-dropdown-hover: #1f2331;
    
    --border-subtle: rgba(255, 255, 255, 0.07);
    --border-mid: rgba(255, 255, 255, 0.12);
    --border-focus: rgba(255, 255, 255, 0.28);
    
    --text-primary: #f4f5f8;
    --text-secondary: #8e93a3;
    --text-muted: #585d6e;
    
    --font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    --font-mono: 'JetBrains Mono', monospace;
    
    --ease-out: cubic-bezier(0.16, 1, 0.3, 1);
}

/* Global Application Reset */
html, body, .stApp {
    background-color: var(--bg-main) !important;
    font-family: var(--font-family) !important;
    color: var(--text-primary) !important;
    letter-spacing: -0.012em;
    overflow-x: hidden;
}

/* Clean Scrollbar */
::-webkit-scrollbar {
    width: 4px;
    height: 4px;
}
::-webkit-scrollbar-track {
    background: transparent;
}
::-webkit-scrollbar-thumb {
    background: rgba(255, 255, 255, 0.12);
    border-radius: 4px;
}
::-webkit-scrollbar-thumb:hover {
    background: rgba(255, 255, 255, 0.25);
}

/* Hide Default Streamlit Clutter */
header[data-testid="stHeader"] {
    display: none !important;
}
#MainMenu, footer {
    visibility: hidden;
}

/* Minimalist Top App Bar */
.tg-top-bar {
    position: sticky;
    top: 0;
    z-index: 1000;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0.8rem 1.2rem;
    background: var(--bg-header);
    backdrop-filter: blur(20px);
    border-bottom: 1px solid var(--border-subtle);
    margin: -1rem -1rem 1.5rem -1rem;
    animation: fadeInDown 0.35s var(--ease-out);
}

.tg-brand {
    display: flex;
    align-items: center;
    gap: 0.6rem;
}
.tg-brand-dot {
    width: 7px;
    height: 7px;
    background: #e2e5eb;
    border-radius: 50%;
    box-shadow: 0 0 8px rgba(255, 255, 255, 0.5);
    animation: gentlePulse 2.5s infinite var(--ease-out);
}
.tg-brand-title {
    font-size: 0.96rem;
    font-weight: 700;
    color: var(--text-primary);
    letter-spacing: -0.02em;
}

/* Smooth Animated Dropdown for Models */
div[data-baseweb="select"] {
    background: transparent !important;
}
div[data-baseweb="select"] > div {
    background: var(--bg-dropdown) !important;
    border: 1px solid var(--border-subtle) !important;
    border-radius: 12px !important;
    color: var(--text-primary) !important;
    font-size: 0.86rem !important;
    font-weight: 500 !important;
    padding: 0.1rem 0.4rem !important;
    min-height: 38px !important;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.25) !important;
    transition: all 0.25s var(--ease-out) !important;
}
div[data-baseweb="select"] > div:hover {
    background: var(--bg-dropdown-hover) !important;
    border-color: var(--border-mid) !important;
    transform: translateY(-1px);
}
div[data-baseweb="select"] > div:focus-within {
    border-color: var(--border-focus) !important;
    box-shadow: 0 0 0 2px rgba(255, 255, 255, 0.08) !important;
}

/* Dropdown Menu Popover Animation */
div[data-baseweb="popover"], ul[role="listbox"] {
    background: #141721 !important;
    border: 1px solid var(--border-mid) !important;
    border-radius: 12px !important;
    box-shadow: 0 12px 36px rgba(0, 0, 0, 0.65) !important;
    overflow: hidden !important;
    animation: dropdownPop 0.22s var(--ease-out) !important;
}
li[role="option"] {
    background: transparent !important;
    color: var(--text-secondary) !important;
    font-size: 0.86rem !important;
    padding: 0.6rem 0.9rem !important;
    transition: all 0.18s var(--ease-out) !important;
}
li[role="option"]:hover, li[aria-selected="true"] {
    background: #1e2230 !important;
    color: var(--text-primary) !important;
    padding-left: 1.1rem !important;
}

/* Telegram-Style Message Stream */
.stChatMessageContainer {
    max-width: 820px !important;
    margin: 0 auto !important;
}

div[data-testid="stChatMessage"] {
    background: transparent !important;
    padding: 0.45rem 0 !important;
    border: none !important;
    gap: 0.75rem !important;
}

/* Hide Default Streamlit Avatars for pure clean aesthetic */
div[data-testid="stChatMessage"] [data-testid="stChatMessageAvatarCustom"],
div[data-testid="stChatMessage"] [data-testid="chatAvatarIcon-user"],
div[data-testid="stChatMessage"] [data-testid="chatAvatarIcon-assistant"] {
    display: none !important;
}

/* User Message Bubble (Telegram Right-Oriented Bubble) */
div[data-testid="stChatMessage"]:has([aria-label*="user"]) {
    display: flex !important;
    justify-content: flex-end !important;
}
div[data-testid="stChatMessage"]:has([aria-label*="user"]) > div:last-child {
    background: var(--bg-user-bubble) !important;
    color: #ffffff !important;
    border-radius: 18px 18px 4px 18px !important;
    padding: 0.8rem 1.15rem !important;
    max-width: 78% !important;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.28) !important;
    animation: tgMessagePop 0.3s var(--ease-out) forwards !important;
    font-size: 0.94rem !important;
    line-height: 1.5 !important;
}

/* Assistant Message Bubble (Telegram Left-Oriented Bubble) */
div[data-testid="stChatMessage"]:has([aria-label*="assistant"]) {
    display: flex !important;
    justify-content: flex-start !important;
}
div[data-testid="stChatMessage"]:has([aria-label*="assistant"]) > div:last-child {
    background: var(--bg-bot-bubble) !important;
    border: 1px solid var(--border-subtle) !important;
    border-radius: 18px 18px 18px 4px !important;
    padding: 0.95rem 1.25rem !important;
    max-width: 85% !important;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.32) !important;
    animation: tgMessagePop 0.3s var(--ease-out) forwards !important;
    font-size: 0.94rem !important;
    line-height: 1.55 !important;
}

/* Telegram-Style Floating Capsule Chat Input Bar */
div[data-testid="stChatInput"] {
    background: transparent !important;
    padding-bottom: 1.4rem !important;
    max-width: 820px !important;
    margin: 0 auto !important;
}
div[data-testid="stChatInput"] > div {
    background: var(--bg-input) !important;
    backdrop-filter: blur(20px) !important;
    border: 1px solid var(--border-subtle) !important;
    border-radius: 26px !important;
    box-shadow: 0 8px 30px rgba(0, 0, 0, 0.5) !important;
    padding: 0.2rem 0.4rem !important;
    transition: all 0.25s var(--ease-out) !important;
}
div[data-testid="stChatInput"] > div:focus-within {
    border-color: var(--border-mid) !important;
    box-shadow: 0 10px 35px rgba(0, 0, 0, 0.7), 0 0 0 2px rgba(255, 255, 255, 0.06) !important;
    transform: translateY(-1px);
}
div[data-testid="stChatInput"] textarea {
    color: var(--text-primary) !important;
    font-size: 0.94rem !important;
    line-height: 1.4 !important;
    font-family: var(--font-family) !important;
}
div[data-testid="stChatInput"] button {
    background: #252a38 !important;
    color: #ffffff !important;
    border-radius: 50% !important;
    width: 34px !important;
    height: 34px !important;
    margin: auto 0.2rem !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    transition: all 0.2s var(--ease-out) !important;
}
div[data-testid="stChatInput"] button:hover {
    background: #363c50 !important;
    transform: scale(1.08) !important;
}

/* Minimalist Reasoning Accordion */
div[data-testid="stExpander"] {
    background: #0d0f15 !important;
    border: 1px solid var(--border-subtle) !important;
    border-radius: 10px !important;
    margin-bottom: 0.6rem !important;
}
div[data-testid="stExpander"] summary {
    font-size: 0.8rem !important;
    color: var(--text-secondary) !important;
    font-weight: 500 !important;
}
div[data-testid="stExpander"] summary:hover {
    color: var(--text-primary) !important;
}
.reasoning-text-minimal {
    font-family: var(--font-mono);
    font-size: 0.82rem;
    color: #848a9c;
    line-height: 1.55;
    padding: 0.6rem 0.8rem;
}

/* Code Blocks */
pre, code {
    font-family: var(--font-mono) !important;
}
div[data-testid="stChatMessage"] pre {
    background: #0a0c10 !important;
    border: 1px solid var(--border-subtle) !important;
    border-radius: 8px !important;
    padding: 0.85rem !important;
}

/* Minimal Buttons */
.stButton > button {
    background: #141720 !important;
    border: 1px solid var(--border-subtle) !important;
    color: var(--text-secondary) !important;
    border-radius: 10px !important;
    padding: 0.45rem 0.9rem !important;
    font-size: 0.82rem !important;
    font-weight: 500 !important;
    transition: all 0.2s var(--ease-out) !important;
}
.stButton > button:hover {
    background: #1c202d !important;
    color: #ffffff !important;
    border-color: var(--border-mid) !important;
}

/* Streaming Blinking Cursor */
.streaming-cursor-mono {
    display: inline-block;
    width: 6px;
    height: 15px;
    background: #8e93a3;
    margin-left: 3px;
    vertical-align: middle;
    animation: cursorFade 0.75s infinite ease-in-out;
}

/* Animations */
@keyframes tgMessagePop {
    0% {
        opacity: 0;
        transform: translateY(12px) scale(0.98);
    }
    100% {
        opacity: 1;
        transform: translateY(0) scale(1);
    }
}

@keyframes dropdownPop {
    0% {
        opacity: 0;
        transform: translateY(-8px) scale(0.97);
    }
    100% {
        opacity: 1;
        transform: translateY(0) scale(1);
    }
}

@keyframes fadeInDown {
    0% { opacity: 0; transform: translateY(-8px); }
    100% { opacity: 1; transform: translateY(0); }
}

@keyframes gentlePulse {
    0%, 100% { opacity: 0.4; }
    50% { opacity: 1; }
}

@keyframes cursorFade {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.15; }
}

/* Centered Minimal Empty State Placeholder */
.empty-chat-placeholder {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-height: 48vh;
    color: var(--text-muted);
    text-align: center;
    animation: fadeInDown 0.5s var(--ease-out);
}
.placeholder-icon {
    font-size: 2.2rem;
    margin-bottom: 0.6rem;
    opacity: 0.6;
}
.placeholder-title {
    font-size: 1.1rem;
    font-weight: 600;
    color: #b0b5c4;
    margin-bottom: 0.3rem;
}
.placeholder-sub {
    font-size: 0.84rem;
    color: var(--text-muted);
    max-width: 320px;
    line-height: 1.45;
}

/* HUB / LAUNCHER STYLES */
.hub-header {
    text-align: center;
    padding: 3rem 0 2rem 0;
    animation: fadeInDown 0.6s var(--ease-out);
}
.hub-title {
    font-size: 1.6rem;
    font-weight: 700;
    letter-spacing: -0.03em;
    color: var(--text-primary);
    margin-bottom: 0.4rem;
}
.hub-subtitle {
    font-size: 0.88rem;
    color: var(--text-secondary);
}

.hub-card {
    background: #11131b;
    border: 1px solid var(--border-subtle);
    border-radius: 14px;
    padding: 1.4rem 1.5rem;
    margin-bottom: 1.1rem;
    transition: all 0.28s var(--ease-out);
    position: relative;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.25);
}
.hub-card:hover {
    background: #171b26;
    border-color: var(--border-mid);
    transform: translateY(-3px);
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.45);
}

.hub-card-top {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 0.6rem;
}
.hub-card-icon-title {
    display: flex;
    align-items: center;
    gap: 0.6rem;
}
.hub-card-title {
    font-size: 1.05rem;
    font-weight: 600;
    color: var(--text-primary);
    letter-spacing: -0.015em;
}
.hub-card-desc {
    font-size: 0.82rem;
    color: var(--text-secondary);
    line-height: 1.45;
    margin-bottom: 1rem;
}

.hub-status-active {
    font-family: var(--font-mono);
    font-size: 0.68rem;
    color: #e2e5eb;
    background: #212533;
    border: 1px solid rgba(255, 255, 255, 0.12);
    border-radius: 4px;
    padding: 2px 7px;
    letter-spacing: 0.04em;
}
.hub-status-soon {
    font-family: var(--font-mono);
    font-size: 0.68rem;
    color: #585d6e;
    background: #12141c;
    border: 1px solid rgba(255, 255, 255, 0.05);
    border-radius: 4px;
    padding: 2px 7px;
    letter-spacing: 0.04em;
}

/* Return to Hub Button in Chat Top Bar */
.btn-back-hub button {
    background: transparent !important;
    border: 1px solid var(--border-subtle) !important;
    color: var(--text-secondary) !important;
    border-radius: 8px !important;
    padding: 0.25rem 0.6rem !important;
    font-size: 0.8rem !important;
    transition: all 0.2s var(--ease-out) !important;
}
.btn-back-hub button:hover {
    background: #1c202d !important;
    color: var(--text-primary) !important;
    border-color: var(--border-mid) !important;
}
</style>
"""
