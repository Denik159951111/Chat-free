"""
Styles module: Premium Cyber-Editorial UI in the exact style of the reference image.
Deep matte obsidian black (#070709), Electric Acid Lime (#d4ff00) highlights,
Space Grotesk typography, watermark background, and ultra-smooth cubic-bezier physics.
"""

ASAP_EDITORIAL_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=Plus+Jakarta+Sans:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap');

:root {
    --bg-black: #060709;
    --bg-dark: #0a0b0f;
    --bg-surface: #101218;
    --bg-card: #131620;
    --bg-card-hover: #181c28;
    
    /* The exact electric acid lime from the reference */
    --acid-lime: #d4ff00;
    --acid-lime-dim: rgba(212, 255, 0, 0.12);
    --acid-lime-glow: rgba(212, 255, 0, 0.28);
    
    --border-subtle: rgba(255, 255, 255, 0.07);
    --border-mid: rgba(255, 255, 255, 0.14);
    --border-lime: #d4ff00;
    
    --text-pure: #ffffff;
    --text-muted: #838896;
    --text-dark: #4b5060;
    
    --font-heading: 'Space Grotesk', -apple-system, sans-serif;
    --font-body: 'Plus Jakarta Sans', -apple-system, sans-serif;
    --font-mono: 'JetBrains Mono', monospace;
    
    --ease-spring: cubic-bezier(0.16, 1, 0.3, 1);
}

/* Base Body and Streamlit App */
html, body, .stApp {
    background-color: var(--bg-black) !important;
    font-family: var(--font-body) !important;
    color: var(--text-pure) !important;
    overflow-x: hidden;
    letter-spacing: -0.015em;
    selection-background-color: var(--acid-lime);
    selection-color: #000000;
}

::selection {
    background: var(--acid-lime) !important;
    color: #000000 !important;
}

/* Subtle background grain & giant watermark text */
.stApp::before {
    content: "NEMOTRON";
    position: fixed;
    bottom: -4vw;
    left: 4vw;
    font-family: var(--font-heading);
    font-size: 19vw;
    font-weight: 800;
    color: rgba(255, 255, 255, 0.022);
    letter-spacing: -0.06em;
    pointer-events: none;
    z-index: 0;
    line-height: 0.8;
    user-select: none;
}

/* Clean Custom Scrollbars */
::-webkit-scrollbar {
    width: 5px;
    height: 5px;
}
::-webkit-scrollbar-track {
    background: var(--bg-black);
}
::-webkit-scrollbar-thumb {
    background: rgba(255, 255, 255, 0.14);
    border-radius: 2px;
}
::-webkit-scrollbar-thumb:hover {
    background: var(--acid-lime);
}

/* Streamlit Header & Navigation Bar Overrides */
header[data-testid="stHeader"] {
    background: transparent !important;
    border-bottom: 1px solid var(--border-subtle) !important;
    backdrop-filter: blur(20px);
}
#MainMenu, footer {
    visibility: hidden;
}

/* Top Navigation Bar in Reference Style */
.asap-navbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 1.1rem 0;
    border-bottom: 1px solid var(--border-subtle);
    margin-bottom: 2rem;
    position: relative;
    z-index: 10;
    animation: fadeInDown 0.7s var(--ease-spring);
}

.asap-logo-badge {
    background: var(--acid-lime);
    color: #000000;
    font-family: var(--font-heading);
    font-weight: 800;
    font-size: 0.85rem;
    padding: 0.35rem 0.8rem;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    border-radius: 2px;
    display: inline-flex;
    align-items: center;
    box-shadow: 0 0 20px var(--acid-lime-dim);
    transition: all 0.3s var(--ease-spring);
}
.asap-logo-badge:hover {
    box-shadow: 0 0 30px var(--acid-lime-glow);
    transform: translateY(-1px);
}

