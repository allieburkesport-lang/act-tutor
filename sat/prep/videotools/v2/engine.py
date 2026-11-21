"""Tiny animation engine for lesson videos (cairo -> ffmpeg).
A video = list of beats. Each beat has narration audio (wav) and belongs to a scene.
A scene is a function draw(ctx, b, p, t) where b = beat index inside the scene,
p = 0..1 progress through that beat, t = seconds into the beat. Earlier beats of the
same scene are complete, so scenes draw everything from beat 0 up to b."""
import cairo, math, subprocess, json, re, os
W, H, FPS = 1280, 720, 30
def hexc(h): h = h.lstrip('#'); return tuple(int(h[i:i+2], 16) / 255 for i in (0, 2, 4))
C = dict(bg=hexc('0f172a'), bg2=hexc('172036'), ink=hexc('f1f5f9'), mute=hexc('94a3b8'), grid=hexc('1e293b'),
         blue=hexc('60a5fa'), green=hexc('4ade80'), yel=hexc('facc15'), red=hexc('f87171'), pur=hexc('c084fc'),
         org=hexc('fb923c'), pizza=hexc('f5c26b'), crust=hexc('c2803c'), brown=hexc('a16207'))
def clamp(x, a=0, b=1): return max(a, min(b, x))
def ease(x): x = clamp(x); return x * x * (3 - 2 * x)
def seg(p, a, b): return ease((p - a) / (b - a)) if b > a else (1 if p >= a else 0)
def lerp(a, b, k): return a + (b - a) * k

def col(ctx, c, a=1): ctx.set_source_rgba(*c, a)
def line(ctx, x1, y1, x2, y2, c, w=4, k=1, a=1, dash=None):
    if k <= 0: return
    col(ctx, c, a); ctx.set_line_width(w); ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    ctx.set_dash(dash or [])
    ctx.move_to(x1, y1); ctx.line_to(lerp(x1, x2, k), lerp(y1, y2, k)); ctx.stroke(); ctx.set_dash([])
def arc(ctx, cx, cy, r, a0, a1, c, w=4, k=1, a=1, dash=None):
    if k <= 0: return
    col(ctx, c, a); ctx.set_line_width(w); ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.set_dash(dash or [])
    ctx.new_sub_path(); ctx.arc(cx, cy, r, a0, lerp(a0, a1, k)); ctx.stroke(); ctx.set_dash([])
def disc(ctx, x, y, r, c, a=1):
    col(ctx, c, a); ctx.new_sub_path(); ctx.arc(x, y, r, 0, 2 * math.pi); ctx.fill()
def wedge(ctx, x, y, r, a0, a1, c, a=1, stroke=None):
    ctx.move_to(x, y); ctx.arc(x, y, r, a0, a1); ctx.close_path()
    col(ctx, c, a); ctx.fill_preserve() if stroke else ctx.fill()
    if stroke: col(ctx, stroke, a); ctx.set_line_width(2); ctx.stroke()
def rrect(ctx, x, y, w, h, r, fill=None, stroke=None, a=1, lw=2):
    ctx.new_sub_path(); ctx.arc(x + w - r, y + r, r, -math.pi / 2, 0); ctx.arc(x + w - r, y + h - r, r, 0, math.pi / 2)
    ctx.arc(x + r, y + h - r, r, math.pi / 2, math.pi); ctx.arc(x + r, y + r, r, math.pi, 3 * math.pi / 2); ctx.close_path()
    if fill: col(ctx, fill, a); ctx.fill_preserve() if stroke else ctx.fill()
    if stroke: col(ctx, stroke, a); ctx.set_line_width(lw); ctx.stroke()
def font(ctx, size, bold=True, fam='Inter'):
    ctx.select_font_face(fam, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD if bold else cairo.FONT_WEIGHT_NORMAL); ctx.set_font_size(size)
def text(ctx, s, x, y, size=28, c=None, a=1, align='l', bold=True, fam='Inter'):
    if a <= 0: return 0
    font(ctx, size, bold, fam); e = ctx.text_extents(s); w = e.x_advance
    dx = {'l': 0, 'c': -w / 2, 'r': -w}[align]
    col(ctx, c or C['ink'], a); ctx.move_to(x + dx, y); ctx.show_text(s); return w
def twidth(ctx, s, size, bold=True, fam='Inter'): font(ctx, size, bold, fam); return ctx.text_extents(s).x_advance
def write(ctx, s, x, y, size, c, k, align='l', bold=True):
    """handwriting-style reveal: characters appear left to right"""
    if k <= 0: return
    n = max(1, round(len(s) * clamp(k)))
    full = twidth(ctx, s, size, bold); dx = {'l': 0, 'c': -full / 2, 'r': -full}[align]
    text(ctx, s[:n], x + dx, y, size, c, 1, 'l', bold)
