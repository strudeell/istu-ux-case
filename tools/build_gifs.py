"""Собирает пары «вайрфрейм -> готовый дизайн» и рендерит морфинг-гифки."""
import subprocess, sys
from pathlib import Path
from PIL import Image
import numpy as np

ROOT = Path(__file__).resolve().parent
OUT = ROOT.parent / "assets" / "gif"; OUT.mkdir(exist_ok=True)
PAIRS = ROOT / "pairs"; PAIRS.mkdir(exist_ok=True)
FOOT = {"final1": 2405, "final2": 2097, "final3": 2288, "final4": 1073}  # верх футера на живом сайте (px @1440)

def footer_top(wf):
    """Ищем, где начинается серая полоса футера в вайрфрейме (снизу вверх)."""
    a = np.asarray(wf.convert("L"), dtype=int)
    col = a[:, int(wf.width * .01)]
    ref = col[-3]
    for y in range(len(col) - 3, 0, -1):
        if abs(col[y] - ref) > 12:
            return y + 1
    return len(col)

for i, width in [(1, 480), (2, 560), (3, 560), (4, 560)]:
    wf = Image.open(ROOT / "wf" / f"wf{i}.png").convert("RGB")
    fin = Image.open(ROOT / "shots" / f"final{i}.png").convert("RGB")
    if i == 1:
        wf = wf.resize(fin.size, Image.LANCZOS)          # лёгкое вертикальное сжатие схемы
        comp = fin
    else:
        wf = wf.resize((1440, round(wf.height * 1440 / wf.width)), Image.LANCZOS)
        ft = footer_top(wf)
        H = wf.height
        f0 = FOOT[f"final{i}"]
        comp = Image.new("RGB", (1440, H), "white")
        comp.paste(fin.crop((0, 0, 1440, min(ft, f0))), (0, 0))
        comp.paste(fin.crop((0, f0, 1440, f0 + H - ft)), (0, ft))
        print(f"wf{i}: H={H} footer_wf={ft}")
    wf.save(PAIRS / f"wf{i}.png"); comp.save(PAIRS / f"final{i}.png")
    subprocess.run([sys.executable, str(ROOT / "make_gif.py"), str(PAIRS / f"wf{i}.png"), str(PAIRS / f"final{i}.png"), str(OUT / f"wf{i}.gif"), str(width)], check=True)
    print(f"wf{i}.gif", (OUT / f"wf{i}.gif").stat().st_size // 1024, "KB")
