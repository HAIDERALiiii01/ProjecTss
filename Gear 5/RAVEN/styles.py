EXAMPLES = [
    "Most popular AI Agent frameworks in 2026",
    "Most commercially successful Agentic AI implementations in 2026",
    "Celebrities who don't like cheese",
]

# Inline SVG raven (head in profile, glowing eye). To use your own image instead,
# replace the <svg>...</svg> block with: <img src="/gradio_api/file=raven.png" alt="RAVEN">
HEADER_HTML = """
<div class="dr-brand">
    <div class="dr-logo">
        <div class="dr-logo-glow"></div>
        <img src="/gradio_api/file=assets/raven.png" alt="RAVEN logo">
    </div>
    <div class="dr-titles">
        <h1>RAVEN</h1>
        <p>Hunt for knowledge. Deliver intelligence.</p>
    </div>
</div>
"""

CSS = """
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=Inter:wght@400;500;600&display=swap');

.gradio-container {
    --rv-bg: #05070d;
    --rv-surface: #0b1220;
    --rv-surface-2: #101a2e;
    --rv-line: #1b2b4a;
    --rv-blue: #2f8cff;
    --rv-cyan: #4cc9ff;
    --rv-deep: #0a2a5e;
    --rv-text: #e6efff;
    --rv-muted: #7a8aa8;

    max-width: 1080px !important;
    margin: 0 auto !important;
    padding: 2.5rem 2rem 4rem !important;
    background: transparent !important;
    color: var(--rv-text) !important;
    font-family: "Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif !important;
    position: relative;
    z-index: 1;
}

/* Page background: deep black with slow-moving blue light */
body, .gradio-container, gradio-app {
    background: var(--rv-bg, #05070d) !important;
}
body::before {
    content: "";
    position: fixed; inset: -20%;
    z-index: 0;
    pointer-events: none;
    background:
        radial-gradient(40% 35% at 20% 25%, rgba(47,140,255,0.18), transparent 70%),
        radial-gradient(35% 30% at 80% 70%, rgba(10,42,94,0.55), transparent 70%),
        radial-gradient(25% 25% at 60% 10%, rgba(76,201,255,0.10), transparent 70%);
    animation: rv-drift 26s ease-in-out infinite alternate;
}
#rv-stars { position: fixed; inset: 0; z-index: 0; pointer-events: none; }

@keyframes rv-drift {
    from { transform: translate3d(-3%, -2%, 0) scale(1); }
    to   { transform: translate3d(3%, 2%, 0) scale(1.08); }
}

/* === HEADER === */
.dr-brand {
    display: flex;
    align-items: center;
    gap: 1.5rem;
    padding-bottom: 1.4rem;
    margin-bottom: 2.5rem;
    border-bottom: 1px solid var(--rv-line);
    position: relative;
}
.dr-brand::after {
    content: "";
    position: absolute; left: 0; bottom: -1px;
    height: 2px; width: 100%;
    background: linear-gradient(90deg, var(--rv-blue), var(--rv-cyan) 40%, transparent);
    transform-origin: left;
    animation: rv-line-in 1.4s 0.3s cubic-bezier(.2,.8,.2,1) both;
}
@keyframes rv-line-in { from { transform: scaleX(0); } to { transform: scaleX(1); } }

.dr-logo { position: relative; width: 160px; height: 160px; flex: none; }
.dr-logo svg, .dr-logo img {
    position: relative; width: 100%; height: 100%;
    filter: drop-shadow(0 0 10px rgba(47,140,255,0.55));
    animation: rv-float 6s ease-in-out infinite;
}
.dr-logo-glow {
    position: absolute; inset: -14px;
    background: radial-gradient(circle, rgba(47,140,255,0.35), transparent 65%);
    animation: rv-pulse 4s ease-in-out infinite;
}
@keyframes rv-float { 0%,100% { transform: translateY(0) rotate(-1deg); } 50% { transform: translateY(-5px) rotate(1deg); } }
@keyframes rv-pulse { 0%,100% { opacity: .55; transform: scale(.95); } 50% { opacity: 1; transform: scale(1.08); } }

.dr-raven-body { stroke-dasharray: 220; stroke-dashoffset: 220; animation: rv-draw 1.8s ease-out forwards; }
.dr-raven-feather { stroke-dasharray: 90; stroke-dashoffset: 90; opacity: .75; animation: rv-draw 1.6s .9s ease-out forwards; }
@keyframes rv-draw { to { stroke-dashoffset: 0; } }

/* The eye ignites after the outline is drawn, then blinks now and then */
.dr-raven-eye {
    transform-box: fill-box; transform-origin: center;
    opacity: 0;
    filter: drop-shadow(0 0 4px #7fdcff);
    animation: rv-ignite .6s 1.6s ease-out forwards, rv-blink 7s 3s infinite;
}
@keyframes rv-ignite { from { opacity: 0; transform: scale(0); } to { opacity: 1; transform: scale(1); } }
@keyframes rv-blink { 0%, 94%, 100% { transform: scaleY(1); } 96% { transform: scaleY(.1); } }

.dr-titles h1 {
    font-family: "Syne", "Inter", sans-serif;
    font-size: clamp(2.2rem, 6vw, 3.6rem);
    font-weight: 800;
    letter-spacing: 0.14em;
    margin: 0;
    line-height: 1;
    background: linear-gradient(100deg, #e6efff 20%, var(--rv-cyan) 45%, var(--rv-blue) 55%, #e6efff 80%);
    background-size: 250% 100%;
    -webkit-background-clip: text; background-clip: text;
    -webkit-text-fill-color: transparent; color: transparent;
    animation: rv-shimmer 7s linear infinite;
}
@keyframes rv-shimmer { from { background-position: 100% 0; } to { background-position: -150% 0; } }

.dr-titles p {
    font-size: 0.95rem;
    letter-spacing: 0.04em;
    margin: 0.6rem 0 0;
    color: var(--rv-muted);
    overflow: hidden; white-space: nowrap;
    width: 0;
    animation: rv-type 2.4s 1s steps(38, end) forwards;
}
@keyframes rv-type { to { width: 100%; } }

/* === QUERY ROW === */
.dr-query-row { gap: 0 !important; align-items: stretch !important; }

#dr-query, #dr-query > div, #dr-query .wrap, #dr-query .form, #dr-query .block {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    padding: 0 !important;
    border-radius: 0 !important;
}

#dr-query textarea, #dr-query input {
    background: var(--rv-surface) !important;
    color: var(--rv-text) !important;
    border: 1.5px solid var(--rv-line) !important;
    border-radius: 12px 0 0 12px !important;
    padding: 1.05rem 1.25rem !important;
    font-size: 1.05rem !important;
    font-family: inherit !important;
    line-height: 1.45 !important;
    resize: none !important;
    min-height: 58px !important;
    box-shadow: inset 0 0 20px rgba(47,140,255,0.04) !important;
    transition: border-color .2s, box-shadow .2s !important;
}
#dr-query textarea:focus, #dr-query input:focus {
    outline: none !important;
    border-color: var(--rv-blue) !important;
    box-shadow: 0 0 0 3px rgba(47,140,255,0.22), 0 0 28px rgba(47,140,255,0.35) !important;
}
#dr-query textarea::placeholder, #dr-query input::placeholder { color: var(--rv-muted) !important; opacity: 1 !important; }

#dr-run {
    position: relative; overflow: hidden;
    background: linear-gradient(135deg, var(--rv-blue), #1456c8) !important;
    color: #fff !important;
    border: 1.5px solid var(--rv-blue) !important;
    border-left: none !important;
    border-radius: 0 12px 12px 0 !important;
    font-weight: 600 !important;
    letter-spacing: 0.08em !important;
    font-size: 0.95rem !important;
    box-shadow: 0 0 22px rgba(47,140,255,0.35) !important;
    min-width: 150px !important;
    padding: 1rem 1.5rem !important;
    transition: box-shadow .2s, transform .1s, filter .2s !important;
}
#dr-run::after {
    content: ""; position: absolute; top: 0; left: -60%;
    width: 40%; height: 100%;
    background: linear-gradient(100deg, transparent, rgba(255,255,255,0.35), transparent);
    transform: skewX(-20deg);
}
#dr-run:hover { box-shadow: 0 0 36px rgba(76,201,255,0.7) !important; filter: brightness(1.12); }
#dr-run:hover::after { left: 130%; transition: left .7s ease; }
#dr-run:active { transform: translateY(1px) scale(.99) !important; }

/* === EXAMPLES === */
.dr-examples-label {
    font-size: 0.85rem;
    color: var(--rv-muted);
    margin: 2rem 0 0.85rem 0;
    display: flex; align-items: center; gap: 0.85rem;
}
.dr-examples-label::after { content: ""; flex: 1; height: 1px; background: var(--rv-line); }

#dr-examples, #dr-examples > div, #dr-examples .wrap, #dr-examples .block {
    background: transparent !important; border: none !important; padding: 0 !important; box-shadow: none !important;
}
#dr-examples label, #dr-examples .label-wrap, #dr-examples > div > .label-wrap { display: none !important; }
#dr-examples table { border-collapse: separate !important; border-spacing: 0 !important; width: auto !important; background: transparent !important; border: none !important; }
#dr-examples thead { display: none !important; }
#dr-examples tbody { background: transparent !important; }
#dr-examples tr { background: transparent !important; display: flex !important; flex-wrap: wrap !important; gap: 10px !important; border: none !important; }

#dr-examples td, #dr-examples button {
    background: var(--rv-surface) !important;
    border: 1px solid var(--rv-line) !important;
    border-radius: 999px !important;
    padding: 0.65rem 1.15rem !important;
    cursor: pointer !important;
    font-size: 0.9rem !important;
    color: var(--rv-text) !important;
    margin: 0 !important;
    text-align: left !important;
    box-shadow: none !important;
    transition: border-color .2s, box-shadow .2s, transform .15s, color .2s !important;
}
#dr-examples td:hover, #dr-examples button:hover {
    border-color: var(--rv-cyan) !important;
    color: var(--rv-cyan) !important;
    box-shadow: 0 0 18px rgba(76,201,255,0.28) !important;
    transform: translateY(-2px);
}

/* === REPORT === */
#dr-report {
    margin-top: 2.5rem !important;
    padding: 0 !important;
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    color: var(--rv-text) !important;
    min-height: 40px;
}
#dr-report > div, #dr-report .prose { background: transparent !important; color: var(--rv-text) !important; }

#dr-report:not(:empty) {
    background: var(--rv-surface) !important;
    border: 1px solid var(--rv-line) !important;
    border-radius: 14px !important;
    padding: 1.75rem 2rem !important;
    box-shadow: 0 0 40px rgba(47,140,255,0.08) !important;
    animation: rv-rise .5s ease-out both;
}
@keyframes rv-rise { from { opacity: 0; transform: translateY(12px); } to { opacity: 1; transform: none; } }

/* While the agent is working, the report panel glows */
#dr-report.generating {
    animation: rv-hunt 1.6s ease-in-out infinite !important;
}
@keyframes rv-hunt {
    0%,100% { box-shadow: 0 0 10px rgba(47,140,255,0.15); border-color: var(--rv-line); }
    50%     { box-shadow: 0 0 34px rgba(76,201,255,0.45); border-color: var(--rv-cyan); }
}

#dr-report h1 {
    font-family: "Syne", "Inter", sans-serif;
    font-size: 1.9rem; font-weight: 800;
    color: var(--rv-cyan);
    border-bottom: 1px solid var(--rv-line);
    padding-bottom: 0.45rem;
    margin: 1.2rem 0 1rem;
}
#dr-report h2 { font-size: 1.35rem; color: var(--rv-blue); font-weight: 700; margin-top: 1.75rem; }
#dr-report h3 { font-size: 1.1rem; color: var(--rv-text); font-weight: 700; margin-top: 1.5rem; }
#dr-report p  { line-height: 1.7; }
#dr-report a  { color: var(--rv-cyan); text-decoration: underline; text-decoration-thickness: 1.5px; text-underline-offset: 3px; }
#dr-report a:hover { color: #fff; text-shadow: 0 0 10px var(--rv-cyan); }
#dr-report code { background: var(--rv-surface-2); border: 1px solid var(--rv-line); padding: 0.1rem 0.4rem; font-size: 0.92em; border-radius: 6px; }
#dr-report pre  { background: var(--rv-surface-2); border: 1px solid var(--rv-line); border-radius: 10px; padding: 1rem 1.25rem; }
#dr-report blockquote { border-left: 3px solid var(--rv-blue) !important; background: var(--rv-surface-2); padding: 1rem 1.25rem; margin: 1rem 0; border-radius: 0 10px 10px 0; }
#dr-report ul, #dr-report ol { padding-left: 1.5rem; }
#dr-report li { margin: 0.3rem 0; line-height: 1.6; }
#dr-report table { border-collapse: collapse; border: 1px solid var(--rv-line); }
#dr-report th, #dr-report td { border: 1px solid var(--rv-line); padding: 0.5rem 0.85rem; text-align: left; }
#dr-report th { background: var(--rv-surface-2); font-weight: 700; color: var(--rv-cyan); }

footer { display: none !important; }

@media (max-width: 700px) {
    .gradio-container { padding: 1.5rem 1rem 3rem !important; }
    dr-brand { flex-direction: column; align-items: flex-start; }
    .dr-logo { width: 130px; height: 130px; }
    .dr-query-row { flex-direction: column !important; }
    #dr-query textarea, #dr-query input { border-radius: 12px 12px 0 0 !important; }
    #dr-run { border-left: 1.5px solid var(--rv-blue) !important; border-radius: 0 0 12px 12px !important; width: 100% !important; }
}

@media (prefers-reduced-motion: reduce) {
    *, *::before, *::after { animation-duration: 0.01ms !important; animation-iteration-count: 1 !important; }
    .dr-titles p { width: 100%; }
}
"""

