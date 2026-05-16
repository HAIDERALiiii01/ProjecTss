CSS = """
:root {
  --py-color:      #f5c842;
  --py-secondary:  #4fa8e0;
  --cpp-color:     #4fa8e0;
  --cpp-secondary: #f0f4f8;
  --accent:        #6c2ea0;
  --accent-glow:   rgba(108, 46, 160, 0.45);
  --card-bg:       #0e1117;
  --surface:       #0a0c10;
  --border:        rgba(255, 255, 255, 0.07);
  --text:          #e9eef5;
  --muted:         #8b96a8;
}

/* ── Layout ── */
.gradio-container {
  max-width: 100% !important;
  padding: 0 40px !important;
  background: var(--surface) !important;
}
.gradio-container > .main > .wrap > .panel:first-child {
  background: transparent !important;
}

/* ── Code editor cards ── */
.card {
  background: var(--card-bg);
  border: 1px solid var(--border);
  border-radius: 14px;
  padding: 10px;
  transition: border-color .2s;
}
.card:focus-within {
  border-color: rgba(255, 255, 255, 0.16);
}

/* Language label accent dots */
.block:has(.python) > .label-wrap::before,
.block:has([label="Python (original)"]) .label-wrap::before {
  content: "";
  display: inline-block;
  width: 8px; height: 8px;
  border-radius: 50%;
  background: var(--py-color);
  margin-right: 6px;
  vertical-align: middle;
}
.block:has([label="C++ (generated)"]) .label-wrap::before {
  content: "";
  display: inline-block;
  width: 8px; height: 8px;
  border-radius: 50%;
  background: var(--cpp-color);
  margin-right: 6px;
  vertical-align: middle;
}

/* ── Buttons ── */
button.convert-btn {
  background: var(--accent) !important;
  border: 1px solid rgba(255,255,255,.12) !important;
  color: #fff !important;
  font-weight: 700 !important;
  letter-spacing: .025em !important;
  transition: box-shadow .2s, transform .1s !important;
}
button.convert-btn:hover {
  box-shadow: 0 0 18px var(--accent-glow) !important;
  transform: translateY(-1px) !important;
}
button.convert-btn:active { transform: translateY(0) !important; }

button.run-btn {
  background: #161a22 !important;
  color: var(--muted) !important;
  border: 1px solid var(--border) !important;
  font-weight: 600 !important;
  transition: box-shadow .2s, color .2s, transform .1s !important;
}

/* Run Python: yellow text + blue glow on hover */
button.run-btn.py:hover {
  color: var(--py-color) !important;
  box-shadow: 0 0 0 1.5px var(--py-secondary) inset,
              0 0 14px rgba(79, 168, 224, .25) !important;
  transform: translateY(-1px) !important;
}

/* Run C++: blue text + white glow on hover */
button.run-btn.cpp:hover {
  color: var(--cpp-color) !important;
  box-shadow: 0 0 0 1.5px var(--cpp-secondary) inset,
              0 0 14px rgba(240, 244, 248, .15) !important;
  transform: translateY(-1px) !important;
}

/* ── Model dropdown ── */
.controls select, .controls .wrap select {
  background: #161a22 !important;
  color: var(--muted) !important;
  border: 1px solid var(--border) !important;
  border-radius: 8px !important;
}

/* ── Python output: yellow border + blue label ── */
.py-out textarea {
  background: rgba(245, 200, 66, .05) !important;
  border: 1px solid rgba(245, 200, 66, .35) !important;
  border-radius: 10px !important;
  color: var(--py-color) !important;
  font-family: var(--font-mono), monospace !important;
  font-weight: 500 !important;
  font-size: 13px !important;
  transition: border-color .2s !important;
}
.py-out textarea:focus {
  border-color: rgba(245, 200, 66, .65) !important;
}
.py-out .label-wrap span {
  color: var(--py-secondary) !important;
  font-weight: 600;
}

/* ── C++ output: blue border + white label ── */
.cpp-out textarea {
  background: rgba(79, 168, 224, .05) !important;
  border: 1px solid rgba(79, 168, 224, .35) !important;
  border-radius: 10px !important;
  color: var(--cpp-color) !important;
  font-family: var(--font-mono), monospace !important;
  font-weight: 500 !important;
  font-size: 13px !important;
  transition: border-color .2s !important;
}
.cpp-out textarea:focus {
  border-color: rgba(79, 168, 224, .65) !important;
}
.cpp-out .label-wrap span {
  color: var(--cpp-secondary) !important;
  font-weight: 600;
}

/* ── Controls row ── */
.controls .wrap {
  gap: 12px;
  justify-content: center;
  align-items: center;
}

/* ── Thin separator between sections ── */
.gradio-container .row + .row {
  margin-top: 10px;
}

/* ── Global dark polish ── */
.gradio-container textarea,
.gradio-container .codemirror-wrapper {
  background: var(--card-bg) !important;
  border-color: var(--border) !important;
}
.gradio-container label span,
.gradio-container .label-wrap span {
  color: var(--muted) !important;
  font-size: 12px !important;
  font-weight: 500 !important;
  letter-spacing: .03em !important;
  text-transform: uppercase !important;
}

/* ── Dracula syntax highlighting ── */
.ͼp  { color: #ff79c6 !important; font-weight: 600 !important; }
.ͼr  { color: #f8f8f2 !important; }
.ͼs  { color: #50fa7b !important; }
.ͼy  { color: #bd93f9 !important; }
.ͼ10 { color: #ff79c6 !important; }
.ͼv  { color: #f8f8f2 !important; }
.ͼ19 { color: #f1fa8c !important; }
.ͼw  { color: #8be9fd !important; }
.ͼq  { color: #50fa7b !important; }
"""