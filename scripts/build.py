#!/usr/bin/env python3
# Convert persona script .md files into an HTML fragment (collapsible blocks).
import re, html, sys

def esc(s): return html.escape(s, quote=False)

def inline(s):
    s = esc(s)
    s = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', s)
    return s

def convert(path):
    lines = open(path, encoding='utf-8').read().split('\n')
    metas, out, ul = [], [], []
    def flush_ul():
        if ul:
            out.append('<ul>' + ''.join(f'<li>{inline(x)}</li>' for x in ul) + '</ul>')
            ul.clear()
    for raw in lines:
        line = raw.rstrip()
        if not line.strip():
            flush_ul(); continue
        if line.startswith('@meta '):
            metas.append(line[6:].strip()); continue
        if line.startswith('### '):
            flush_ul(); out.append(f'<h6 class="sc-scene">{inline(line[4:])}</h6>'); continue
        if line.startswith('## '):
            flush_ul(); out.append(f'<h5 class="sc-sub">{inline(line[3:])}</h5>'); continue
        if line.startswith('# '):
            flush_ul(); out.append(f'<h4 class="sc-ch">{inline(line[2:])}</h4>'); continue
        if re.match(r'^\d+\.\s', line) or line.startswith('- '):
            ul.append(re.sub(r'^(\d+\.\s|-\s)', '', line)); continue
        flush_ul(); out.append(f'<p>{inline(line)}</p>')
    flush_ul()
    title = metas[0] if metas else path
    sub = metas[1] if len(metas) > 1 else ''
    body = '\n'.join(out)
    return f'''<details class="script">
<summary><span class="sc-name">{esc(title)}</span><span class="sc-type">{esc(sub)}</span><span class="sc-toggle">展開 ▾</span></summary>
<div class="sc-body">
{body}
</div>
</details>'''

frag = convert('scripts/anne.md') + '\n' + convert('scripts/emily.md')
open('scripts/fragment.html', 'w', encoding='utf-8').write(frag)
print('wrote scripts/fragment.html', len(frag), 'chars')
