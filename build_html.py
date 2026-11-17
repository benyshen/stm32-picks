#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把 STM32 学习项目清单 Markdown 渲染成单文件 HTML（自包含、离线、带搜索筛选）。
用法: python build_html.py
"""
import re, json, html, os

BASE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(BASE, "STM32-F1-F4-L4-学习项目清单.md")
OUT = os.path.join(BASE, "index.html")

md = open(SRC, encoding="utf-8").read()
LINK = re.compile(r"\[([^\]]+)\]\((https://github\.com/[^\)]+)\)")
SERIES_TOK = re.compile(r"^(全系|—|-|[FGL]\d*(?:/[A-Z0-9]+)*)$")


def md_inline(t):
    s = html.escape(t)
    s = re.sub(r"\[([^\]]+)\]\((https?://[^\)]+)\)",
               lambda m: '<a href="%s" target="_blank" rel="noopener">%s</a>'
                         % (html.unescape(m.group(2)).replace("&amp;", "&"), m.group(1)), s)
    s = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    return s


def series_tags(text):
    t = text.upper()
    tags = set()
    if re.search(r"F1\b|F10\d|F10X|F103", t): tags.add("F1")
    if re.search(r"F4\b|F40\d|F44\d|F7\b", t): tags.add("F4")
    if re.search(r"L4\b|L47\d|L4P\d", t): tags.add("L4")
    return tags


def norm_token(tok):
    tok = tok.strip()
    if tok in ("—", "-", ""):
        return set(), "通用"
    if tok == "全系":
        return {"F1", "F4", "L4"}, "全系"
    tg = series_tags(tok)
    if not tg:
        return {"F1", "F4", "L4"}, tok
    return tg, ("全系" if len(tg) == 3 else "多系" if len(tg) > 1 else sorted(tg)[0])


# ---------------- 解析 markdown ----------------
lines = md.split("\n")
i = 0
tree = {"h1": "", "intro": [], "sections": []}
cur = None

def target():
    if cur is None:
        return tree["intro"]
    return cur["children"][-1]["items"] if cur["children"] else cur["items"]

while i < len(lines):
    ln = lines[i]
    s = ln.strip()
    if s in ("---", "***", ""):
        i += 1
        continue
    if ln.startswith("# "):
        tree["h1"] = ln[2:].strip()
    elif ln.startswith("## "):
        cur = {"title": ln[3:].strip(), "items": [], "children": []}
        tree["sections"].append(cur)
    elif ln.startswith("### "):
        if cur is None:
            cur = {"title": "正文", "items": [], "children": []}
            tree["sections"].append(cur)
        cur["children"].append({"title": ln[4:].strip(), "items": [], "children": []})
    elif ln.startswith("|"):
        rows = []
        while i < len(lines) and lines[i].startswith("|"):
            rows.append(lines[i])
            i += 1
        target().append(("table", rows))
        continue
    elif s.startswith(">"):
        buf = []
        while i < len(lines) and lines[i].strip().startswith(">"):
            buf.append(lines[i].lstrip(">").strip())
            i += 1
        target().append(("quote", buf))
        continue
    elif re.match(r"^\s*(\d+\.|[-*])\s+", ln):
        buf = []
        while i < len(lines) and (re.match(r"^\s*(\d+\.|[-*])\s+", lines[i]) or lines[i].strip() == ""):
            if lines[i].strip():
                buf.append(re.sub(r"^\s*(\d+\.|[-*])\s+", "", lines[i].strip()))
            i += 1
        target().append(("list", buf))
        continue
    else:
        target().append(("p", s))
    i += 1

# ---------------- 表格 → 卡片 / 表格 ----------------
seen = set()


def parse_table(rows):
    head = [c.strip() for c in rows[0].strip().strip("|").split("|")]
    body = []
    for r in rows[2:]:
        cells = [c.strip() for c in r.strip().strip("|").split("|")]
        if len(cells) < len(head):
            cells += [""] * (len(head) - len(cells))
        body.append(cells)
    return head, body


def to_render(items):
    out = []
    for kind, val in items:
        if kind == "table":
            head, body = parse_table(val)
            if not (body and LINK.search(body[0][0])):
                out.append({"type": "table", "head": head, "body": body})
                continue
            cards = []
            for cells in body:
                m = LINK.search(cells[0])
                if not m:
                    continue
                url = m.group(2)
                repo = url.replace("https://github.com/", "").rstrip("/")
                if "/" not in repo or repo in seen:
                    continue
                seen.add(repo)
                title = m.group(1)
                stars = None
                if len(cells) > 1:
                    mm = re.search(r"(\d[\d,]*)", cells[1].replace("*", ""))
                    if mm:
                        stars = int(mm.group(1).replace(",", ""))
                rest = cells[2:]
                tags, chip = set(), None
                if rest and SERIES_TOK.match(rest[0].strip()):
                    tags, chip = norm_token(rest[0])
                    rest = rest[1:]
                note = " · ".join([c for c in rest if c])
                if not tags:
                    tags = series_tags(title + " " + repo + " " + note)
                    if len(tags) == 3:
                        chip = "全系"
                    elif len(tags) == 1:
                        chip = sorted(tags)[0]
                    elif len(tags) > 1:
                        chip = "多系"
                    else:
                        tags = {"F1", "F4", "L4"}   # 通用资源：任何系列筛选下都可见
                        chip = chip or "通用"
                cards.append({"repo": repo, "title": title, "url": url, "stars": stars,
                              "note": note, "chip": chip, "tags": sorted(tags)})
            if cards:
                out.append({"type": "cards", "cards": cards})
        elif kind == "list":
            out.append({"type": "list", "value": val})
        elif kind == "quote":
            out.append({"type": "quote", "value": val})
        elif kind == "p":
            out.append({"type": "p", "value": val})
    return out


render_sections = []
for sec in tree["sections"]:
    kids = [{"title": c["title"], "groups": to_render(c["items"])} for c in sec["children"]]
    kids = [k for k in kids if k["groups"]]
    render_sections.append({"title": sec["title"], "groups": to_render(sec["items"]), "kids": kids})
render_sections = [s for s in render_sections if s["groups"] or s["kids"]]

n_cards = sum(len(g["cards"]) for s in render_sections
              for grp in [s] + s["kids"] for g in grp["groups"] if g["type"] == "cards")
DATA = json.dumps(render_sections, ensure_ascii=False)
INTRO = [{"type": k, "value": v} for k, v in to_render(tree["intro"])]

CSS = r"""
:root{--bg:#0d1117;--card:#161d27;--card2:#1c2531;--fg:#e6edf3;--muted:#8b98a8;
--line:#26313e;--acc:#2BAE85;--acc2:#4ad3a5;--f1:#f0883e;--f4:#58a6ff;--l4:#d2a8ff;--gold:#f0c04a}
[data-theme="light"]{--bg:#f5f7f9;--card:#fff;--card2:#eef1f5;--fg:#101720;--muted:#5b6675;
--line:#dde3ea;--acc:#0d7f60;--acc2:#0a6b51;--f1:#b45309;--f4:#1d4ed8;--l4:#6d28d9;--gold:#a16207}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{margin:0;background:var(--bg);color:var(--fg);
font:16px/1.65 -apple-system,"Segoe UI","Microsoft YaHei","PingFang SC",sans-serif;-webkit-font-smoothing:antialiased}
a{color:var(--acc2);text-decoration:none}a:hover{text-decoration:underline}
code{background:var(--card2);padding:1px 5px;border-radius:5px;font-size:.88em;
font-family:ui-monospace,Consolas,monospace}
header.top{position:sticky;top:0;z-index:50;background:var(--bg);border-bottom:1px solid var(--line)}
.top-in{max-width:1200px;margin:0 auto;padding:10px 18px;display:flex;gap:9px;align-items:center;flex-wrap:wrap}
.brand{font-weight:700;white-space:nowrap;margin-right:4px}
.brand span{color:var(--acc)}
.searchwrap{position:relative;flex:1;min-width:170px}
#q{width:100%;padding:9px 12px 9px 33px;border-radius:9px;border:1px solid var(--line);
background:var(--card);color:var(--fg);font-size:14px;outline:none;font-family:inherit}
#q:focus{border-color:var(--acc)}
.searchwrap::before{content:"⌕";position:absolute;left:11px;top:7px;color:var(--muted);font-size:17px}
.btn{border:1px solid var(--line);background:var(--card);color:var(--muted);cursor:pointer;
border-radius:9px;padding:7px 11px;font-size:13px;font-family:inherit;transition:.15s}
.btn:hover{color:var(--fg);border-color:var(--acc)}
.btn.on{color:var(--acc2);border-color:var(--acc);background:color-mix(in srgb,var(--acc) 12%,var(--card))}
.wrap{max-width:1200px;margin:0 auto;padding:0 18px 70px;display:grid;
grid-template-columns:236px minmax(0,1fr);gap:34px;align-items:start}
nav.toc{position:sticky;top:62px;max-height:calc(100vh - 80px);overflow:auto;padding:20px 0;font-size:13.4px}
nav.toc a{display:block;color:var(--muted);padding:5px 9px;border-left:2px solid transparent;
border-radius:0 6px 6px 0}
nav.toc a:hover{color:var(--fg);background:var(--card);text-decoration:none}
nav.toc a.on{color:var(--acc2);border-left-color:var(--acc);background:var(--card)}
nav.toc .sub{padding-left:20px;font-size:12.9px}
main{min-width:0}
.hero{padding:34px 0 10px;border-bottom:1px solid var(--line);margin-bottom:6px}
.hero h1{font-size:31px;line-height:1.25;margin:0 0 10px;letter-spacing:-.5px}
.hero h1 em{font-style:normal;color:var(--acc)}
.hero .sub{color:var(--muted);font-size:15px;max-width:70ch;margin:6px 0}
.stats{display:flex;gap:9px;flex-wrap:wrap;margin:17px 0 14px}
.stat{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:7px 13px;
font-size:12.5px;color:var(--muted)}
.stat b{color:var(--fg);font-size:15px;margin-right:3px}
h2.sec{font-size:21px;margin:40px 0 4px;letter-spacing:-.2px;scroll-margin-top:66px}
h2.sec .num{color:var(--acc);font-variant-numeric:tabular-nums;margin-right:8px}
h3.sub{font-size:16px;margin:26px 0 8px;color:var(--acc2);scroll-margin-top:66px}
h3.sub .num{color:var(--acc);opacity:.85;margin-right:6px}
.cards{display:grid;grid-template-columns:repeat(auto-fill,minmax(274px,1fr));gap:11px;margin:12px 0 18px}
.card{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:13px 14px;
display:flex;flex-direction:column;gap:7px;transition:border-color .15s,transform .15s,background .15s}
.card:hover{border-color:var(--acc);transform:translateY(-2px);background:var(--card2)}
.card .row1{display:flex;align-items:baseline;gap:7px;flex-wrap:wrap}
.card .repo{font-weight:600;font-size:14.4px;color:var(--fg);word-break:break-word}
.card .repo:hover{color:var(--acc2);text-decoration:none}
.card .star{margin-left:auto;color:var(--gold);font-size:12.4px;font-variant-numeric:tabular-nums;white-space:nowrap}
.card .note{color:var(--muted);font-size:13.2px;line-height:1.55}
.card .note strong,.card .note code,.card .note a{color:var(--fg)}
.chip{font-size:10.5px;padding:1px 7px;border-radius:999px;border:1px solid;font-weight:700}
.chip.F1{color:var(--f1);border-color:color-mix(in srgb,var(--f1) 45%,transparent)}
.chip.F4{color:var(--f4);border-color:color-mix(in srgb,var(--f4) 45%,transparent)}
.chip.L4{color:var(--l4);border-color:color-mix(in srgb,var(--l4) 45%,transparent)}
.chip.多系,.chip.全系,.chip.通用{color:var(--acc2);border-color:color-mix(in srgb,var(--acc) 40%,transparent)}
.chip.其他,.chip.—,.chip.G4{color:var(--muted);border-color:var(--line)}
.tw{overflow-x:auto;margin:12px 0 20px;border:1px solid var(--line);border-radius:12px;background:var(--card)}
table{border-collapse:collapse;width:100%;font-size:13.5px}
th,td{padding:9px 12px;text-align:left;border-bottom:1px solid var(--line);vertical-align:top}
thead th{background:var(--card2);font-weight:600;white-space:nowrap;font-size:12.8px}
tbody tr:last-child td{border-bottom:none}
tbody tr:hover{background:color-mix(in srgb,var(--acc) 6%,transparent)}
ul.plain{margin:8px 0 16px;padding-left:21px;color:var(--muted)}
ul.plain li{margin:5px 0}
ul.plain strong,ul.plain code{color:var(--fg)}
blockquote{margin:12px 0;padding:10px 15px;border-left:3px solid var(--acc);background:var(--card);
border-radius:0 9px 9px 0;color:var(--muted);font-size:13.8px}
blockquote p{margin:4px 0}
p{max-width:78ch}
footer{border-top:1px solid var(--line);margin-top:46px;padding:20px 0 0;color:var(--muted);
font-size:12.8px;line-height:1.7}
.empty{color:var(--muted);padding:24px 0;font-size:14px}
#toTop{position:fixed;right:18px;bottom:18px;z-index:60;display:none;width:40px;height:40px;
border-radius:50%;border:1px solid var(--line);background:var(--card);color:var(--fg);
cursor:pointer;font-size:15px}
@media (max-width:920px){.wrap{grid-template-columns:1fr;gap:0}nav.toc{display:none}
.hero h1{font-size:23px}.cards{grid-template-columns:1fr}}
@media print{header.top,nav.toc,#toTop{display:none}body{background:#fff;color:#000}
.wrap{grid-template-columns:1fr}.card,.tw{break-inside:avoid}a{color:#000}}
"""

JS = r"""
const DATA=__DATA__, INTRO=__INTRO__;
let filter='all', q='';
const esc=s=>String(s).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
function inl(t){
  let s=esc(t);
  s=s.replace(/\[([^\]]+)\]\((https?:\/\/[^\)]+)\)/g,(m,a,b)=>`<a href="${b}" target="_blank" rel="noopener">${a}</a>`);
  s=s.replace(/\*\*([^*]+)\*\*/g,'<strong>$1</strong>');
  s=s.replace(/`([^`]+)`/g,'<code>$1</code>');
  return s;
}
function match(c){
  if(filter!=='all'){
    if(!(c.tags.includes(filter)||c.tags.length===3)) return false;
  }
  if(!q) return true;
  return (c.repo+' '+c.title+' '+c.note+' '+c.chip).toLowerCase().includes(q);
}
function cards(list){
  const f=list.filter(match);
  if(!f.length) return '<div class="empty">没有匹配的项目 —— 换个关键词，或点「全部」。</div>';
  return '<div class="cards">'+f.map(c=>`<div class="card">
    <div class="row1"><span class="chip ${esc(c.chip)}">${esc(c.chip)}</span>
    <a class="repo" href="${c.url}" target="_blank" rel="noopener">${esc(c.title||c.repo)}</a>
    ${c.stars?`<span class="star">★ ${c.stars.toLocaleString()}</span>`:''}</div>
    <div class="note">${inl(c.note)}</div></div>`).join('')+'</div>';
}
function group(g){
  if(g.type==='cards') return cards(g.cards);
  if(g.type==='table') return '<div class="tw"><table><thead><tr>'+
    g.head.map(h=>'<th>'+inl(h)+'</th>').join('')+'</tr></thead><tbody>'+
    g.body.map(r=>'<tr>'+r.map(c=>'<td>'+inl(c)+'</td>').join('')+'</tr>').join('')+'</tbody></table></div>';
  if(g.type==='list') return '<ul class="plain">'+g.value.map(x=>'<li>'+inl(x)+'</li>').join('')+'</ul>';
  if(g.type==='quote') return '<blockquote>'+g.value.map(x=>'<p>'+inl(x)+'</p>').join('')+'</blockquote>';
  if(g.type==='p') return '<p>'+inl(g.value)+'</p>';
  return '';
}
function countCards(s){
  const own=s.groups.filter(g=>g.type==='cards').reduce((a,g)=>a+g.cards.length,0);
  return own+s.kids.reduce((b,k)=>b+k.groups.filter(g=>g.type==='cards')
    .reduce((a,g)=>a+g.cards.length,0),0);
}
function hero(){
  const total=DATA.reduce((n,s)=>n+countCards(s),0);
  return `<div class="hero"><h1>STM32 <em>F1 / F4 / L4</em> 学习项目清单</h1>
    <div class="sub">给大学生的一份 GitHub 项目地图：从点灯到能写进简历的实物项目。</div>
    <div class="stats"><span class="stat"><b>${total}</b>个开源项目</span>
    <span class="stat"><b>${DATA.length}</b>个章节</span>
    <span class="stat"><b>3</b>个芯片系列</span>
    <span class="stat">数据快照<b>2026-11-08</b></span>
    <span class="stat">外链实测<b>200 OK</b></span></div>
    ${INTRO.map(group).join('')}</div>`;
}
function render(){
  let h=hero(), toc='';
  DATA.forEach((s,si)=>{
    const m=s.title.match(/^([\d.]+)\s*(.*)$/), num=m?m[1]:'', rest=m?m[2]:s.title;
    h+=`<h2 class="sec" id="s${si}">${num?`<span class="num">${esc(num)}</span>`:''}${esc(rest)}</h2>`;
    toc+=`<a href="#s${si}">${num?esc(num)+' ':''}${esc(rest)}</a>`;
    s.groups.forEach(g=>{h+=group(g)});
    s.kids.forEach((k,ki)=>{
      const km=k.title.match(/^([\d.]+)\s*(.*)$/);
      h+=`<h3 class="sub" id="s${si}_${ki}">`+
         (km?`<span class="num">${esc(km[1])}</span>${esc(km[2])}`:esc(k.title))+`</h3>`;
      toc+=`<a class="sub" href="#s${si}_${ki}">${esc(k.title)}</a>`;
      k.groups.forEach(g=>{h+=group(g)});
    });
  });
  h+=`<footer>星数与更新时间为 2026-11-08 从 GitHub 官方 API 抓取的快照，会随时间变化。<br>
  仓库体积差异极大（<code>stm32ai-modelzoo</code> 4.2GB、<code>rusefi</code> 1.6GB、<code>STM32CubeL4</code> 334MB），
  克隆前先看 README，优先 <code>--depth 1</code>。<br>
  部分中文项目是学生毕设代码，工程规范参差：当参考实现，不要当工程范本。引用他人代码/硬件设计请遵守仓库 LICENSE 并注明出处。<br>
  单文件离线版，生成脚本 <code>build_html.py</code> 与源文档 <code>STM32-F1-F4-L4-学习项目清单.md</code> 位于同一目录。</footer>`;
  document.getElementById('content').innerHTML=h;
  document.getElementById('toc').innerHTML=toc;
  observe();
}
let obs=null;
function observe(){
  if(obs) obs.disconnect();
  const links=[...document.querySelectorAll('#toc a')];
  obs=new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting){
    links.forEach(a=>a.classList.toggle('on',a.getAttribute('href')==='#'+e.target.id));};}),
    {rootMargin:'-66px 0px -72% 0px'});
  document.querySelectorAll('h2.sec,h3.sub').forEach(el=>obs.observe(el));
}
document.getElementById('q').addEventListener('input',e=>{q=e.target.value.trim().toLowerCase();render()});
document.querySelectorAll('.btn[data-filter]').forEach(b=>b.addEventListener('click',()=>{
  filter=b.dataset.filter;
  document.querySelectorAll('.btn[data-filter]').forEach(x=>x.classList.toggle('on',x===b));
  render();
}));
document.getElementById('theme').addEventListener('click',()=>{
  const light=document.documentElement.dataset.theme==='light';
  document.documentElement.dataset.theme=light?'dark':'light';
  document.getElementById('theme').textContent=light?'☾ 深色':'☀ 浅色';
});
const tt=document.getElementById('toTop');
addEventListener('scroll',()=>{tt.style.display=scrollY>600?'block':'none'});
tt.addEventListener('click',()=>scrollTo({top:0,behavior:'smooth'}));
document.querySelector('.btn[data-filter="all"]').classList.add('on');
render();
"""

HTML_TPL = """<!DOCTYPE html>
<html lang="zh-CN" data-theme="dark">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="description" content="STM32F1/F4/L4 开源学习项目精选：例程、中文教程、真实项目与课设改造建议">
<title>STM32 F1 / F4 / L4 学习项目清单</title>
<style>%(css)s</style>
</head>
<body>
<header class="top"><div class="top-in">
  <div class="brand">STM32 <span>学习项目清单</span></div>
  <div class="searchwrap"><input id="q" placeholder="搜索项目 / 关键词：FOC、低功耗、Bootloader、智能家居…" autocomplete="off" aria-label="搜索项目"></div>
  <button class="btn" data-filter="all">全部</button>
  <button class="btn" data-filter="F1">F1</button>
  <button class="btn" data-filter="F4">F4</button>
  <button class="btn" data-filter="L4">L4</button>
  <button class="btn" id="theme" title="切换深浅色">☀ 浅色</button>
</div></header>
<div class="wrap">
  <nav class="toc" id="toc" aria-label="目录"></nav>
  <main id="content"></main>
</div>
<button id="toTop" title="回到顶部" aria-label="回到顶部">↑</button>
<script>%(js)s</script>
</body>
</html>
"""

out = HTML_TPL % {"css": CSS,
                   "js": JS.replace("__DATA__", DATA).replace("__INTRO__", json.dumps(INTRO, ensure_ascii=False))}
open(OUT, "w", encoding="utf-8").write(out)
print("输出:", OUT)
print("大小: %.1f KB" % (os.path.getsize(OUT) / 1024))
print("章节:", len(render_sections), " 项目卡片:", n_cards)
