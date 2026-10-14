"""Готовит изображения из Figma для сайта: кроп как в макете, плашки-цензура, WebP."""
import sys
from pathlib import Path
from PIL import Image, ImageDraw

RAW = Path(sys.argv[1])          # папка с исходниками из Figma (image fills)
ROOT = Path(__file__).resolve().parent.parent
IMG = ROOT / "assets" / "img"


def cover(im, w, h):
    s = max(w / im.width, h / im.height)
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    l, t = (im.width - w) // 2, (im.height - h) // 2
    return im.crop((l, t, l + w, t + h))


def crop_tf(im, tf):
    """imageTransform из Figma (режим STRETCH) -> область исходника."""
    (sx, _, tx), (_, sy, ty) = tf
    W, H = im.size
    return im.crop((round(tx * W), round(ty * H), round((tx + sx) * W), round((ty + sy) * H)))


def save(im, name, q=86):
    im.save(IMG / f"{name}.webp", "WEBP", quality=q, method=6)
    print(name, im.size, (IMG / f"{name}.webp").stat().st_size // 1024, "KB")


def bars(im, node_w, rects):
    """Чёрные плашки поверх скриншотов (скрытие персональных данных) — координаты из макета."""
    k = im.width / node_w
    d = ImageDraw.Draw(im)
    for x, y, w, h, r in rects:
        d.rounded_rectangle([x * k, y * k, (x + w) * k, (y + h) * k], radius=r * k, fill=(10, 12, 12))
    return im


def raw(name):
    return Image.open(RAW / name).convert("RGB")


# --- уже скачанные через MCP картинки (hero, AS IS) ---
for n in ["hero-old", "hero-new"] + [f"asis-{i:02d}" for i in range(1, 11)]:
    src = IMG / f"{n}.png"
    if src.exists():
        im = Image.open(src).convert("RGB")
        w, h = (510, 1038) if n == "hero-new" else (498, 1012) if n == "hero-old" else (498, 1014)
        save(cover(im, w, h), n)
        src.unlink()
src = IMG / "hero-logo-bg.png"
if src.exists():
    im = Image.open(src)
    im = im.resize((1940, round(im.height * 1940 / im.width)), Image.LANCZOS)
    im.save(IMG / "hero-logo-bg.webp", "WEBP", quality=80, method=6)
    src.unlink()

# --- юзабилити: 3x от размера в макете, с плашками ---
K = 3
im = crop_tf(raw("usab-1"), [[1, 0, 0], [0, .7905, .0392]]).resize((306 * K, 169 * K), Image.LANCZOS)
save(bars(im, 306, [(164, 29, 45, 5, 0)]), "usab-1")
save(cover(raw("usab-2"), 306 * K, round(172.4 * K)), "usab-2")
save(bars(cover(raw("usab-3"), 306 * K, 169 * K), 306, [(159, 23, 29, 4, 2), (138, 145, 29, 4, 2)]), "usab-3")
save(bars(cover(raw("usab-4"), 306 * K, 169 * K), 306, [(159, 25.47, 27, 3.92, 2), (139, 147.06, 29, 3.92, 2)]), "usab-4")
save(cover(raw("usab-sus"), 1216, 714), "usab-sus")

# --- опрос ---
save(crop_tf(raw("survey-charts"), [[.98146, 0, .01739], [0, .81991, .07213]]), "survey-charts")
im = crop_tf(raw("survey-filters"), [[.96005, 0, 0], [0, .99958, .00021]])
save(im.resize((1600, round(im.height * 1600 / im.width)), Image.LANCZOS), "survey-filters")
p = raw("survey-params")  # склейка из трёх кусков, как в макете (630x297)
W2 = 1260
parts = [(.91169, .94026, 11), (0, .65714, 253), (.91169, 1.0, 34)]
out = Image.new("RGB", (W2, sum(h for *_, h in parts) * 2), "white")
y = 0
for a, b, h in parts:
    piece = p.crop((0, round(a * p.height), p.width, round(b * p.height))).resize((W2, h * 2), Image.LANCZOS)
    out.paste(piece, (0, y))
    y += h * 2
save(out, "survey-params")

# --- дизайн-решение, спасибо ---
save(cover(raw("uikit-cover"), 912, 513), "uikit-cover")
save(raw("thanks"), "thanks")

# --- вайрфреймы (исходники для гифок) ---
wf = ROOT / "tools" / "wf"
wf.mkdir(exist_ok=True)
crop_tf(raw("wf1"), [[.99961, 0, .00019], [0, 1, 0]]).save(wf / "wf1.png")
cover(raw("wf2"), 1830, 1656).save(wf / "wf2.png")
cover(raw("wf3"), 1830, 1656).save(wf / "wf3.png")
crop_tf(raw("wf4"), [[.99979, 0, .00011], [0, .94198, 0]]).save(wf / "wf4.png")
print("wireframes ready")