.asap-nav-links {
    display: flex;
    align-items: center;
    gap: 2.2rem;
}
.asap-nav-item {
    font-size: 0.82rem;
    font-weight: 500;
    color: var(--text-muted);
    letter-spacing: 0.02em;
    transition: color 0.25s ease;
    cursor: pointer;
    text-decoration: none;
}
.asap-nav-item:hover, .asap-nav-item.active {
    color: var(--text-pure);
}

.asap-top-actions {
    display: flex;
    align-items: center;
    gap: 0.9rem;
}
.asap-action-btn {
    width: 32px;
    height: 32px;
    border: 1px solid var(--border-subtle);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.8rem;
    color: var(--text-muted);
    border-radius: 2px;
    transition: all 0.25s var(--ease-spring);
}
.asap-action-btn:hover {
    border-color: var(--acid-lime);
    color: var(--acid-lime);
    box-shadow: 0 0 12px var(--acid-lime-dim);
}

/* Sidebar Custom Styling */
section[data-testid="stSidebar"] {
    background-color: #08090d !important;
    border-right: 1px solid var(--border-subtle) !important;
}
section[data-testid="stSidebar"] .block-container {
    padding-top: 1.5rem !important;
}

/* Reference Category Model List in Sidebar */
.model-list-container {
    display: flex;
    flex-direction: column;
    gap: 0.35rem;
    margin: 1.2rem 0;
}
.model-row-item {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0.55rem 0.8rem;
    font-size: 0.84rem;
    font-weight: 500;
    color: var(--text-muted);
    border-radius: 2px;
    cursor: pointer;
    transition: all 0.25s var(--ease-spring);
    border: 1px solid transparent;
}
.model-row-item:hover {
    color: var(--text-pure);
    background: rgba(255, 255, 255, 0.03);
    padding-left: 1rem;
}
.model-row-item.active {
    background: var(--acid-lime) !important;
    color: #000000 !important;
    font-weight: 700 !important;
    box-shadow: 0 0 20px var(--acid-lime-dim);
}
.model-row-item.active .model-ctx {
    color: #1a1a1a !important;
    font-weight: 600;
}
.model-ctx {
    font-family: var(--font-mono);
    font-size: 0.72rem;
    color: var(--text-dark);
}

/* Editorial Hero Section */
.editorial-hero {
    margin: 2rem 0 2.5rem 0;
    animation: fadeInUp 0.8s var(--ease-spring);
}
.editorial-hero-tag {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    font-family: var(--font-mono);
    font-size: 0.76rem;
    color: var(--acid-lime);
    text-transform: uppercase;
    letter-spacing: 0.12em;
    margin-bottom: 1.2rem;
}
.editorial-hero-title {
    font-family: var(--font-heading);
    font-size: 3.4rem;
    font-weight: 700;
    line-height: 1.08;
    letter-spacing: -0.04em;
    color: var(--text-pure);
    margin-bottom: 1.4rem;
}
.editorial-hero-desc {
    font-size: 1.05rem;
    color: var(--text-muted);
    line-height: 1.6;
    max-width: 620px;
    margin-bottom: 2rem;
    font-weight: 400;
}

/* Reference Slide Indicator (01 - 05 line in screenshot) */
.hero-meta-strip {
    display: flex;
    align-items: center;
    gap: 1.2rem;
    margin-top: 1.8rem;
}
.meta-line {
    width: 60px;
    height: 2px;
    background: var(--acid-lime);
    box-shadow: 0 0 10px var(--acid-lime-dim);
}
.meta-number {
    font-family: var(--font-mono);
    font-size: 0.8rem;
    color: var(--acid-lime);
    font-weight: 600;
}
.meta-label {
    font-size: 0.85rem;
    color: var(--text-pure);
    font-weight: 600;
    letter-spacing: -0.01em;
}

/* Interactive Prompt Chips in Reference Style */
.starter-grid-editorial {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 1rem;
    margin: 2.5rem 0;
    animation: fadeInUp 0.9s var(--ease-spring);
}

