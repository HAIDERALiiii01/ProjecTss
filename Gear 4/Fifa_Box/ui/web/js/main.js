/* ============================================================
   Small utilities
   ============================================================ */

// Deterministic hue from a string, used to give each card's
// placeholder art a slightly different tint without any images.
function hueFromString(str) {
  let h = 0;
  for (let i = 0; i < str.length; i++) h = (h * 31 + str.charCodeAt(i)) % 360;
  return h;
}

function el(tag, className, html) {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (html !== undefined) node.innerHTML = html;
  return node;
}

// Checks whether a local media file actually exists by trying to load it.
function probeImage(src) {
  return new Promise((resolve) => {
    const img = new Image();
    img.onload = () => resolve(true);
    img.onerror = () => resolve(false);
    img.src = src;
  });
}

/* ============================================================
   Data access — talks to the pywebview Python bridge.
   Falls back to the bundled JSON via fetch if pywebview isn't
   present yet (useful when just opening index.html in a browser
   during design work).
   ============================================================ */
const Bridge = {
  ready: false,
  async waitForPywebview() {
    if (window.pywebview) { this.ready = true; return; }
    await new Promise((resolve) => {
      window.addEventListener('pywebviewready', () => { this.ready = true; resolve(); }, { once: true });
      // Safety timeout: proceed in "static preview" mode if pywebview never announces itself.
      setTimeout(resolve, 700);
    });
  },
  async getWinners() {
    if (this.ready && window.pywebview) return window.pywebview.api.get_winners();
    return fetch('../data/winners.json').then(r => r.json());
  },
  async getMoments() {
    if (this.ready && window.pywebview) return window.pywebview.api.get_moments();
    return fetch('../data/moments.json').then(r => r.json());
  },
  async ask(question) {
    if (this.ready && window.pywebview) return window.pywebview.api.ask(question);
    // Static preview fallback so the UI is clickable without the backend running.
    await new Promise(r => setTimeout(r, 500));
    return { answer: "(Preview mode — connect app.py through pywebview to get real answers from the archive.)", sources: [] };
  }
};

/* ============================================================
   Card rendering
   ============================================================ */
function assetBase(kind, item) {
  return `./assets/${kind}/${item.id}/`;
}

function buildYearBadge(year) {
  const wrap = el('div', 'card__year');
  String(year).split('').forEach(d => {
    const span = el('span', null, d);
    wrap.appendChild(span);
  });
  return wrap;
}

async function buildCardMedia(kind, item) {
  const media = el('div', 'card__media');
  const base = assetBase(kind, item);

  const posterOk = await probeImage(base + 'poster.jpg');
  const gifOk = await probeImage(base + 'gif.gif');

  if (posterOk) {
    const img = el('img');
    img.src = base + 'poster.jpg';
    img.className = 'is-active';
    img.alt = item.title || item.champion;
    media.appendChild(img);
  } else {
    const ph = el('div', 'card__placeholder is-active');
    const hue = hueFromString(item.id);
    ph.style.background = `linear-gradient(160deg, hsl(${hue} 35% 14%) 0%, hsl(${(hue+40)%360} 30% 9%) 100%)`;
    const glyph = el('span', 'card__placeholder-glyph', String(item.year).slice(2));
    ph.appendChild(glyph);
    media.appendChild(ph);
  }

  if (gifOk) {
    const gif = el('img');
    gif.dataset.src = base + 'gif.gif';
    gif.alt = '';
    media.appendChild(gif);
    media.dataset.hasGif = '1';
  }

  return media;
}

function factRow(kind, item) {
  if (kind === 'winners') {
    return `<span>${item.host}</span><span>${item.score}</span>`;
  }
  return `<span>${item.tagline}</span><span>&#9679;</span>`;
}

async function buildCard(kind, item) {
  const card = el('div', 'card');
  card.tabIndex = 0;
  card.dataset.kind = kind === 'winners' ? 'winner' : 'moment';
  card.dataset.id = item.id;

  const media = await buildCardMedia(kind, item);
  card.appendChild(media);
  card.appendChild(buildYearBadge(item.year));
  card.appendChild(el('div', 'card__tag', kind === 'winners' ? 'Champion' : 'Moment'));

  const body = el('div', 'card__body');
  body.appendChild(el('h3', 'card__title', kind === 'winners' ? item.champion : item.title));
  body.appendChild(el('div', 'card__meta', factRow(kind, item)));
  card.appendChild(body);

  // Hover / focus swaps in the gif if we have one.
  const activate = () => {
    if (media.dataset.hasGif !== '1') return;
    const gif = media.querySelector('img[data-src]');
    if (gif && !gif.src) gif.src = gif.dataset.src;
    gif && gif.classList.add('is-active');
  };
  const deactivate = () => {
    const gif = media.querySelector('img[data-src]');
    gif && gif.classList.remove('is-active');
  };
  card.addEventListener('mouseenter', activate);
  card.addEventListener('mouseleave', deactivate);
  card.addEventListener('focus', activate);
  card.addEventListener('blur', deactivate);

  card.addEventListener('click', () => openDetail(kind, item));
  card.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); openDetail(kind, item); }
  });

  return card;
}

async function renderRail(kind, items, trackEl) {
  trackEl.innerHTML = '';
  for (const item of items) {
    trackEl.appendChild(await buildCard(kind, item));
  }
}

/* ============================================================
   Detail overlay
   ============================================================ */
const detailView = document.getElementById('detail-view');
let currentDetailItem = null;

