"""Shared helpers for Reading & Writing videos."""
from common import *

def passage(ctx, segs, x, y, w, size=30, k=1, lh=1.5, box=True, pad=26):
    """segs: list of (text, color, kind). kind: None | 'hl' (highlight) | 'blank' (text = filled word or '').
    Returns bottom y."""
    if k <= 0: return y
    words = []
    for s, c, kind in segs:
        if kind == 'blank': words.append((s, c, 'blank')); continue
        for wd in s.split(' '):
            if wd: words.append((wd, c, kind))
    font(ctx, size, False); sp = ctx.text_extents(' ').x_advance
    lines, cur, cw = [], [], 0
    for wd, c, kind in words:
        ww = (max(twidth(ctx, wd, size, kind == 'blank'), 130) + 16) if kind == 'blank' else twidth(ctx, wd, size, kind == 'hl')
        if cur and cw + sp + ww > w - 2 * pad: lines.append(cur); cur, cw = [], 0
        cur.append((wd, c, kind, ww)); cw += (sp if cw else 0) + ww
    if cur: lines.append(cur)
    H = len(lines) * size * lh + 2 * pad - size * (lh - 1) + 8
    if box: rrect(ctx, x, y, w, H, 16, fill=C['bg2'], stroke=C['mute'], a=k, lw=1)
    yy = y + pad + size * .9
    for ln in lines:
        xx = x + pad
        for wd, c, kind, ww in ln:
            if kind == 'blank':
                line(ctx, xx, yy + 8, xx + ww - 8, yy + 8, c, 3, 1, k)
                if wd: text(ctx, wd, xx + (ww - 8) / 2, yy, size, c, k, 'c')
            else:
                if kind == 'hl':
                    rrect(ctx, xx - 4, yy - size * .85, ww + 8, size * 1.15, 6, fill=c, a=.22 * k)
                text(ctx, wd, xx, yy, size, c if kind == 'hl' else C['ink'], k, 'l', kind == 'hl')
            xx += ww + sp
        yy += size * lh
    return y + H

def choices(ctx, opts, x, y, w, k=1, right=None, out=(), size=26, gap=62):
    for i, s in enumerate(opts):
        kk_ = seg(k, i * .12, i * .12 + .4)
        if kk_ <= 0: continue
        L = 'ABCD'[i]; c = C['green'] if right == i else C['mute']
        rrect(ctx, x, y + i * gap, w, gap - 12, 10, fill=C['bg2'], stroke=c, a=kk_, lw=3 if right == i else 1)
        text(ctx, L, x + 20, y + i * gap + 34, size, c, kk_)
        text(ctx, s, x + 60, y + i * gap + 34, size, C['green'] if right == i else C['ink'], kk_, 'l', False)
        if i in out: line(ctx, x + 50, y + i * gap + 25, x + 70 + twidth(ctx, s, size, False), y + i * gap + 25, C['red'], 3, 1, kk_)

def steps(ctx, items, x, y, p, a=0, z=.9, size=30, gap=70):
    n = len(items)
    for i, (s, c) in enumerate(items):
        k = seg(p, a + (z - a) * i / n, a + (z - a) * (i + .6) / n)
        if k <= 0: continue
        disc(ctx, x + 22, y + i * gap - 10, 22, c, k); text(ctx, str(i + 1), x + 22, y + i * gap, 24, C['bg'], k, 'c')
        text(ctx, s, x + 62, y + i * gap, size, C['ink'], k)

def join(ctx, L, M, R, y, k, mc=None, tags=None, size=30, x=80):
    """Draw 'L M R' on one line; M in big colored type. tags=(lt, rt) labels under each side."""
    if k <= 0: return
    mc = mc or C['yel']
    wl = twidth(ctx, L, size, False); wm = twidth(ctx, M, size + 8) if M.strip() else 30
    text(ctx, L, x, y, size, C['ink'], k, 'l', False)
    if M.strip(): text(ctx, M, x + wl + 4, y, size + 8, mc, k)
    else: rrect(ctx, x + wl + 6, y - size, 18, size + 6, 4, stroke=mc, a=k, lw=2)
    text(ctx, R, x + wl + wm + 14, y, size, C['ink'], k, 'l', False)
    if tags:
        for (lab, xx, ww, ok) in [(tags[0], x, wl, tags[0] == 'FULL'), (tags[1], x + wl + wm + 14, twidth(ctx, R, size, False), tags[1] == 'FULL')]:
            if not lab: continue
            c = C['green'] if ok else C['org']
            line(ctx, xx, y + 14, xx + ww, y + 14, c, 3, 1, k); text(ctx, lab, xx + ww / 2, y + 44, 20, c, k, 'c')

