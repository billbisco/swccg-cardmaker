// SWCCG Card Maker — browser UI. Edits a card "spec" (same JSON the batch tools use) and asks the render service
// for a preview image. No build step, no dependencies.
"use strict";
const API = new URL("api/", location.href.replace(/[^/]*$/, "")).href;   // /cardmaker/api/
const $ = (s, el = document) => el.querySelector(s);
const form = $("#form");
let spec = null, opts = null, renderSeq = 0, timer = null;

const STAT_DEFAULTS = {
  Character: [["POWER", "1"], ["ABILITY", "1"]], Starfighter: [["POWER", "1"], ["MANEUVER", "1"], ["HYPERSPEED", "1"]],
  Starship: [["POWER", "1"], ["ARMOR", "1"], ["HYPERSPEED", "1"]], Vehicle: [["POWER", "1"], ["MANEUVER", "1"], ["LANDSPEED", "1"]],
  Creature: [["FEROCITY", "1"]],
};
const BANNER = s => ({ "Character": "", "Site": "", "System": "", "Objective": "", "Epic Event": "", "Admiral's Order": "" }[s] ?? s.toUpperCase());

async function j(url, init) {
  const r = await fetch(url, init);
  if (!r.ok) { let m = r.statusText; try { m = (await r.json()).error || m; } catch (_) {} throw new Error(m); }
  return r.json();
}

function fillSelect(sel, values, labeler = v => v ?? "— none —") {
  sel.innerHTML = "";
  for (const v of values) { const o = document.createElement("option"); o.value = v ?? ""; o.textContent = labeler(v); sel.appendChild(o); }
}

function checks(el, names, selected, prefix) {
  el.innerHTML = "";
  for (const n of names) {
    const id = prefix + n; const l = document.createElement("label");
    l.innerHTML = `<input type="checkbox" id="${id}" value="${n}" ${selected.includes(n) ? "checked" : ""}> ${n.replace(/-/g, " ")}`;
    el.appendChild(l);
  }
}

