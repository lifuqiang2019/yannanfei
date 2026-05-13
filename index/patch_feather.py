import re, json, io, csv
from collections import defaultdict

# ── 1. Read current HTML ──────────────────────────────────────────────
with io.open('d:/BFU/2025-2026/information visual/index/feather.html', 'r', encoding='utf-8') as f:
    src = f.read()

# ── 2. Extract actual June data from CSV ─────────────────────────────
june_csv = defaultdict(lambda: [[0,0]]*30)
for sp in ['swagoo1','gragoo','bahgoo','gwfgoo']:
    june_csv[sp] = [[0,0] for _ in range(30)]
june_csv['douyan'] = [[0,0] for _ in range(30)]

with io.open('d:/BFU/2025-2026/information visual/data/2025/全国五种雁_2025年1-6月.csv',
             'r', encoding='utf-8-sig') as f:
    for row in csv.DictReader(f):
        t = row['观测时间'].strip()
        if not t.startswith('2025-06'):
            continue
        sp = row['物种代码'].strip()
        day = int(t[8:10]) - 1
        qty_s = row['数量'].strip()
        qty = int(qty_s) if qty_s.isdigit() else 0
        key = 'douyan' if sp in ('taibeg1','tunbeg1') else sp
        if key in june_csv:
            june_csv[key][day][0] += 1
            june_csv[key][day][1] += qty

# ── 3. Parse existing data arrays and patch June ──────────────────────
def patch_june(html, sp_id, new_june):
    """Replace indices 151-180 of sp_id.s with new_june data."""
    pat = rf'({sp_id}:\{{[\s\n]*s:)(\[\[.*?\]\])'
    m = re.search(pat, html, re.DOTALL)
    if not m:
        return html
    arr = json.loads(m.group(2))
    arr[151:181] = new_june
    new_arr = json.dumps(arr, separators=(',',':'))
    return html.replace(m.group(0), m.group(1) + new_arr)

for sp_id in ['swagoo1','douyan','gragoo','bahgoo']:
    src = patch_june(src, sp_id, june_csv[sp_id])

# ── 4. CSS & layout changes ───────────────────────────────────────────
# Background
src = src.replace('background:#06101A;', 'background:#F7F9FA;')

# Title
src = src.replace(
    "color:rgba(246,242,231,.82)",
    "color:#D05D61"
)
# Subtitle / p
src = src.replace(
    "color:rgba(246,242,231,.28);margin-top:5px",
    "color:#A8A8A8;margin-top:5px"
)
# Legend text
src = src.replace(
    "color:rgba(246,242,231,.38)",
    "color:#888888"
)
# Legend separator
src = src.replace(
    "color:rgba(246,242,231,.15);font-size:10px",
    "color:#CCCCCC;font-size:10px"
)
# Tooltip bg border: keep dark but update
src = src.replace(
    "background:rgba(6,16,26,.88);border:1px solid rgba(246,242,231,.18);",
    "background:rgba(38,28,28,.92);border:1px solid rgba(150,100,100,.3);"
)
src = src.replace(
    ".tt-sp{font-size:13px;font-weight:500;color:rgba(246,242,231,.9);letter-spacing:1px}",
    ".tt-sp{font-size:13px;font-weight:500;color:rgba(255,235,235,.95);letter-spacing:1px}"
)
src = src.replace(
    ".tt-per{font-size:8.5px;color:rgba(246,242,231,.42);",
    ".tt-per{font-size:8.5px;color:rgba(255,210,210,.5);"
)
src = src.replace(
    ".tt-unit{font-size:8px;color:rgba(246,242,231,.38);",
    ".tt-unit{font-size:8px;color:rgba(255,210,210,.45);"
)
src = src.replace(
    ".tt-rec{font-size:8px;color:rgba(246,242,231,.3);",
    ".tt-rec{font-size:8px;color:rgba(255,210,210,.38);"
)

# ── 5. Species colors ─────────────────────────────────────────────────
# Replace SP array entirely
old_sp = """const SP = [
  {id:'swagoo1',cn:'鸿　雁',la:'Anser cygnoides', sc:'#F2C03C',ac:'#6A9FAD'},
  {id:'douyan', cn:'豆　雁',la:'Anser fabalis',   sc:'#E89828',ac:'#5080A0'},
  {id:'gragoo', cn:'灰　雁',la:'Anser anser',     sc:'#D8CA60',ac:'#78AEB8'},
  {id:'bahgoo', cn:'斑头雁',la:'Anser indicus',   sc:'#EAA030',ac:'#6090A8'},
  {id:'gwfgoo', cn:'白额雁',la:'Anser albifrons', sc:'#F0D858',ac:'#4870A0'},
];"""
new_sp = """const SP = [
  {id:'swagoo1',cn:'鸿　雁',la:'Anser cygnoides', sc:'#D05D61',ac:'#2A588F'},
  {id:'douyan', cn:'豆　雁',la:'Anser fabalis',   sc:'#C04858',ac:'#1E4878'},
  {id:'gragoo', cn:'灰　雁',la:'Anser anser',     sc:'#CC8888',ac:'#6080A0'},
  {id:'bahgoo', cn:'斑头雁',la:'Anser indicus',   sc:'#B84050',ac:'#3470A8'},
  {id:'gwfgoo', cn:'白额雁',la:'Anser albifrons', sc:'#D87880',ac:'#4880B8'},
];"""
src = src.replace(old_sp, new_sp)

