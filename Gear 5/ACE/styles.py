EXAMPLES = [
    "Most popular AI Agent frameworks in 2026",
    "Most commercially successful Agentic AI implementations in 2026",
    "Most anticipated movies of 2027",
    "Best way to start learning python in 2026",
]

# The logo already contains the name and tagline, so the header is just the image.
# Put the file at assets/ace.png (app.py allows the "assets" folder).
HEADER_HTML = """
<div class="dr-brand">
    <div class="dr-logo">
        <img src="/gradio_api/file=assets/ace.png" alt="Ace Ventura: The Digital Detective. Alrighty then, let's investigate!">
    </div>
</div>
"""

# Palette pulled from the logo:
#   sun yellow (circle), signal red (title), ink black (outlines),
#   Hawaiian blue + teal (shirt, magnifier glass), orange (hibiscus), cream (paper)
CSS = """
@import url('https://fonts.googleapis.com/css2?family=Bangers&family=Nunito:wght@400;600;700;800&display=swap');

:root, .gradio-container {
    --av-yellow: #ffc907;
    --av-yellow-soft: #ffe27a;
    --av-red: #e0170f;
    --av-red-hot: #ff3b2f;
    --av-ink: #0d0b14;
    --av-blue: #2b6cb0;
    --av-teal: #35b6d6;
    --av-orange: #f4811f;
    --av-cream: #fff6d6;
    --av-paper: #fffdf3;
    --av-shadow: 5px 5px 0 var(--av-ink);
}

.gradio-container {
    max-width: 1080px !important;
    margin: 0 auto !important;
    padding: 0.5rem 2rem 5rem !important;
    background: transparent !important;
    color: var(--av-ink) !important;
    font-family: "Nunito", -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif !important;
    position: relative;
    z-index: 1;
}

/* Page background: sunny yellow with a comic halftone */
body, gradio-app, .gradio-container {
    background-color: var(--av-yellow) !important;
    background-image: radial-gradient(rgba(13,11,20,0.14) 1.3px, transparent 1.6px) !important;
    background-size: 18px 18px !important;
}

/* Palm silhouettes in the bottom corners, like the logo's circle */
body::before, body::after {
    content: "";
    position: fixed; bottom: -10px;
    width: 230px; height: 310px;
    z-index: 0; pointer-events: none;
    opacity: 0.2;
    background: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 220 300'><g fill='%230d0b14'><path d='M96 300 C100 220 104 170 112 110 L121 110 C114 170 113 230 114 300Z'/><path d='M116 110 C90 60 50 50 15 70 C55 65 90 80 116 110Z'/><path d='M116 110 C80 90 40 100 12 135 C50 115 85 112 116 110Z'/><path d='M116 110 C130 55 170 40 205 55 C168 58 140 80 116 110Z'/><path d='M116 110 C150 85 190 95 215 130 C180 110 148 108 116 110Z'/><path d='M116 110 C100 50 105 20 120 0 C122 35 122 70 116 110Z'/></g></svg>") no-repeat bottom / contain;
}
body::before { left: 0; }
body::after  { right: 0; transform: scaleX(-1); }

/* === HEADER === */
.dr-brand {
    display: flex;
    justify-content: center;
    margin: -0.80rem 0 -0.30rem;
}
.dr-logo { width: min(350px, 88vw); flex: none; }
.dr-logo img {
    display: block; width: 100%; height: auto;
    transform-origin: 50% 90%;
    animation: av-pop 0.9s cubic-bezier(.2,1.4,.4,1) both;
    transition: transform .25s;
}
.dr-logo img:hover { transform: rotate(-2deg) scale(1.03); }

/* The one orchestrated moment: the logo pops in like a sticker slapped on the page */
@keyframes av-pop {
    0%   { opacity: 0; transform: scale(.4) rotate(-8deg); }
    60%  { opacity: 1; transform: scale(1.06) rotate(2deg); }
    100% { opacity: 1; transform: scale(1) rotate(0); }
}

/* === QUERY ROW === */
.dr-query-row {
    gap: 0 !important;
    align-items: stretch !important;
    border-radius: 16px;
    box-shadow: var(--av-shadow);
}

#dr-query, #dr-query > div, #dr-query .wrap, #dr-query .form, #dr-query .block {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    padding: 0 !important;
    border-radius: 0 !important;
}

#dr-query textarea, #dr-query input {
    background: var(--av-paper) !important;
    color: var(--av-ink) !important;
    border: 3px solid var(--av-ink) !important;
    border-radius: 16px 0 0 16px !important;
    padding: 1.05rem 1.25rem !important;
    font-size: 1.1rem !important;
    font-weight: 600 !important;
    font-family: inherit !important;
    line-height: 1.45 !important;
    resize: none !important;
    min-height: 62px !important;
    box-shadow: none !important;
    transition: background .2s, box-shadow .2s !important;
}
#dr-query textarea:focus, #dr-query input:focus {
    outline: none !important;
    background: #fff !important;
    box-shadow: inset 0 0 0 3px var(--av-teal) !important;
}
#dr-query textarea::placeholder, #dr-query input::placeholder {
    color: #6b6450 !important; opacity: 1 !important; font-weight: 600 !important;
}

#dr-run {
    background: var(--av-red) !important;
    color: #fff !important;
    border: 3px solid var(--av-ink) !important;
    border-radius: 0 16px 16px 0 !important;
    font-family: "Bangers", "Nunito", sans-serif !important;
    font-weight: 400 !important;
    letter-spacing: 0.08em !important;
    font-size: 1.5rem !important;
    text-shadow: 2px 2px 0 var(--av-ink);
    box-shadow: none !important;
    min-width: 170px !important;
    padding: 1rem 1.5rem !important;
    transition: background .15s, transform .1s !important;
}
#dr-run:hover { background: var(--av-red-hot) !important; }
#dr-run:active { transform: translate(2px, 2px) !important; }

/* Visible keyboard focus */
#dr-run:focus-visible, #dr-examples button:focus-visible {
    outline: 3px solid var(--av-blue) !important;
    outline-offset: 3px !important;
}

/* === EXAMPLES === */
.dr-examples-label {
    font-family: "Bangers", "Nunito", sans-serif;
    font-size: 1.4rem;
    letter-spacing: 0.06em;
    color: var(--av-ink);
    margin: 2.25rem 0 0.9rem 0;
    display: flex; align-items: center; gap: 0.85rem;
}
.dr-examples-label::after {
    content: ""; flex: 1; height: 0;
    border-top: 3px dashed var(--av-ink);
}

#dr-examples, #dr-examples > div, #dr-examples .wrap, #dr-examples .block {
    background: transparent !important; border: none !important; padding: 0 !important; box-shadow: none !important;
}
#dr-examples label, #dr-examples .label-wrap, #dr-examples > div > .label-wrap { display: none !important; }
#dr-examples table { border-collapse: separate !important; border-spacing: 0 !important; width: auto !important; background: transparent !important; border: none !important; }
#dr-examples thead { display: none !important; }
#dr-examples tbody { background: transparent !important; }
#dr-examples tr { background: transparent !important; display: flex !important; flex-wrap: wrap !important; gap: 12px !important; border: none !important; }

#dr-examples td, #dr-examples button {
    background: var(--av-cream) !important;
    border: 2.5px solid var(--av-ink) !important;
    border-radius: 999px !important;
    padding: 0.6rem 1.15rem !important;
    cursor: pointer !important;
    font-size: 0.95rem !important;
    font-weight: 700 !important;
    color: var(--av-ink) !important;
    margin: 0 !important;
    text-align: left !important;
    box-shadow: 3px 3px 0 var(--av-ink) !important;
    transition: background .15s, color .15s, box-shadow .15s, transform .15s !important;
}
#dr-examples td:hover, #dr-examples button:hover {
    background: var(--av-blue) !important;
    color: #fff !important;
    box-shadow: 5px 5px 0 var(--av-ink) !important;
    transform: translate(-2px, -2px) rotate(-1deg);
}

/* === REPORT === */
#dr-report {
    margin-top: 2.5rem !important;
    padding: 0 !important;
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    color: var(--av-ink) !important;
    min-height: 40px;
}
#dr-report > div, #dr-report .prose { background: transparent !important; color: var(--av-ink) !important; }
#dr-report .prose *, #dr-report p, #dr-report li { color: var(--av-ink); }

#dr-report:not(:empty) {
    background: var(--av-paper) !important;
    border: 3px solid var(--av-ink) !important;
    border-radius: 18px !important;
    padding: 1.75rem 2rem !important;
    box-shadow: 8px 8px 0 var(--av-ink) !important;
}

/* While the agent is working, the shadow flashes red/blue like a case light */
#dr-report.generating {
    animation: av-case 1.1s steps(2, end) infinite !important;
}
@keyframes av-case {
    0%   { box-shadow: 8px 8px 0 var(--av-red); }
    50%  { box-shadow: 8px 8px 0 var(--av-blue); }
    100% { box-shadow: 8px 8px 0 var(--av-red); }
}

#dr-report h1 {
    font-family: "Bangers", "Nunito", sans-serif;
    font-size: 2.4rem; font-weight: 400;
    letter-spacing: 0.04em;
    color: var(--av-red);
    text-shadow: 2px 2px 0 var(--av-ink);
    border-bottom: 3px solid var(--av-ink);
    padding-bottom: 0.4rem;
    margin: 1.2rem 0 1rem;
}
#dr-report h2 {
    font-family: "Bangers", "Nunito", sans-serif;
    font-size: 1.7rem; font-weight: 400; letter-spacing: 0.04em;
    color: var(--av-blue); margin-top: 1.75rem;
}
#dr-report h3 { font-size: 1.15rem; color: var(--av-ink); font-weight: 800; margin-top: 1.5rem; }
#dr-report p  { line-height: 1.7; font-size: 1.02rem; }
#dr-report a  { color: var(--av-blue); font-weight: 700; text-decoration: underline; text-decoration-thickness: 2px; text-underline-offset: 3px; }
#dr-report a:hover { color: var(--av-red); }
#dr-report code { background: var(--av-yellow-soft); border: 1.5px solid var(--av-ink); padding: 0.1rem 0.4rem; font-size: 0.92em; border-radius: 6px; color: var(--av-ink); }
#dr-report pre  { background: var(--av-ink); border: 3px solid var(--av-ink); border-radius: 10px; padding: 1rem 1.25rem; }
#dr-report pre code { background: transparent; border: none; color: var(--av-cream); }
#dr-report blockquote { border-left: 6px solid var(--av-red) !important; background: var(--av-yellow-soft); padding: 1rem 1.25rem; margin: 1rem 0; border-radius: 0 10px 10px 0; }
#dr-report ul, #dr-report ol { padding-left: 1.5rem; }
#dr-report li { margin: 0.3rem 0; line-height: 1.6; }
#dr-report table { border-collapse: collapse; border: 2.5px solid var(--av-ink); }
#dr-report th, #dr-report td { border: 2px solid var(--av-ink); padding: 0.5rem 0.85rem; text-align: left; }
#dr-report th { background: var(--av-yellow); font-weight: 800; color: var(--av-ink); }

footer { display: none !important; }

@media (max-width: 900px) {
    body::before, body::after { display: none; }
}

@media (max-width: 700px) {
    .gradio-container { padding: 1.25rem 1rem 3rem !important; }
    .dr-query-row { flex-direction: column !important; }
    #dr-query textarea, #dr-query input { border-radius: 16px 16px 0 0 !important; }
    #dr-run { border-radius: 0 0 16px 16px !important; width: 100% !important; border-top: none !important; }
    #dr-report:not(:empty) { padding: 1.25rem 1.1rem !important; }
}

@media (prefers-reduced-motion: reduce) {
    *, *::before, *::after { animation-duration: 0.01ms !important; animation-iteration-count: 1 !important; transition-duration: 0.01ms !important; }
}
"""

JS = """
() => {
    // This theme is light-only: keep Gradio out of dark mode
    const forceLight = () => document.body.classList.remove('dark');
    forceLight();
    new MutationObserver(forceLight).observe(document.body, { attributes: true, attributeFilter: ['class'] });

    // Focus the query box
    const focus = () => {
        const el = document.querySelector("#dr-query textarea, #dr-query input");
        if (el) { el.focus(); return true; }
        return false;
    };
    if (!focus()) {
        let tries = 0;
        const i = setInterval(() => { if (focus() || ++tries > 20) clearInterval(i); }, 100);
    }
}
"""