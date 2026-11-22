import sys, math, json, subprocess
sys.path.insert(0, '/home/claude/v2')
from engine import *
PI = math.pi
rad = math.radians
def chip(ctx, s, c):
    w = twidth(ctx, s, 15) + 26; rrect(ctx, 28, 58, w, 30, 15, fill=C['bg2'], stroke=c, lw=1.5); text(ctx, s, 41, 78, 15, c)
def trap(ctx, x, y, w, l1, l2, k, size=21):
    while size > 14 and max(twidth(ctx, l1, size), twidth(ctx, l2, size)) > w - 40: size -= 1
    rrect(ctx, x, y, w, 110, 12, fill=(0.25, 0.08, 0.08), stroke=C['red'], a=seg(k, 0, .2))
    text(ctx, 'TRAP', x + 20, y + 28, 15, C['red'], seg(k, 0, .2))
    text(ctx, l1, x + 20, y + 62, size, C['ink'], seg(k, .15, .4))
    text(ctx, l2, x + 20, y + 94, size, C['red'], seg(k, .35, .6))
def question(ctx, s, k, size=24):
    chip(ctx, 'SAT-style question', C['yel'])
    rrect(ctx, 60, 100, 1160, 70, 12, fill=C['bg2'], stroke=C['mute'], lw=1)
    write(ctx, s, 80, 145, size, C['ink'], k)
def answer(ctx, s, x, y, w, k, size=32):
    while size > 16 and twidth(ctx, s, size) > w - 30: size -= 1
    rrect(ctx, x, y, w, 64, 12, fill=C['bg2'], stroke=C['green'], a=k)
    text(ctx, s, x + w / 2, y + 32 + size * .36, size, C['green'], k, 'c')
def recap(ctx, p, items):
    text(ctx, 'Lock it in', 640, 150, 54, C['ink'], seg(p, 0, .1), 'c')
    for i, (s, c) in enumerate(items):
        k = seg(p, .12 + i * .25, .27 + i * .25)
        rrect(ctx, 230, 210 + i * 100, 820, 80, 16, fill=C['bg2'], stroke=c, a=k, lw=3)
        disc(ctx, 275, 250 + i * 100, 22, c, k); text(ctx, str(i + 1), 275, 259 + i * 100, 24, C['bg'], k, 'c')
        text(ctx, s, 320, 262 + i * 100, 32, c, k)
def kk(b, bb, p, a=0, z=.7):
    """reveal for something that appears on beat bb"""
    return 0 if b < bb else (seg(p, a, z) if b == bb else 1)
def run(D, NAR, PLAN, SC, header, hook, pads, CH):
    """stills | render"""
    assert len(PLAN) == len(NAR), (len(PLAN), len(NAR))
    BEATS = list(zip(PLAN, NAR))
    if sys.argv[1:] == ['stills']:
        import cairo, os
        os.makedirs(f'{D}/st', exist_ok=True); cnt = {}
        for i, (n, _) in enumerate(BEATS):
            b = cnt.get(n, 0); cnt[n] = b + 1
            surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); ctx = cairo.Context(surf); background(ctx); SC[n](ctx, b, 1, 3); caption(ctx, NAR[i][:120])
            surf.write_to_png(f'{D}/st/{i:02d}.png')
        from PIL import Image
        ims = [Image.open(f'{D}/st/{i:02d}.png').resize((320, 180)) for i in range(len(BEATS))]
        c = Image.new('RGB', (1280, 180 * ((len(ims) + 3) // 4)))
        for i, im in enumerate(ims): c.paste(im, ((i % 4) * 320, (i // 4) * 180))
        c.save(f'{D}/sheet.png')
    else:
        durs, starts = render(BEATS, SC, f'{D}/video.mp4', header, f'{D}/wav', pads=pads)
        json.dump(dict(durs=durs, starts=starts), open(f'{D}/timing.json', 'w'))
        thumb(hook, 0, f'{D}/thumb.png')
        ch = []; seen = set()
        for i, n in enumerate(PLAN):
            if n not in seen and n in CH: seen.add(n); ch.append([int(starts[i]), CH[n]])
        json.dump(ch, open(f'{D}/chapters.json', 'w'))

class Graph:
    """maps math coords to screen inside box (x0,y0,w,h) for ranges xr, yr"""
    def __init__(s, x0, y0, w, h, xr, yr): s.x0, s.y0, s.w, s.h, s.xr, s.yr = x0, y0, w, h, xr, yr
    def X(s, x): return s.x0 + (x - s.xr[0]) / (s.xr[1] - s.xr[0]) * s.w
    def Y(s, y): return s.y0 + s.h - (y - s.yr[0]) / (s.yr[1] - s.yr[0]) * s.h
    def axes(s, ctx, k=1, grid=1):
        if k <= 0: return
        if grid:
            for gx in range(math.ceil(s.xr[0]), math.floor(s.xr[1]) + 1, grid): line(ctx, s.X(gx), s.y0, s.X(gx), s.y0 + s.h, C['grid'], 1, k)
            for gy in range(math.ceil(s.yr[0]), math.floor(s.yr[1]) + 1, grid): line(ctx, s.x0, s.Y(gy), s.x0 + s.w, s.Y(gy), C['grid'], 1, k)
        line(ctx, s.x0, s.Y(0), s.x0 + s.w, s.Y(0), C['mute'], 2, k); line(ctx, s.X(0), s.y0, s.X(0), s.y0 + s.h, C['mute'], 2, k)
    def plot(s, ctx, f, c, w=4, k=1, n=160):
        if k <= 0: return
        col(ctx, c); ctx.set_line_width(w); ctx.set_line_cap(cairo.LINE_CAP_ROUND); first = True
        for i in range(int(n * k) + 1):
            x = s.xr[0] + (s.xr[1] - s.xr[0]) * i / n; y = f(x)
            if y < s.yr[0] or y > s.yr[1]: first = True; continue
            (ctx.move_to if first else ctx.line_to)(s.X(x), s.Y(y)); first = False
        ctx.stroke()
    def dot(s, ctx, x, y, c, k=1, r=8): 
        if k > 0: disc(ctx, s.X(x), s.Y(y), r * clamp(k * 1.5), c)