function statsUI(stats) {
  const box = $("#stats"); box.innerHTML = "";
  (stats || []).forEach(([k, v], i) => {
    const r = document.createElement("div"); r.className = "row";
    r.innerHTML = `<input aria-label="stat label" value="${esc(k)}"><input aria-label="stat value" value="${esc(v)}"><button type="button" title="remove" aria-label="remove stat">×</button>`;
    r.querySelector("button").onclick = () => { r.remove(); changed(); };
    box.appendChild(r);
  });
}
const esc = s => String(s ?? "").replace(/&/g, "&amp;").replace(/"/g, "&quot;").replace(/</g, "&lt;");

function artUI(data) {
  const box = $("#artChoices"); box.innerHTML = "";
  const a = spec.art || { kind: "none" };
  const add = (key, label, img) => {
    const l = document.createElement("label");
    const on = (key === "orig" || key === "x4") ? (a.kind === "library" && (a.version || "orig") === key) : a.kind === key;
    l.innerHTML = `${img ? `<img src="${img}" alt="" loading="lazy">` : ""}<input type="radio" name="artpick" value="${key}" ${on ? "checked" : ""}> ${label}`;
    box.appendChild(l);
  };
  const u = (data && data.art_urls) || {};
  if (u.orig) add("orig", "Printed art", u.orig);
  if (u.x4) add("x4", "AI 4× upscale", u.x4);
  if (spec.gempId) add("scan", "Card's own scan");
  if (a.kind === "ovs" || ((data && data.art_sources) || []).includes("ovs")) add("ovs", "Remaster art (as published)");
  if (a.kind === "upload") add("upload", "Your picture", a.data);
  $("#fZoom").value = a.zoom ?? 1; $("#fX").value = a.fx ?? 0.5; $("#fY").value = a.fy ?? 0.5;
  add("none", "No art");
}

function readForm() {
  const fd = new FormData(form);
  const s = { ...spec };
  for (const k of ["side", "slip_type", "title", "card_type", "destiny", "deploy", "forfeit", "lore", "game_text", "dark_text",
                   "title_back", "game_text_back", "caption", "credit_strip", "number", "parsec", "credits", "copyright", "style"]) {
    const v = fd.get(k); if (v !== null) s[k] = v;
  }
  const mk = $("#setMark").value;   // "", "ovs:N", "pc:N", "vb:N"
  s.virtual_set = mk.startsWith("ovs:") ? +mk.slice(4) : null;
  s.set_mark = /^(pc|vb):/.test(mk) ? mk : null;
  s.affiliation = fd.get("affiliation") || null;
  s.expansion = fd.get("expansion") || null;
  s.scomp = !!fd.get("scomp");
  s.wide = !!fd.get("wide") && WIDE_OK(s);
  s.stats = [...$("#stats").querySelectorAll(".row")].map(r => [...r.querySelectorAll("input")].map(i => i.value)).filter(([k]) => k.trim());
  s.icons = [...$("#icons").querySelectorAll("input:checked")].map(i => i.value);
  if (isLoc(s)) {
    const li = [...$("#locicons").querySelectorAll("input:checked")].map(i => i.value);
    s.light_icons = li; s.dark_icons = li;
    s.light_force_count = +fd.get("light_force_count") || 0; s.dark_force_count = +fd.get("dark_force_count") || 0;
    s.light_force = s.light_force_count > 0; s.dark_force = s.dark_force_count > 0;
    s.card_type = (s.title || "").toUpperCase();   // a location's banner is its title
  }
  if (s.slip_type === "Character") s.card_type = "";
  const pick = form.querySelector("input[name=artpick]:checked");
  if (pick) {
    const k = pick.value;
    if (k === "orig" || k === "x4") s.art = { kind: "library", gempId: s.gempId, version: k };
    else if (k === "upload") s.art = { ...spec.art, zoom: +$("#fZoom").value, fx: +$("#fX").value, fy: +$("#fY").value };
    else s.art = { kind: k, gempId: s.gempId };
  }
  if (s.deploy === "" && s.forfeit === "") { delete s.deploy; delete s.forfeit; }
  return s;
}
// wide (landscape) layouts: Reflections Gold Interrupts / Effects (both sides); Dark Side weapons (Bardez has only DS)
const WIDE_OK = s => /Interrupt|Effect/.test(s.slip_type || "") || (/Weapon/.test(s.slip_type || "") && s.side === "Dark");
const isLoc = s => s.slip_type === "Site" || s.slip_type === "System";

function writeForm(s, data) {
  spec = s;
  for (const el of form.elements) {
    if (!el.name || el.type === "file" || el.type === "radio") continue;
    if (el.type === "checkbox") el.checked = !!s[el.name];
    else el.value = s[el.name] ?? "";
  }
  if (!s.style) form.elements.style.value = "decipher";
  $("#setMark").value = s.set_mark || (s.virtual_set ? "ovs:" + s.virtual_set : "");
  form.elements.light_force_count.value = s.light_force_count ?? (s.light_force ? 1 : 0);
  form.elements.dark_force_count.value = s.dark_force_count ?? (s.dark_force ? 1 : 0);
  statsUI(s.stats);
  checks($("#icons"), opts.icons, s.icons || [], "ic-");
  checks($("#locicons"), opts.loc_icons, s.light_icons || [], "li-");
  artUI(data);
  layoutFor(s);
}

function layoutFor(s) {
  const loc = isLoc(s), obj = s.slip_type === "Objective", ch = s.slip_type === "Character";
  document.querySelectorAll(".loconly").forEach(e => e.hidden = !loc);
  document.querySelectorAll(".objonly").forEach(e => e.hidden = !obj);
  $(".loclight").hidden = loc; $(".locdark").hidden = !loc;
  $(".aff").style.visibility = ch ? "visible" : "hidden";
  $(".wideonly").hidden = !WIDE_OK(s);
  $(".rgonly").style.visibility = /Interrupt|Effect/.test(s.slip_type || "") ? "visible" : "hidden";
  $(".widelbl").textContent = /Weapon/.test(s.slip_type || "") ? "Wide layout (as Maul's Double-Bladed Lightsaber)" : "Reflections Gold wide layout";
  $("#frameBox").hidden = !(s.art && s.art.kind === "upload");
  $(".lorebox").hidden = /Jedi Test|Admiral|Epic/.test(s.slip_type);
  $(".banner").style.visibility = (ch || loc) ? "hidden" : "visible";
  document.querySelectorAll(".df").forEach(e => e.style.visibility = (loc || /Interrupt|Effect|Objective|Epic|Admiral|Shield/.test(s.slip_type)) ? "hidden" : "visible");
}

function changed() {
  const s = readForm();
  layoutFor(s);
  spec = s;
  clearTimeout(timer); timer = setTimeout(preview, 600);
  $("#card").classList.add("stale");
}

async function renderBlob(s, size, format) {
  const r = await fetch(API + "render", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ spec: s, size, format }) });
  if (!r.ok) { let m = r.statusText; try { m = (await r.json()).error; } catch (_) {} throw new Error(m); }
  return r.blob();
}

