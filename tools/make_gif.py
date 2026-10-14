"""Морфинг-гифка: вайрфрейм плавно превращается в готовый дизайн.

python tools/make_gif.py wireframe.png final.png out.gif [ширина]
"""
import sys
from PIL import Image, ImageFilter, ImageDraw, ImageChops

FPS = 20
HOLD_A, MORPH, HOLD_B, BACK = 0.9, 1.6, 1.8, 0.7  # секунды
ACCENT = (31, 144, 236)


def ease(t):  # easeInOutCubic
    return 4 * t * t * t if t < .5 else 1 - (-2 * t + 2) ** 3 / 2


def load(path, w):
    im = Image.open(path).convert("RGB")
    return im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)


def frame_morph(a, b, t, mask_cache={}):
    """Фронт-волна сверху вниз: под волной — финальный дизайн, над ней — вайрфрейм,
    на самой границе — размытие и светящаяся линия."""
    w, h = a.size
    band = int(h * .22)
    edge = int(-band + (h + 2 * band) * t)
    key = (w, h, band)
    if key not in mask_cache:
        grad = Image.new("L", (1, band * 3))
        for y in range(band * 3):
            v = 255 if y < band else 0 if y >= 2 * band else int(255 * (1 - (y - band) / band))
            grad.putpixel((0, y), v)
        mask_cache[key] = grad.resize((w, band * 3))
    mask = Image.new("L", (w, h), 0)
    mask.paste(255, (0, 0, w, max(0, edge - band)))
    mask.paste(mask_cache[key], (0, edge - 2 * band))
    blur_b = b.filter(ImageFilter.GaussianBlur(6 * (1 - t)))
    out = Image.composite(blur_b, a, mask)
    # мягкое голубое свечение по фронту
    glow = Image.new("RGB", (w, h), ACCENT)
    gmask = Image.new("L", (w, h), 0)
    d = ImageDraw.Draw(gmask)
    for i in range(18):
        y = edge - band + i - 9
        d.line([(0, y), (w, y)], fill=int(140 * (1 - abs(i - 9) / 9) * min(1, 5 * (1 - t), 5 * t)))
    out = Image.composite(glow, out, gmask)
    return out


def main():
    wf, fin, dst = sys.argv[1:4]
    width = int(sys.argv[4]) if len(sys.argv) > 4 else 640
    a, b = load(wf, width), load(fin, width)
    if b.size != a.size:  # подгоняем высоту финала к вайрфрейму (кроп сверху)
        b = b.crop((0, 0, a.width, a.height)) if b.height >= a.height else b.resize(a.size, Image.LANCZOS)
    frames, durs = [], []

    def add(im, ms):
        frames.append(im)
        durs.append(ms)

    add(a, int(HOLD_A * 1000))
    n = int(MORPH * FPS)
    for i in range(1, n):
        add(frame_morph(a, b, ease(i / n)), int(1000 / FPS))
    add(b, int(HOLD_B * 1000))
    n = int(BACK * FPS)
    for i in range(1, n):
        add(Image.blend(b, a, ease(i / n)), int(1000 / FPS))

    # общая палитра по вайрфрейму + финалу + кадру со свечением — без мерцания и потери цвета
    probe = Image.new("RGB", (a.width * 3, a.height))
    probe.paste(a, (0, 0)); probe.paste(b, (a.width, 0)); probe.paste(frames[len(frames) // 3], (a.width * 2, 0))
    pal = probe.quantize(colors=255, method=Image.Quantize.FASTOCTREE)
    q = [f.quantize(palette=pal, dither=Image.FLOYDSTEINBERG) for f in frames]
    q[0].save(dst, save_all=True, append_images=q[1:], duration=durs, loop=0, optimize=True, disposal=1)


if __name__ == "__main__":
    main()