# ── 6. Legend HTML ────────────────────────────────────────────────────
src = src.replace(
    'style="background:#F2C03C;box-shadow:0 0 6px #F2C03C80"',
    'style="background:#D05D61"'
)
src = src.replace(
    'style="background:#6A9FAD;box-shadow:0 0 6px #6A9FAD80"',
    'style="background:#2A588F"'
)

# ── 7. Remove glow filter defs & usage ───────────────────────────────
# Remove filter defs block
src = re.sub(
    r"// Glow filters.*?}\);\n\n",
    "",
    src,
    flags=re.DOTALL
)
# Remove filter attribute on group elements
src = src.replace(
    "const sg=svg.append('g').attr('filter','url(#glow-gold)');",
    "const sg=svg.append('g');"
)
src = src.replace(
    "const ag=svg.append('g').attr('filter','url(#glow-teal)');",
    "const ag=svg.append('g');"
)

# ── 8. SVG baseline stroke ────────────────────────────────────────────
src = src.replace(
    ".attr('stroke','rgba(246,242,231,0.06)').attr('stroke-width',0.5);",
    ".attr('stroke','rgba(0,0,0,0.07)').attr('stroke-width',0.5);"
)

# ── 9. drawFeather: rachis stroke ────────────────────────────────────
src = src.replace(
    ".attr('stroke','rgba(246,242,231,0.55)')",
    ".attr('stroke','rgba(100,100,100,0.45)')"
)
# Month tick stroke
src = src.replace(
    ".attr('stroke','rgba(246,242,231,0.18)').attr('stroke-width',0.8);",
    ".attr('stroke','rgba(0,0,0,0.14)').attr('stroke-width',0.8);"
)
# Month label fill
src = src.replace(
    ".attr('fill','rgba(246,242,231,0.22)').attr('letter-spacing','0.2px')",
    ".attr('fill','rgba(0,0,0,0.32)').attr('letter-spacing','0.2px')"
)
# Species cn label
src = src.replace(
    ".attr('fill','rgba(246,242,231,0.72)').text(sp.cn);",
    ".attr('fill','#4A4A4A').text(sp.cn);"
)
# Species latin label
src = src.replace(
    ".attr('fill','rgba(246,242,231,0.20)').text(sp.la);",
    ".attr('fill','#B0B0B0').text(sp.la);"
)

# ── 10. Envelope – smoother, reaches tip ────────────────────────────
src = src.replace(
    "function envelope(t){ return Math.exp(-Math.pow((t-0.38)/0.31,2)*1.9); }",
    "function envelope(t){ return Math.exp(-Math.pow((t-0.42)/0.42,2)*1.5); }"
)

# ── 11. t mapping – extend to tip ───────────────────────────────────
src = src.replace(
    "const t = i / (nDays-1) * 0.93 + 0.035;",
    "const t = i / (nDays-1) * 0.98 + 0.01;"
)

# ── 12. Opacity & length thresholds for light bg ────────────────────
src = src.replace(
    "const op   = tot>0 ? 0.22+0.65*((cnt||0)/(maxCnt||1)) : 0.06;",
    "const op   = tot>0 ? 0.32+0.58*((cnt||0)/(maxCnt||1)) : 0.10;"
)
src = src.replace(
    "if(len<0.25||env<0.04) return;",
    "if(len<0.18||env<0.015) return;"
)

# ── 13. Remove animation ─────────────────────────────────────────────
src = re.sub(
    r"const swayData=\[\];\n",
    "",
    src
)
src = re.sub(
    r"  swayData\.push\(\{.*?\}\);\n  swayData\.push\(\{.*?\}\);\n",
    "",
    src,
    flags=re.DOTALL
)
src = re.sub(
    r"/\* ═+\n   ANIMATION.*?requestAnimationFrame\(frame\);\n",
    "",
    src,
    flags=re.DOTALL
)

# ── 14. Write output ─────────────────────────────────────────────────
out = 'd:/BFU/2025-2026/information visual/index/feather.html'
with io.open(out, 'w', encoding='utf-8') as f:
    f.write(src)
print('Done. Written to', out)
print('File size:', len(src.encode('utf-8')), 'bytes')
