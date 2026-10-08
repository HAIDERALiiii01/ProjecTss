"""Styling constants for the digital twin Gradio app — hacker / matrix theme."""

# Palette (single source of truth; keep in sync with the CSS variables below)
GREEN = "#00ff41"       # matrix green (primary)
DIM_GREEN = "#00a82b"   # secondary / borders
DEEP_GREEN = "#0a2e14"  # tinted surfaces
BLACK = "#020604"

# Backwards-compatible aliases so existing imports don't break
GOLD = GREEN
BLUE = DIM_GREEN
PURPLE = DEEP_GREEN

EXAMPLES = [
    "Tell me about your background and experience.",
    "What kinds of projects are you working on now?",
    "What are your strongest technical skills?",
    "How can I get in touch with you?",
]

CSS = """
:root {
  --hx-green: #00ff41;
  --hx-green-dim: #00a82b;
  --hx-green-deep: #0a2e14;
  --hx-bg: #020604;
  --hx-surface: rgba(4, 14, 8, 0.88);
  --hx-surface-2: rgba(8, 26, 14, 0.92);
  --hx-border: #0f4d22;
  --hx-border-strong: #00a82b;
  --hx-text: #b9ffcb;
  --hx-muted: #4f8f65;
  --hx-glow: 0 0 6px rgba(0, 255, 65, 0.55), 0 0 18px rgba(0, 255, 65, 0.25);
  --hx-mono: 'JetBrains Mono', 'Fira Code', 'SF Mono', Menlo, Consolas, monospace;
}

/* Hacker mode is always dark — ignore Gradio's light/dark toggle */
footer, .built-with, .show-api, .api-docs { display: none !important; }

html, body { background: var(--hx-bg) !important; }
gradio-app { background: transparent !important; }

/* ---------- CRT overlay: scanlines + vignette + subtle flicker ---------- */
body::before {
  content: "";
  position: fixed;
  inset: 0;
  pointer-events: none;
  z-index: 9999;
  background: repeating-linear-gradient(
    to bottom,
    rgba(0, 0, 0, 0) 0px,
    rgba(0, 0, 0, 0) 2px,
    rgba(0, 0, 0, 0.22) 3px,
    rgba(0, 0, 0, 0) 4px
  );
  animation: hx-flicker 6s infinite;
}
body::after {
  content: "";
  position: fixed;
  inset: 0;
  pointer-events: none;
  z-index: 9998;
  background: radial-gradient(ellipse at center, rgba(0,0,0,0) 55%, rgba(0,0,0,0.75) 100%);
}
/* a faint bright bar that sweeps down the screen like a CRT refresh */
.hx-sweep {
  position: fixed;
  left: 0; right: 0; top: -20%;
  height: 18%;
  pointer-events: none;
  z-index: 9997;
  background: linear-gradient(to bottom, rgba(0,255,65,0), rgba(0,255,65,0.05), rgba(0,255,65,0));
  animation: hx-sweep 7s linear infinite;
}
#hx-rain {
  position: fixed;
  inset: 0;
  width: 100vw;
  height: 100vh;
  z-index: 0;
  pointer-events: none;
  opacity: 0.16;
}

@keyframes hx-flicker {
  0%, 100% { opacity: 1; }
  92% { opacity: 1; }
  93% { opacity: 0.82; }
  94% { opacity: 1; }
  97% { opacity: 0.9; }
}
@keyframes hx-sweep {
  from { transform: translateY(0); }
  to   { transform: translateY(700%); }
}

/* ---------- Stable layout ---------- */
.gradio-container {
  position: relative !important;
  z-index: 1 !important;
  background: transparent !important;
  color: var(--hx-text) !important;
  font-family: var(--hx-mono) !important;
  width: 100% !important;
  max-width: 880px !important;
  min-width: 0 !important;
  margin: 0 auto !important;
  padding: 32px 24px 48px !important;
}
.gradio-container .main, .gradio-container .contain, .gradio-container .wrap {
  width: 100% !important;
  max-width: 100% !important;
  min-width: 0 !important;
}
.gradio-container * { min-width: 0; }

/* ---------- Title: prompt prefix, reveal, glitch, blinking cursor ---------- */
.gradio-container h1 {
  position: relative;
  color: var(--hx-green) !important;
  font-family: var(--hx-mono) !important;
  font-size: 26px !important;
  font-weight: 700 !important;
  letter-spacing: 0.04em !important;
  text-shadow: var(--hx-glow);
  border-left: 3px solid var(--hx-green);
  padding-left: 12px !important;
  margin: 4px 0 8px !important;
  text-align: left !important;
  animation:
    hx-reveal 1.4s steps(24, end) both,
    hx-glitch 7s infinite 2s;
}
.gradio-container h1::before { content: "> "; color: var(--hx-green-dim); }
.gradio-container h1::after {
  content: "_";
  margin-left: 2px;
  animation: hx-blink 1s steps(1) infinite;
}
.gradio-container h1 + p, .gradio-container .prose p {
  color: var(--hx-muted);
}

@keyframes hx-reveal {
  from { clip-path: inset(0 100% 0 0); }
  to   { clip-path: inset(0 0 0 0); }
}
@keyframes hx-blink { 0%, 49% { opacity: 1; } 50%, 100% { opacity: 0; } }
@keyframes hx-glitch {
  0%, 94%, 100% { transform: none; text-shadow: var(--hx-glow); }
  95% { transform: translate(-2px, 0); text-shadow: 2px 0 #ff0055, -2px 0 #00e5ff; }
  96% { transform: translate(2px, 1px); text-shadow: -2px 0 #ff0055, 2px 0 #00e5ff; }
  97% { transform: translate(-1px, -1px); text-shadow: 1px 0 #ff0055, -1px 0 #00e5ff; }
  98% { transform: none; text-shadow: var(--hx-glow); }
}

/* ---------- Sharp corners everywhere ---------- */
.chatbot, .chatbot *, .block, .form,
button, input, textarea,
.examples button {
  border-radius: 0 !important;
}

/* ---------- Block surfaces ---------- */
.block, .form { background: transparent !important; box-shadow: none !important; }

/* ---------- Hide the Chatbot label / header strip ---------- */
.chatbot > .block-label,
.chatbot > label,
.chatbot .label-wrap,
.chatbot .block-label,
.chatbot > .label-container {
  display: none !important;
}

/* ---------- Chatbot frame: glowing terminal window ---------- */
.chatbot, .chatbot.block {
  background: var(--hx-surface) !important;
  border: 1px solid var(--hx-border-strong) !important;
  min-height: 460px !important;
  box-shadow: 0 0 0 1px rgba(0,255,65,0.08), 0 0 24px rgba(0,255,65,0.12), inset 0 0 40px rgba(0,255,65,0.04) !important;
  animation: hx-pulse 4s ease-in-out infinite;
}
@keyframes hx-pulse {
  0%, 100% { box-shadow: 0 0 0 1px rgba(0,255,65,0.08), 0 0 18px rgba(0,255,65,0.10), inset 0 0 40px rgba(0,255,65,0.04); }
  50%      { box-shadow: 0 0 0 1px rgba(0,255,65,0.18), 0 0 32px rgba(0,255,65,0.22), inset 0 0 40px rgba(0,255,65,0.07); }
}
.chatbot .placeholder, .chatbot .placeholder * { color: var(--hx-muted) !important; }

/* ---------- Message rows: strip parent backgrounds ---------- */
.message-row,
.message-row > div,
.message-row .role,
.message-wrap, .bubble-wrap {
  background: transparent !important;
  border: 0 !important;
  box-shadow: none !important;
}

/* ---------- Reset borders on every bubble variant first ---------- */
.message-row .message,
.message-row .message-bubble,
.message-row .bubble {
  border: 0 !important;
  box-shadow: none !important;
  padding: 8px 12px !important;
  font-family: var(--hx-mono) !important;
}

/* ---------- Bubbles ---------- */
.message-row.user-row .message,
.message-row.user-row .message-bubble,
.message-row.user-row .bubble,
.message-row[data-role="user"] .message,
.message-row[data-role="user"] .message-bubble {
  background: var(--hx-green-deep) !important;
  color: var(--hx-green) !important;
  border: 1px solid var(--hx-border-strong) !important;
  text-shadow: 0 0 4px rgba(0,255,65,0.45);
}

.message-row.bot-row .message,
.message-row.bot-row .message-bubble,
.message-row.bot-row .bubble,
.message-row[data-role="assistant"] .message,
.message-row[data-role="assistant"] .message-bubble {
  background: var(--hx-surface-2) !important;
  color: var(--hx-text) !important;
}

/* ---------- Green stripe on assistant bubbles (outermost match only) ---------- */
.message-row.bot-row .message,
.message-row.bot-row .bubble,
.message-row.bot-row .message-bubble,
.message-row[data-role="assistant"] .message,
.message-row[data-role="assistant"] .bubble,
.message-row[data-role="assistant"] .message-bubble {
  border-left: 2px solid var(--hx-green) !important;
}

.message-row.bot-row .message .message,
.message-row.bot-row .message .bubble,
.message-row.bot-row .message .message-bubble,
.message-row.bot-row .bubble .message,
.message-row.bot-row .bubble .bubble,
.message-row.bot-row .bubble .message-bubble,
.message-row.bot-row .message-bubble .message,
.message-row.bot-row .message-bubble .bubble,
.message-row.bot-row .message-bubble .message-bubble,
.message-row[data-role="assistant"] .message .message,
.message-row[data-role="assistant"] .message .bubble,
.message-row[data-role="assistant"] .message .message-bubble,
.message-row[data-role="assistant"] .bubble .message,
.message-row[data-role="assistant"] .bubble .bubble,
.message-row[data-role="assistant"] .bubble .message-bubble,
.message-row[data-role="assistant"] .message-bubble .message,
.message-row[data-role="assistant"] .message-bubble .bubble,
.message-row[data-role="assistant"] .message-bubble .message-bubble {
  border-left: 0 !important;
}

/* ---------- New messages slide/fade in ---------- */
.message-row {
  animation: hx-msg-in 0.35s ease-out both;
}
@keyframes hx-msg-in {
  from { opacity: 0; transform: translateY(8px); filter: blur(2px); }
  to   { opacity: 1; transform: none; filter: none; }
}

/* ---------- Uniform font size + terminal prompt prefixes ---------- */
.message-row .message,
.message-row .message-bubble,
.message-row .bubble {
  font-size: 13.5px !important;
  line-height: 1.6 !important;
}
.message-row .message p,
.message-row .message-bubble p,
.message-row .bubble p,
.message-row .prose p {
  font-size: 13.5px !important;
  line-height: 1.6 !important;
  margin: 0 0 8px !important;
  color: inherit !important;
}
.message-row .message p:last-child,
.message-row .message-bubble p:last-child,
.message-row .bubble p:last-child,
.message-row .prose p:last-child { margin-bottom: 0 !important; }

.message-row.user-row p:first-child::before,
.message-row[data-role="user"] p:first-child::before {
  content: "$ ";
  color: var(--hx-green-dim);
}
.message-row.bot-row p:first-child::before,
.message-row[data-role="assistant"] p:first-child::before {
  content: "> ";
  color: var(--hx-green);
}

/* Strip stray internal borders/backgrounds from anything inside a bubble */
.message-row .message *,
.message-row .message-bubble *,
.message-row .bubble * {
  background: transparent !important;
  border-color: transparent !important;
  box-shadow: none !important;
  color: inherit !important;
}
.message-row .message a,
.message-row .message-bubble a {
  color: var(--hx-green) !important;
  text-decoration: underline;
  text-shadow: 0 0 6px rgba(0,255,65,0.6);
}
/* code blocks keep a dark inset (higher specificity than the strip rule above) */
.message-row .message pre,
.message-row .message code {
  background: rgba(0, 0, 0, 0.55) !important;
  border: 1px solid var(--hx-border) !important;
  color: var(--hx-green) !important;
  font-family: var(--hx-mono) !important;
}
.message-row .message code { padding: 1px 5px !important; }

/* ---------- Input row ---------- */
.input-row,
.gr-input-row,
.chat-input-row,
form[class*="input"] { align-items: stretch !important; }

textarea, input[type="text"] {
  background: rgba(0, 0, 0, 0.7) !important;
  border: 1px solid var(--hx-border) !important;
  color: var(--hx-green) !important;
  caret-color: var(--hx-green) !important;
  font-family: var(--hx-mono) !important;
  font-size: 14px !important;
  padding: 12px 14px !important;
  line-height: 1.4 !important;
  min-height: 48px !important;
  transition: border-color 0.15s ease, box-shadow 0.15s ease;
}
textarea:focus, input[type="text"]:focus {
  border-color: var(--hx-green) !important;
  outline: none !important;
  box-shadow: var(--hx-glow) !important;
}
textarea::placeholder, input::placeholder { color: var(--hx-muted) !important; }

/* ---------- Buttons ---------- */
button {
  font-family: var(--hx-mono) !important;
  letter-spacing: 0.14em !important;
  text-transform: uppercase !important;
  font-size: 11px !important;
  font-weight: 700 !important;
  border: 1px solid var(--hx-border-strong) !important;
  background: transparent !important;
  color: var(--hx-green) !important;
  padding: 0 16px !important;
  min-height: 48px !important;
  align-self: stretch !important;
  display: inline-flex !important;
  align-items: center !important;
  justify-content: center !important;
  cursor: pointer;
  transition: background 0.12s ease, color 0.12s ease, box-shadow 0.12s ease, transform 0.08s ease;
}
button:hover {
  background: rgba(0,255,65,0.1) !important;
  box-shadow: var(--hx-glow);
  text-shadow: 0 0 6px rgba(0,255,65,0.8);
}
button:active { transform: translateY(1px) scale(0.98); }

button.primary,
button[variant="primary"],
button.submit,
button.submit-button,
.submit-button,
button.lg.primary {
  background: var(--hx-green) !important;
  border: 1px solid var(--hx-green) !important;
  color: #001a07 !important;
  text-shadow: none !important;
  box-shadow: 0 0 12px rgba(0,255,65,0.45);
  min-height: 48px !important;
  align-self: stretch !important;
  padding: 0 14px !important;
  display: inline-flex !important;
  align-items: center !important;
  justify-content: center !important;
}
button.primary:hover,
button.submit:hover,
.submit-button:hover,
button.lg.primary:hover {
  background: #5dff7f !important;
  border-color: #5dff7f !important;
  color: #001a07 !important;
  box-shadow: 0 0 22px rgba(0,255,65,0.8);
}

/* ---------- Submit-button icon ---------- */
button.submit svg,
button.submit-button svg,
.submit-button svg,
button.primary svg,
button[variant="primary"] svg {
  width: 18px !important;
  height: 18px !important;
  margin: 0 auto !important;
  display: block !important;
  align-self: center !important;
  color: #001a07 !important;
  fill: currentColor !important;
  stroke: currentColor !important;
}

/* ---------- Examples: terminal commands ---------- */
.examples, .examples-holder, [data-testid="examples"] {
  background: transparent !important;
  padding: 0 !important;
  margin-top: 14px !important;
}
.examples table, .examples-table { background: transparent !important; border: 0 !important; }
.examples button, .example, .examples td button, [data-testid="examples"] button {
  background: rgba(0, 0, 0, 0.6) !important;
  border: 1px solid var(--hx-border) !important;
  color: var(--hx-text) !important;
  text-transform: none !important;
  letter-spacing: 0 !important;
  font-family: var(--hx-mono) !important;
  font-size: 12.5px !important;
  font-weight: 400 !important;
  padding: 10px 14px !important;
  text-align: left !important;
  min-height: 0 !important;
  align-self: auto !important;
  display: inline-block !important;
  box-shadow: none !important;
}
.examples button::before, .example::before, [data-testid="examples"] button::before {
  content: "$ ";
  color: var(--hx-green-dim);
}
.examples button:hover, .example:hover, [data-testid="examples"] button:hover {
  border-color: var(--hx-green) !important;
  color: var(--hx-green) !important;
  background: rgba(0,255,65,0.08) !important;
  box-shadow: var(--hx-glow) !important;
  transform: translateX(3px);
}

/* ---------- Icon buttons (clear, retry, copy) ---------- */
.icon-button, .chatbot .icon-button {
  color: var(--hx-muted) !important;
  background: transparent !important;
  border: 0 !important;
  box-shadow: none !important;
  min-height: 0 !important;
  align-self: auto !important;
  padding: 4px !important;
  display: inline-flex !important;
  align-items: center !important;
  justify-content: center !important;
}
.icon-button:hover, .chatbot .icon-button:hover { color: var(--hx-green) !important; background: transparent !important; }

/* ---------- Loading / progress ---------- */
.progress-text, .generating, .meta-text { color: var(--hx-green) !important; font-family: var(--hx-mono) !important; }
.wrap.generating, .wrap.pending { border-color: var(--hx-green) !important; }

/* ---------- Scrollbar ---------- */
::-webkit-scrollbar { width: 10px; height: 10px; }
::-webkit-scrollbar-track { background: var(--hx-bg); }
::-webkit-scrollbar-thumb { background: var(--hx-border-strong); }
::-webkit-scrollbar-thumb:hover { background: var(--hx-green); box-shadow: var(--hx-glow); }

/* ---------- Selection ---------- */
::selection { background: var(--hx-green); color: #001a07; }

/* ---------- Mobile ---------- */
@media (max-width: 640px) {
  .gradio-container { padding: 22px 14px 36px !important; }
  .gradio-container h1 { font-size: 20px !important; }
}

/* ---------- Respect reduced-motion settings ---------- */
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after { animation: none !important; transition: none !important; }
  #hx-rain, .hx-sweep { display: none !important; }
}
"""