def rich(ctx, parts, x, y, size, k=1, align='l'):
    """parts = [(text, color)]; reveal by k"""
    tot = sum(len(t) for t, _ in parts); show = round(tot * clamp(k)); full = sum(twidth(ctx, t, size) for t, _ in parts)
    xx = x + {'l': 0, 'c': -full / 2, 'r': -full}[align]
    for t, c in parts:
        if show <= 0: break
        s = t[:show]; show -= len(t); text(ctx, s, xx, y, size, c); xx += twidth(ctx, t, size)
def label_box(ctx, lab, body_parts, x, y, w, c, k=1, size=26):
    if k <= 0: return
    a = clamp(k * 3)
    rrect(ctx, x, y, w, 70 if body_parts else 40, 12, fill=C['bg2'], stroke=c, a=a, lw=2)
    text(ctx, lab.upper(), x + 16, y + 22, 13, c, a)
    if body_parts: rich(ctx, body_parts, x + 16, y + 56, size, k)

def background(ctx):
    col(ctx, C['bg']); ctx.paint()
    ctx.set_line_width(1); col(ctx, C['grid'], .55)
    for x in range(0, W, 40): ctx.move_to(x, 0); ctx.line_to(x, H)
    for y in range(0, H, 40): ctx.move_to(0, y); ctx.line_to(W, y)
    ctx.stroke()

def caption(ctx, s):
    if not s: return
    size = 24; words = s.split(); lines = []; cur = ''
    for w in words:
        t = (cur + ' ' + w).strip()
        if twidth(ctx, t, size, False) > W - 220 and cur: lines.append(cur); cur = w
        else: cur = t
    if cur: lines.append(cur)
    lines = lines[-2:]
    h = 18 + 34 * len(lines)
    rrect(ctx, 90, H - h - 14, W - 180, h, 14, fill=(0, 0, 0), a=.62)
    for i, l in enumerate(lines): text(ctx, l, W / 2, H - h - 14 + 38 + 34 * i, size, C['ink'], 1, 'c', False)

def sentences(s):
    out = re.split(r'(?<=[.?!])\s+', s.strip()); return [x for x in out if x]

def render(beats, scenes, out_mp4, header, wavdir, pads=None):
    """beats: list of (scene_name, narration). scenes: name -> draw fn"""
    durs = []
    for i in range(len(beats)):
        d = float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', f'{wavdir}/{i}.wav']).decode())
        durs.append(d + (pads or {}).get(i, 0.55))
    # audio: concat wav + silence pads
    lst = []
    for i, d in enumerate(durs):
        lst.append(f"file '{os.path.abspath(wavdir)}/{i}.wav'")
        pad = d - float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', f'{wavdir}/{i}.wav']).decode())
        sil = f'{wavdir}/sil_{i}.wav'
        subprocess.run(['ffmpeg', '-y', '-v', 'error', '-f', 'lavfi', '-i', 'anullsrc=r=24000:cl=mono', '-t', f'{pad:.3f}', '-ar', '24000', '-ac', '1', sil])
        lst.append(f"file '{os.path.abspath(sil)}'")
    open(f'{wavdir}/list.txt', 'w').write('\n'.join(lst))
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-f', 'concat', '-safe', '0', '-i', f'{wavdir}/list.txt', '-ar', '24000', '-ac', '1', f'{wavdir}/all.wav'], check=True)
    # scene beat indices
    sb = []; counts = {}
    for name, _ in beats: sb.append(counts.get(name, 0)); counts[name] = counts.get(name, 0) + 1
    starts = [sum(durs[:i]) for i in range(len(durs))]; total = sum(durs)
    ff = subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'bgra', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                           '-i', f'{wavdir}/all.wav', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '20', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '128k', '-shortest', '-movflags', '+faststart', out_mp4], stdin=subprocess.PIPE)
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); ctx = cairo.Context(surf)
    nf = int(total * FPS) + 1; chapters = []
    for f in range(nf):
        t = f / FPS; i = max(k for k in range(len(starts)) if starts[k] <= t + 1e-9)
        lt = t - starts[i]; spoken = durs[i] - (pads or {}).get(i, 0.55)
        p = clamp(lt / max(.1, spoken))
        name = beats[i][0]
        background(ctx)
        scenes[name](ctx, sb[i], p, lt)
        text(ctx, header, 28, 40, 17, C['mute'], 1, 'l', True)
        # caption: sentence by share of characters
        ss = sentences(beats[i][1]); tot = sum(len(x) for x in ss); acc = 0; cur = ss[-1] if ss else ''
        for s_ in ss:
            acc += len(s_)
            if p <= acc / tot + 1e-6: cur = s_; break
        caption(ctx, cur)
        ff.stdin.write(bytes(surf.get_data()))
    ff.stdin.close(); ff.wait()
    return durs, starts

def thumb(scene_fn, b, out_png, header=None):
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); ctx = cairo.Context(surf)
    background(ctx); scene_fn(ctx, b, 1, 99)
    surf.write_to_png(out_png)
