"""Ждёт снятия лимита Figma REST API и выгружает 4 аватарки портретов ЦА (векторные иллюстрации) в PNG."""
import json, time, datetime, urllib.request, urllib.error
from pathlib import Path

KEY = "fOE168TDQZh9jfcdtGCQwW"
TOKEN = (Path.home() / ".figma_token").read_text().strip()
OUT = Path(__file__).resolve().parent / "ava"
OUT.mkdir(exist_ok=True)
SETS = [
    {"artem": "I37:6037;2035:22570;2027:21742", "polina": "I37:6037;2032:21978;37:5687",
     "olga": "I37:6037;2032:22278;37:5721", "dmitry": "I37:6037;2028:22170;37:5760"},
    {"artem": "2027:21742", "polina": "37:5687", "olga": "37:5721", "dmitry": "37:5760"},
]
START = datetime.datetime(2026, 10, 15, 0, 55)


def call(ids):
    url = f"https://api.figma.com/v1/images/{KEY}?ids={','.join(ids)}&format=png&scale=3"
    req = urllib.request.Request(url, headers={"X-Figma-Token": TOKEN})
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            return 200, json.load(r), 0
    except urllib.error.HTTPError as e:
        return e.code, None, int(e.headers.get("Retry-After") or 0)


wait = (START - datetime.datetime.now()).total_seconds()
if wait > 0:
    time.sleep(wait)
got = {}
for ids in SETS:
    todo = {k: v for k, v in ids.items() if k not in got}
    if not todo:
        break
    for attempt in range(3):
        code, data, retry = call(list(todo.values()))
        if code == 429 and retry and retry < 3 * 3600:
            print(f"429, жду {retry} с", flush=True)
            time.sleep(retry + 30)
            continue
        break
    if code != 200:
        print("FAIL", code, flush=True)
        continue
    for name, nid in todo.items():
        u = (data.get("images") or {}).get(nid)
        if u:
            (OUT / f"{name}.png").write_bytes(urllib.request.urlopen(u, timeout=120).read())
            got[name] = nid
print("AVATARS", sorted(got), flush=True)