async function preview() {
  const seq = ++renderSeq; $("#spinner").hidden = false; $("#err").hidden = true;
  try {
    const b = await renderBlob(spec, "preview", "webp");
    if (seq !== renderSeq) return;
    const img = $("#card"); const old = img.src; img.src = URL.createObjectURL(b); if (old.startsWith("blob:")) URL.revokeObjectURL(old);
    img.classList.remove("stale");
  } catch (e) { if (seq === renderSeq) { $("#err").textContent = "Could not render: " + e.message; $("#err").hidden = false; } }
  finally { if (seq === renderSeq) $("#spinner").hidden = true; }
}

async function download(size) {
  const btn = size === "master" ? $("#dlMaster") : $("#dlHolo"); const t = btn.textContent; btn.textContent = "Rendering…"; btn.disabled = true;
  try {
    const b = await renderBlob(spec, size, "png");
    const a = document.createElement("a"); a.href = URL.createObjectURL(b);
    a.download = (spec.title || "card").replace(/[•<>:"/\\|?*]+/g, "").trim().replace(/\s+/g, "_") + (size === "master" ? "_600dpi" : "") + ".png";
    a.click(); setTimeout(() => URL.revokeObjectURL(a.href), 5000);
  } catch (e) { alert("Download failed: " + e.message); }
  finally { btn.textContent = t; btn.disabled = false; }
}

async function loadCard(gid) {
  if ($("#browse").hidden) $("#results").hidden = true;   // browsing: keep the set list open to click through
  const data = await j(API + "card/" + encodeURIComponent(gid));
  writeForm(data.spec, data); history.replaceState(null, "", "#card=" + gid); preview();
}

function blank() {
  writeForm({ side: "Light", slip_type: "Character", title: "•New Character", caption: "", destiny: "1",
    lore: "", game_text: "", stats: STAT_DEFAULTS.Character, deploy: "3", forfeit: "3", icons: ["warrior"], affiliation: "Rebel",
    expansion: null, card_type: "", art: { kind: "none" } }, null);
  history.replaceState(null, "", "#"); preview();
}

let qTimer = null;
$("#q").addEventListener("input", e => {
  clearTimeout(qTimer);
  const q = e.target.value.trim();
  if (q.length < 2) { $("#results").hidden = true; return; }
  qTimer = setTimeout(async () => {
    const list = await j(API + "search?q=" + encodeURIComponent(q) + "&limit=40");
    const ul = $("#results"); ul.innerHTML = "";
    for (const c of list) {
      const li = document.createElement("li"); li.tabIndex = 0;
      li.innerHTML = `<span><span class="side-${c.side}">●</span> ${esc(c.title)}</span><span class="meta">${esc(c.type)} · ${esc(c.set)}</span>`;
      li.onclick = () => loadCard(c.gempId); li.onkeydown = ev => { if (ev.key === "Enter") loadCard(c.gempId); };
      ul.appendChild(li);
    }
    ul.hidden = !list.length;
  }, 250);
});

form.addEventListener("input", e => {
  // a remaster's recorded slip line breaks only hold for the text as transcribed: editing the text drops them
  const LINES = { game_text: "game_text_lines", dark_text: "dark_text_lines", game_text_back: "game_text_back_lines" };
  if (LINES[e.target.name]) delete spec[LINES[e.target.name]];
  if (e.target.type !== "file") changed();
});
form.addEventListener("change", e => {
  if (e.target.name === "slip_type") {
    const st = e.target.value;
    spec = readForm();
    if (STAT_DEFAULTS[st] && !(spec.stats || []).length) statsUI(STAT_DEFAULTS[st]);
    if (st === "Site" || st === "System") $("#icons").querySelectorAll("input:checked").forEach(i => i.checked = false);   // pilot/warrior… don't belong on a location
    if (!spec.card_type || spec.card_type === spec.card_type.toUpperCase()) form.elements.card_type.value = BANNER(st);
  }
  if (e.target.name === "wide" && e.target.checked && !form.elements.expansion.value && /Interrupt|Effect/.test(form.elements.slip_type.value)) form.elements.expansion.value = "Reflections Gold";
  if (e.target.type !== "file") changed();
});
$("#addStat").onclick = () => { const s = readForm(); s.stats.push(["STAT", ""]); statsUI(s.stats); changed(); };
$("#newBtn").onclick = blank;

// browse: every card by set / side / type
function showList(list) {
  const ul = $("#results"); ul.innerHTML = "";
  for (const c of list) {
    const li = document.createElement("li"); li.tabIndex = 0;
    li.innerHTML = `<span><span class="side-${c.side}">●</span> ${esc(c.title)}</span><span class="meta">${esc(c.type)} · ${esc(c.set)}</span>`;
    li.onclick = () => loadCard(c.gempId); li.onkeydown = ev => { if (ev.key === "Enter") loadCard(c.gempId); };
    ul.appendChild(li);
  }
  ul.hidden = !list.length;
}
let setsLoaded = false;
$("#browseBtn").onclick = async () => {
  const box = $("#browse"); box.hidden = !box.hidden; $("#browseBtn").setAttribute("aria-expanded", String(!box.hidden));
  if (box.hidden) { $("#results").hidden = true; return; }
  if (!setsLoaded) {
    const d = await j(API + "sets"); setsLoaded = true;
    const sel = $("#bSet"); sel.innerHTML = "";
    const groups = {};
    for (const s of d.sets) {
      if (!groups[s.group]) { groups[s.group] = document.createElement("optgroup"); groups[s.group].label = s.group; sel.appendChild(groups[s.group]); }
      const o = document.createElement("option"); o.value = s.id; o.textContent = `${s.name} (${s.count})`; groups[s.group].appendChild(o);
    }
    for (const t of d.types) { const o = document.createElement("option"); o.textContent = t; $("#bType").appendChild(o); }
  }
  runBrowse();
};
async function runBrowse() {
  const p = new URLSearchParams({ set: $("#bSet").value, side: $("#bSide").value, type: $("#bType").value });
  const list = await j(API + "browse?" + p);
  $("#bCount").textContent = `${list.length} card${list.length === 1 ? "" : "s"}`;
  showList(list);
}
for (const id of ["#bSet", "#bSide", "#bType"]) $(id).onchange = runBrowse;

function readFile(input, cb) {
  const f = input.files[0]; if (!f) return;
  if (f.size > 15e6) { alert("Please use an image under 15 MB."); return; }
  const r = new FileReader(); r.onload = () => cb(r.result); r.readAsDataURL(f);
}
$("#artFile").onchange = e => readFile(e.target, d => { spec = readForm(); spec.art = { kind: "upload", data: d, zoom: 1, fx: 0.5, fy: 0.5 }; artUI(null); changed(); });
$("#symFile").onchange = e => readFile(e.target, d => { spec = readForm(); spec.set_symbol = d; changed(); });
$("#dlHolo").onclick = () => download("holotable");
$("#dlMaster").onclick = () => download("master");
$("#exportJson").onclick = () => {
  const s = readForm(); const a = document.createElement("a");
  a.href = URL.createObjectURL(new Blob([JSON.stringify(s, null, 1)], { type: "application/json" }));
  a.download = (s.title || "card").replace(/[•<>:"/\\|?*]+/g, "").trim().replace(/\s+/g, "_") + ".json"; a.click();
};
$("#importJson").onchange = e => readFile(e.target, d => {
  try { const s = JSON.parse(atob(d.split(",")[1])); writeForm(s, null); preview(); } catch (err) { alert("Not a card JSON file: " + err.message); }
});
$("#helpLink").onclick = e => { e.preventDefault(); $("#help").showModal(); };
document.querySelectorAll('a[href="#help"]').forEach(a => a.onclick = e => { e.preventDefault(); $("#help").showModal(); });

(async function init() {
  opts = await j(API + "options");
  fillSelect(form.elements.side, opts.sides);
  fillSelect(form.elements.slip_type, opts.slip_types);
  { // set marks: Original Virtual Sets 1-17, modern Virtual Sets 0-27, Virtual Blocks 1-9
    const sel = $("#setMark"); sel.innerHTML = '<option value="">None</option>';
    const grp = (label, pre, a, b, name) => { const g = document.createElement("optgroup"); g.label = label;
      for (let i = a; i <= b; i++) { const o = document.createElement("option"); o.value = pre + i; o.textContent = name + " " + i; g.appendChild(o); }
      sel.appendChild(g); };
    grp("Original Virtual Sets (2002–2008)", "ovs:", 1, 17, "Original Virtual Set");
    grp("Virtual Blocks (2009–2014)", "vb:", 1, 9, "Virtual Block");
    grp("Virtual Sets (2014–)", "pc:", 0, 27, "Virtual Set");
  }
  fillSelect(form.elements.affiliation, [null, ...opts.affiliations]);
  fillSelect(form.elements.expansion, opts.expansions, v => v ?? "— none —");
  $("#tokens").innerHTML = Object.entries(opts.tokens).map(([k, v]) => `<tr><td><code>${esc(k)}</code></td><td>${esc(v)}</td></tr>`).join("");
  const m = location.hash.match(/card=([\w-]+)/);
  if (m) loadCard(m[1]); else loadCard("5_5");
})();
