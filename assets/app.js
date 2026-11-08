/* Shared chrome, i18n and chart helpers for guide.erbihou.org.
   Language: English by default on first load; toggle persists in localStorage. */
(function () {
  'use strict';
  var PAGES = [
    ['index.html', 'Home', '首页'],
    ['l1.html', 'L1 Composition', 'L1 构成', 'l1'],
    ['l2.html', 'L2 Discordance', 'L2 不一致', 'l2'],
    ['l3.html', 'L3 Archaeology', 'L3 引文考古', 'l3'],
    ['l4.html', 'L4 Concordance', 'L4 跨指南一致性', 'l4'],
    ['l5.html', 'L5 Dynamics', 'L5 版本动态', 'l5'],
    ['explorer.html', 'Explorer', '推荐浏览器'],
    ['thin-ice.html', 'Thin ice', '薄冰推荐', 'l3'],
    ['discordance.html', 'Discordance', '分歧对位', 'l4'],
    ['dynamics.html', 'Versions', '版本变迁', 'l5'],
    ['zombies.html', 'Zombie watch', '僵尸观察', 'l5'],
    ['lookup.html', 'PMID lookup', 'PMID 反查', 'l3'],
    ['citations.html', 'Citation search', '引文正查', 'l3'],
    ['questions.html', 'Questions', '问题查询', 'l4'],
    ['verification.html', 'Verification', '核查中心'],
    ['framework.html', 'Framework', '框架'],
    ['downloads.html', 'Downloads', '下载']
  ];
  /* Fixed layer colour code — mirrors assets/style.css (--l1..--l5). */
  window.GC = {};
  GC.lang = localStorage.getItem('gc-lang') || 'en';
  GC.t = function (en, zh) { return GC.lang === 'zh' ? zh : en; };
  GC.hues = { l1: '#0d7a6f', l2: '#46689c', l3: '#9c6b24', l4: '#74549b', l5: '#a6503c' };
  GC.hue = function (l) { return GC.hues[l] || '#0c5563'; };
  GC.qs = function (name) { return new URLSearchParams(location.search).get(name); };

  function applyLang() {
    document.documentElement.lang = GC.lang === 'zh' ? 'zh-CN' : 'en';
    document.querySelectorAll('[data-en]').forEach(function (el) {
      el.textContent = GC.lang === 'zh' ? el.getAttribute('data-zh') : el.getAttribute('data-en');
    });
    document.querySelectorAll('[data-en-ph]').forEach(function (el) {
      el.placeholder = GC.lang === 'zh' ? el.getAttribute('data-zh-ph') : el.getAttribute('data-en-ph');
    });
    document.querySelectorAll('nav.main a').forEach(function (a) {
      a.textContent = GC.lang === 'zh' ? a.getAttribute('data-zh') : a.getAttribute('data-en');
    });
    var b = document.getElementById('langbtn');
    if (b) b.textContent = GC.lang === 'zh' ? 'EN' : '中文';
    if (window.onLangChange) window.onLangChange();
  }
  GC.applyLang = applyLang;

  document.addEventListener('DOMContentLoaded', function () {
    var here = location.pathname.split('/').pop() || 'index.html';
    var header = document.createElement('header');
    header.className = 'site';
    var nav = PAGES.map(function (p) {
      var layer = p[3] ? ' data-layer="' + p[3] + '" style="--nl:' + GC.hue(p[3]) + '"' : '';
      return '<a href="' + p[0] + '" data-en="' + p[1] + '" data-zh="' + p[2] + '"' + layer +
        (p[0] === here ? ' class="on"' : '') + '>' + p[1] + '</a>';
    }).join('');
    header.innerHTML = '<div class="bar">' +
      '<a class="brand" href="index.html">GuideCensus' +
      '<small data-en="The evidence beneath ENT guideline recommendations" ' +
      'data-zh="耳鼻喉科指南推荐背后的证据">The evidence beneath ENT guideline recommendations</small></a>' +
      '<nav class="main">' + nav + '</nav>' +
      '<button class="langbtn" id="langbtn">中文</button></div>';
    document.body.insertBefore(header, document.body.firstChild);
    var footer = document.createElement('footer');
    footer.className = 'site';
    footer.innerHTML = '<div class="bar"><span data-en="GuideCensus — a five-layer census of the evidence beneath ENT clinical guideline recommendations. All data frozen 2026-11-08; every number on this site is generated from the frozen datasets." ' +
      'data-zh="GuideCensus —— 耳鼻喉科临床指南推荐证据的五层普查。全部数据冻结于 2026-11-08；本站每个数字均由冻结数据集生成。">GuideCensus</span>' +
      '<span><a href="downloads.html" data-en="Data &amp; downloads" data-zh="数据与下载">Data</a> · ' +
      '<a href="verification.html" data-en="Verification record" data-zh="核查记录">Verification</a></span></div>';
    document.body.appendChild(footer);
    document.getElementById('langbtn').addEventListener('click', function () {
      GC.lang = GC.lang === 'zh' ? 'en' : 'zh';
      localStorage.setItem('gc-lang', GC.lang);
      applyLang();
    });
    /* Copy-link buttons (data-copy-url="?…" resolves against the page URL). */
    document.addEventListener('click', function (e) {
      var b = e.target && e.target.closest ? e.target.closest('[data-copy-url]') : null;
      if (!b) return;
      e.preventDefault();
      var url = b.getAttribute('data-copy-url');
      if (url.charAt(0) === '?') url = location.origin + location.pathname + url;
      if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(url);
      var old = b.textContent;
      b.textContent = GC.t('Copied ✓', '已复制 ✓');
      setTimeout(function () { b.textContent = old; }, 1600);
    });
    applyLang();
    if (window.onSiteReady) window.onSiteReady();
  });

  /* ---- data access -------------------------------------------------------
     Every page reads data ONLY through GC.load / GC.api. GC.resolveData is
     the single swap point: when the D1-backed API (see INTEGRATION.md) goes
     live, it alone changes — e.g. return 'https://api.guide.erbihou.org/v1/'
     + name.replace(/\.json$/, '') — and no page code changes. */
  GC.resolveData = function (name) { return 'data/' + name; };
  GC.load = function (name) {
    return fetch(GC.resolveData(name)).then(function (r) { return r.json(); });
  };
  GC.api = {
    items: function () { return GC.load('items.json'); },
    stats: function () { return GC.load('stats.json'); },
    questions: function () { return GC.load('questions.json'); },
    discordant: function () { return GC.load('discordant.json'); },
    compare: function () { return GC.load('compare.json'); },
    dynamics: function () { return GC.load('dynamics.json'); },
    zombies: function () { return GC.load('zombies.json'); },
    pmidIndex: function () { return GC.load('pmid_index.json'); },
    citations: function () { return GC.load('citations.json'); },
    coverage: function () { return GC.load('pmid_coverage.json'); },
    verification: function () { return GC.load('verification.json'); },
    downloads: function () { return GC.load('downloads.json'); }
  };
  GC.esc = function (s) {
    return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  };
  GC.pct = function (x, digits) {
    if (x == null || isNaN(x)) return '—';
    return (100 * x).toFixed(digits == null ? 1 : digits) + '%';
  };
  GC.dirHTML = function (d) {
    var label = d === 'for' ? GC.t('For', '支持') : d === 'against' ? GC.t('Against', '反对') : GC.t('No stance', '未表态');
    return '<span class="dir-' + (d || 'none') + '">' + label + '</span>';
  };

  /* ---- minimal SVG charts ---- */
  GC.barChart = function (el, rows, opts) {
    // rows: [{label, value, display, color, link?, tip?}] — a row with `link`
    // becomes a click-through to a pre-filtered view, with a hover tooltip.
    opts = opts || {};
    var w = opts.width || 720, lh = opts.labelWidth || 190, rh = 26;
    var max = Math.max.apply(null, rows.map(function (r) { return r.value; }).concat([1]));
    var h = rows.length * rh + 8;
    var s = '<svg viewBox="0 0 ' + w + ' ' + h + '" width="100%" role="img">';
    rows.forEach(function (r, i) {
      var y = i * rh + 4, bw = Math.max(1, (w - lh - 90) * r.value / max);
      var g = '<title>' + GC.esc(r.tip || (r.label + ' — ' + r.display)) + '</title>' +
        '<text x="' + (lh - 8) + '" y="' + (y + 15) + '" text-anchor="end" font-size="12.5">' + GC.esc(r.label) + '</text>' +
        '<rect x="' + lh + '" y="' + y + '" width="' + bw + '" height="17" rx="3" fill="' + (r.color || '#0c5563') + '"/>' +
        '<text x="' + (lh + bw + 7) + '" y="' + (y + 14) + '" font-size="12.5" fill="#33424f">' + GC.esc(r.display) + '</text>';
      s += r.link ? '<a href="' + r.link + '">' + g + '</a>' : g;
    });
    el.innerHTML = s + '</svg>';
  };
  GC.stackBar = function (el, segs, opts) {
    // segs: [{label, value, color, link?, tip?}] — segments with `link`
    // click through to the matching pre-filtered explorer view.
    opts = opts || {};
    var w = opts.width || 720, h = 30, total = segs.reduce(function (a, s) { return a + s.value; }, 0);
    var x = 0, s = '<svg viewBox="0 0 ' + w + ' ' + (h + 22) + '" width="100%" role="img">';
    segs.forEach(function (g) {
      var bw = w * g.value / total;
      var seg = '<title>' + GC.esc(g.tip || (g.label + ' — ' + g.value)) + '</title>' +
        '<rect x="' + x + '" y="0" width="' + Math.max(0, bw - 1) + '" height="' + h + '" fill="' + g.color + '"/>';
      if (bw > 44) seg += '<text x="' + (x + bw / 2) + '" y="19" text-anchor="middle" font-size="12.5" fill="#fff">' + g.value + '</text>';
      seg += '<text x="' + (x + bw / 2) + '" y="' + (h + 16) + '" text-anchor="middle" font-size="11.5" fill="#5b6b7a">' + GC.esc(g.label) + '</text>';
      s += g.link ? '<a href="' + g.link + '">' + seg + '</a>' : seg;
      x += bw;
    });
    el.innerHTML = s + '</svg>';
  };
})();