async function openDetail(kind, item) {
  currentDetailItem = { kind, item };
  const base = assetBase(kind, item);

  document.getElementById('detail-year').textContent = `${item.year} \u00b7 ${kind === 'winners' ? 'Champion' : 'Iconic Moment'}`;
  document.getElementById('detail-title').textContent = kind === 'winners' ? item.champion : item.title;
  document.getElementById('detail-tagline').textContent = item.tagline;

  const factsEl = document.getElementById('detail-facts');
  factsEl.innerHTML = '';
  if (kind === 'winners') {
    factsEl.innerHTML = `
      <span>Host &nbsp;<b>${item.host}</b></span>
      <span>Runner-up &nbsp;<b>${item.runner_up}</b></span>
      <span>Final &nbsp;<b>${item.score}</b></span>`;
  } else {
    factsEl.innerHTML = `<span>Year &nbsp;<b>${item.year}</b></span>`;
  }

  const heroMedia = document.getElementById('detail-hero-media');
  heroMedia.innerHTML = '';
  const posterOk = await probeImage(base + 'poster.jpg');
  const videoOk = await probeImage(base + 'video-poster.jpg'); // lightweight probe; real <video> checked separately
  if (posterOk) {
    const img = el('img');
    img.src = base + 'poster.jpg';
    heroMedia.appendChild(img);
  } else {
    const hue = hueFromString(item.id);
    heroMedia.style.background = `linear-gradient(160deg, hsl(${hue} 35% 14%) 0%, hsl(${(hue+40)%360} 30% 9%) 100%)`;
    heroMedia.appendChild(el('span', 'card__placeholder-glyph', String(item.year)));
    heroMedia.style.display = 'flex';
    heroMedia.style.alignItems = 'center';
    heroMedia.style.justifyContent = 'center';
  }

  const timelineEl = document.getElementById('detail-timeline');
  timelineEl.innerHTML = '';
  item.timeline.forEach((step, i) => {
    const li = el('li', null, step);
    li.dataset.i = String(i + 1).padStart(2, '0');
    timelineEl.appendChild(li);
  });

  // Gallery: probe a handful of numbered images; only show what exists.
  const galleryEl = document.getElementById('detail-gallery');
  galleryEl.innerHTML = '';
  const galleryChecks = await Promise.all(
    [1, 2, 3, 4, 5].map(n => probeImage(`${base}gallery/${n}.jpg`).then(ok => ({ n, ok })))
  );
  const found = galleryChecks.filter(g => g.ok);
  found.forEach(({ n }) => {
    const cell = el('div', 'detail__gallery-item');
    const img = el('img');
    img.src = `${base}gallery/${n}.jpg`;
    cell.appendChild(img);
    galleryEl.appendChild(cell);
  });
  galleryEl.style.display = found.length ? 'flex' : 'none';

  detailView.classList.add('is-open');
  detailView.setAttribute('aria-hidden', 'false');
  document.body.style.overflow = 'hidden';
  detailView.scrollTop = 0;
}

function closeDetail() {
  detailView.classList.remove('is-open');
  detailView.setAttribute('aria-hidden', 'true');
  document.body.style.overflow = '';
}

document.getElementById('detail-close').addEventListener('click', closeDetail);
document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape' && detailView.classList.contains('is-open')) closeDetail();
});

document.getElementById('detail-ask').addEventListener('click', () => {
  if (!currentDetailItem) return;
  const { kind, item } = currentDetailItem;
  const subject = kind === 'winners' ? item.champion + ' ' + item.year : item.title;
  openChat(`Tell me more about ${subject} (${item.year}).`);
});

/* ============================================================
   Chat drawer
   ============================================================ */
const chatDrawer = document.getElementById('chat-drawer');
const chatLog = document.getElementById('chat-log');
const chatForm = document.getElementById('chat-form');
const chatInput = document.getElementById('chat-input');
const chatSend = chatForm.querySelector('.chat-form__send');

function openChat(prefill) {
  chatDrawer.classList.add('is-open');
  chatDrawer.setAttribute('aria-hidden', 'false');
  if (prefill) {
    chatInput.value = prefill;
    chatInput.focus();
  } else {
    chatInput.focus();
  }
}
function closeChat() {
  chatDrawer.classList.remove('is-open');
  chatDrawer.setAttribute('aria-hidden', 'true');
}

document.getElementById('chat-launcher').addEventListener('click', () => openChat());
document.getElementById('chat-close').addEventListener('click', closeChat);
document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape' && chatDrawer.classList.contains('is-open')) closeChat();
});

function addMessage(role, text, sources) {
  const msg = el('div', `chat-msg chat-msg--${role}`);
  msg.appendChild(el('p', null, text));
  chatLog.appendChild(msg);
  chatLog.scrollTop = chatLog.scrollHeight;
  return msg;
}

chatForm.addEventListener('submit', async (e) => {
  e.preventDefault();
  const question = chatInput.value.trim();
  if (!question) return;

  addMessage('user', question);
  chatInput.value = '';
  chatSend.disabled = true;

  const pending = el('div', 'chat-msg chat-msg--bot chat-msg--pending');
  pending.appendChild(el('p', null, 'Checking the box\u2026'));
  chatLog.appendChild(pending);
  chatLog.scrollTop = chatLog.scrollHeight;

  try {
    const result = await Bridge.ask(question);
    pending.remove();
    addMessage('bot', result.answer, result.sources);
  } catch (err) {
    pending.remove();
    addMessage('bot', "Something went wrong reaching the archive. Please try again.");
    console.error(err);
  } finally {
    chatSend.disabled = false;
  }
});

/* ============================================================
   Boot
   ============================================================ */
(async function boot() {
  await Bridge.waitForPywebview();
  const [winners, moments] = await Promise.all([Bridge.getWinners(), Bridge.getMoments()]);
  await renderRail('winners', winners.sort((a, b) => b.year - a.year), document.getElementById('winners-track'));
  await renderRail('moments', moments, document.getElementById('moments-track'));
})();