JS = """
() => {
    // RAVEN is dark-only
    document.body.classList.add('dark');

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

    // Drifting blue starfield behind everything
    if (document.getElementById('rv-stars')) return;
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
    const c = document.createElement('canvas');
    c.id = 'rv-stars';
    document.body.prepend(c);
    const ctx = c.getContext('2d');
    let w, h, stars;
    const init = () => {
        w = c.width = window.innerWidth;
        h = c.height = window.innerHeight;
        stars = Array.from({ length: Math.min(110, Math.floor(w * h / 14000)) }, () => ({
            x: Math.random() * w, y: Math.random() * h,
            r: Math.random() * 1.4 + 0.3,
            v: Math.random() * 0.25 + 0.05,
            a: Math.random() * Math.PI * 2,
        }));
    };
    const tick = () => {
        ctx.clearRect(0, 0, w, h);
        for (const s of stars) {
            s.y += s.v; s.a += 0.02;
            if (s.y > h) { s.y = -2; s.x = Math.random() * w; }
            ctx.globalAlpha = 0.25 + 0.5 * Math.abs(Math.sin(s.a));
            ctx.fillStyle = '#4cc9ff';
            ctx.beginPath(); ctx.arc(s.x, s.y, s.r, 0, 6.283); ctx.fill();
        }
        requestAnimationFrame(tick);
    };
    window.addEventListener('resize', init);
    init(); tick();
}
"""