.starter-editorial-card {
    background: rgba(14, 16, 22, 0.7);
    border: 1px solid var(--border-subtle);
    border-radius: 4px;
    padding: 1.4rem;
    cursor: pointer;
    position: relative;
    overflow: hidden;
    transition: all 0.35s var(--ease-spring);
}
.starter-editorial-card::before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    width: 2px;
    height: 100%;
    background: var(--acid-lime);
    transform: scaleY(0);
    transition: transform 0.3s var(--ease-spring);
    transform-origin: bottom;
}
.starter-editorial-card:hover {
    background: #141722;
    border-color: rgba(212, 255, 0, 0.3);
    transform: translateY(-3px);
    box-shadow: 0 12px 30px rgba(0, 0, 0, 0.6), 0 0 25px rgba(212, 255, 0, 0.08);
}
.starter-editorial-card:hover::before {
    transform: scaleY(1);
}
.card-num {
    font-family: var(--font-mono);
    font-size: 0.74rem;
    color: var(--acid-lime);
    margin-bottom: 0.6rem;
}
.card-title {
    font-family: var(--font-heading);
    font-size: 1.05rem;
    font-weight: 600;
    color: var(--text-pure);
    margin-bottom: 0.4rem;
    letter-spacing: -0.02em;
}
.card-sub {
    font-size: 0.82rem;
    color: var(--text-muted);
    line-height: 1.45;
}

/* Chat Message Overrides */
div[data-testid="stChatMessage"] {
    background-color: transparent !important;
    padding: 1.3rem 0 !important;
    border-bottom: 1px solid rgba(255, 255, 255, 0.05) !important;
    animation: slideUpMessage 0.45s var(--ease-spring) forwards !important;
}

/* Assistant Message Container */
div[data-testid="stChatMessage"]:has([aria-label*="assistant"]) {
    background: rgba(13, 15, 21, 0.6) !important;
    border-left: 2px solid var(--acid-lime) !important;
    border-radius: 0 6px 6px 0 !important;
    padding: 1.4rem 1.6rem !important;
    margin: 0.9rem 0 !important;
    border-top: 1px solid rgba(255, 255, 255, 0.04) !important;
    border-right: 1px solid rgba(255, 255, 255, 0.04) !important;
    border-bottom: 1px solid rgba(255, 255, 255, 0.04) !important;
    box-shadow: 0 4px 24px rgba(0,0,0,0.35) !important;
}

/* User Message Container */
div[data-testid="stChatMessage"]:has([aria-label*="user"]) {
    background: rgba(24, 27, 36, 0.7) !important;
    border: 1px solid rgba(255, 255, 255, 0.09) !important;
    border-radius: 4px !important;
    padding: 1.2rem 1.5rem !important;
    margin: 0.9rem 0 !important;
}

/* Reasoning Disclosure Box */
div[data-testid="stExpander"] {
    background-color: #0b0d13 !important;
    border: 1px solid rgba(212, 255, 0, 0.18) !important;
    border-radius: 2px !important;
    margin: 0.8rem 0 !important;
    transition: all 0.3s var(--ease-spring);
}
div[data-testid="stExpander"]:hover {
    border-color: var(--acid-lime) !important;
}
div[data-testid="stExpander"] summary {
    font-family: var(--font-heading) !important;
    font-size: 0.86rem !important;
    color: var(--text-pure) !important;
    font-weight: 600 !important;
    letter-spacing: 0.02em !important;
}

.reasoning-text-block {
    font-family: var(--font-mono);
    font-size: 0.84rem;
    color: #9ba1b4;
    line-height: 1.65;
    background: #07080c;
    padding: 1rem 1.2rem;
    border-left: 2px solid var(--acid-lime);
    border-radius: 0 4px 4px 0;
}