JS = """
() => {
  document.title = 'Digital Twin // online';

  /* ---------- Matrix rain background ---------- */
  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (!reduceMotion && !document.getElementById('hx-rain')) {
    const canvas = document.createElement('canvas');
    canvas.id = 'hx-rain';
    document.body.appendChild(canvas);

    const sweep = document.createElement('div');
    sweep.className = 'hx-sweep';
    document.body.appendChild(sweep);

    const ctx = canvas.getContext('2d');
    const glyphs = 'アイウエオカキクケコサシスセソタチツテトナニヌネノ0123456789<>/{}[]$#@%&*+=';
    const size = 16;
    let columns = 0;
    let drops = [];

    const resize = () => {
      canvas.width = window.innerWidth;
      canvas.height = window.innerHeight;
      columns = Math.ceil(canvas.width / size);
      drops = Array.from({ length: columns }, () => Math.random() * -50);
    };
    resize();
    window.addEventListener('resize', resize);

    let last = 0;
    const draw = (t) => {
      requestAnimationFrame(draw);
      if (document.hidden || t - last < 55) return;   // ~18 fps, pauses in background tabs
      last = t;
      ctx.fillStyle = 'rgba(2, 6, 4, 0.12)';
      ctx.fillRect(0, 0, canvas.width, canvas.height);
      ctx.font = size + 'px monospace';
      for (let i = 0; i < columns; i++) {
        const ch = glyphs[Math.floor(Math.random() * glyphs.length)];
        const y = drops[i] * size;
        ctx.fillStyle = Math.random() > 0.96 ? '#d6ffe0' : '#00ff41';  // occasional bright head
        ctx.fillText(ch, i * size, y);
        if (y > canvas.height && Math.random() > 0.975) drops[i] = 0;
        drops[i]++;
      }
    };
    requestAnimationFrame(draw);
  }

  /* ---------- Focus handling ---------- */
  const focusInput = () => {
    const areas = document.querySelectorAll('textarea');
    if (areas.length) areas[areas.length - 1].focus();
  };
  setTimeout(focusInput, 300);

  // Re-focus the message field whenever Gradio re-enables it
  // (i.e. after the assistant finishes responding).
  const watchTextarea = (area) => {
    if (area.dataset.twinWatched) return;
    area.dataset.twinWatched = '1';
    let wasDisabled = area.disabled || area.readOnly;
    new MutationObserver(() => {
      const isDisabled = area.disabled || area.readOnly;
      if (wasDisabled && !isDisabled) area.focus();
      wasDisabled = isDisabled;
    }).observe(area, { attributes: true, attributeFilter: ['disabled', 'readonly'] });
  };

  const scan = () => document.querySelectorAll('textarea').forEach(watchTextarea);
  setTimeout(scan, 500);
  new MutationObserver(scan).observe(document.body, { childList: true, subtree: true });
}
"""