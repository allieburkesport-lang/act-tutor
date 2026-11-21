"""Make HTML survive Gmail's sender: it strips CSS backgrounds and <img>. Move div/span/a backgrounds into bgcolor table cells."""
import re
PAT = re.compile(r"<(div|span|a)([^>]*?)style='([^']*?)background:(#[0-9A-Fa-f]{6})([^']*)'([^>]*)>")

def fix(h):
    out, i = [], 0
    while True:
        m = PAT.search(h, i)
        if not m:
            out.append(h[i:]); break
        out.append(h[i:m.start()])
        tag, pre, st1, col, st2, post = m.groups()
        st = re.sub(r'background-image:[^;]*;?', '', st1 + st2)
        st = re.sub(r'display:inline-block;?', '', st)
        inline = tag in ('span', 'a')
        depth, j = 1, m.end()
        op = re.compile(r"<%s[\s>]|</%s>" % (tag, tag))
        while depth:
            mm = op.search(h, j)
            depth += -1 if mm.group().startswith('</') else 1
            j = mm.end()
        inner = fix(h[m.end():mm.start()])
        if tag == 'a':
            astyle = re.sub(r'padding:[^;]*;?|border-radius:[^;]*;?', '', st)
            inner = f"<a{pre}style='{astyle}'{post}>{inner}</a>"
        tstyle = 'border-collapse:separate;' + ('display:inline-table;vertical-align:middle;' if inline else '')
        width = '' if inline else " width='100%'"
        out.append(f"<table role='presentation'{width} cellpadding='0' cellspacing='0' border='0' style='{tstyle}'><tr><td bgcolor='{col}' style='{st}'>{inner}</td></tr></table>")
        i = j
    return ''.join(out)