/* Chat Input Bar */
div[data-testid="stChatInput"] {
    background: transparent !important;
    padding-bottom: 1.8rem !important;
}
div[data-testid="stChatInput"] > div {
    background-color: rgba(13, 15, 21, 0.85) !important;
    backdrop-filter: blur(24px) !important;
    border: 1px solid rgba(255, 255, 255, 0.12) !important;
    border-radius: 4px !important;
    box-shadow: 0 10px 40px rgba(0, 0, 0, 0.75) !important;
    transition: all 0.3s var(--ease-spring) !important;
}
div[data-testid="stChatInput"] > div:focus-within {
    border-color: var(--acid-lime) !important;
    box-shadow: 0 10px 40px rgba(0, 0, 0, 0.9), 0 0 25px var(--acid-lime-dim) !important;
}
div[data-testid="stChatInput"] textarea {
    color: var(--text-pure) !important;
    font-size: 0.96rem !important;
    font-family: var(--font-body) !important;
}
div[data-testid="stChatInput"] button {
    background-color: var(--acid-lime) !important;
    color: #000000 !important;
    border-radius: 2px !important;
    font-weight: 700 !important;
    transition: all 0.25s var(--ease-spring) !important;
}
div[data-testid="stChatInput"] button:hover {
    transform: scale(1.05) !important;
    box-shadow: 0 0 15px var(--acid-lime) !important;
}

/* Buttons in General */
.stButton > button {
    background-color: #12141c !important;
    border: 1px solid var(--border-subtle) !important;
    color: var(--text-pure) !important;
    font-family: var(--font-heading) !important;
    font-weight: 600 !important;
    border-radius: 2px !important;
    padding: 0.6rem 1.2rem !important;
    transition: all 0.3s var(--ease-spring) !important;
    letter-spacing: -0.01em !important;
}
.stButton > button:hover {
    background-color: #1a1e2a !important;
    border-color: var(--acid-lime) !important;
    color: var(--acid-lime) !important;
    box-shadow: 0 0 18px var(--acid-lime-dim) !important;
    transform: translateY(-2px);
}

/* Download Button */
.stDownloadButton > button {
    background-color: transparent !important;
    border: 1px solid var(--border-subtle) !important;
    color: var(--text-pure) !important;
    border-radius: 2px !important;
    font-family: var(--font-heading) !important;
    font-weight: 600 !important;
    transition: all 0.3s var(--ease-spring) !important;
}
.stDownloadButton > button:hover {
    border-color: var(--acid-lime) !important;
    color: var(--acid-lime) !important;
    box-shadow: 0 0 15px var(--acid-lime-dim) !important;
}

/* Streaming Blinking Cursor */
.streaming-cursor {
    display: inline-block;
    width: 8px;
    height: 18px;
    background-color: var(--acid-lime);
    margin-left: 4px;
    vertical-align: middle;
    animation: cursorBlink 0.8s infinite;
    box-shadow: 0 0 8px var(--acid-lime);
}

/* Animations */
@keyframes cursorBlink {
    0%, 100% { opacity: 1; }
    50% { opacity: 0; }
}

@keyframes fadeInDown {
    from {
        opacity: 0;
        transform: translateY(-15px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

@keyframes fadeInUp {
    from {
        opacity: 0;
        transform: translateY(20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

@keyframes slideUpMessage {
    from {
        opacity: 0;
        transform: translateY(16px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

/* Sticky Contact Tab on the right side like in the reference image */
.asap-side-tab {
    position: fixed;
    right: 0;
    top: 35%;
    background: var(--acid-lime);
    color: #000000;
    font-family: var(--font-heading);
    font-weight: 700;
    font-size: 0.78rem;
    padding: 0.5rem 0.9rem;
    writing-mode: vertical-rl;
    transform: rotate(180deg);
    letter-spacing: 0.05em;
    cursor: pointer;
    z-index: 100;
    box-shadow: -4px 0 20px var(--acid-lime-dim);
    transition: all 0.3s var(--ease-spring);
    border-radius: 0 3px 3px 0;
}
.asap-side-tab:hover {
    padding-bottom: 1.3rem;
    box-shadow: -4px 0 30px var(--acid-lime-glow);
}
</style>
"""
