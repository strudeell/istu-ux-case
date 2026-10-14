import asyncio, sys
from playwright.async_api import async_playwright
from PIL import Image
W = int(sys.argv[1]) if len(sys.argv) > 1 else 1440
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={"width": W, "height": 900}, device_scale_factor=1)
        errs = []
        pg.on("console", lambda m: errs.append(m.text) if m.type == "error" else None)
        pg.on("pageerror", lambda e: errs.append(str(e)))
        await pg.goto("http://localhost:8765/", wait_until="networkidle"); await pg.add_style_tag(content="html{scroll-behavior:auto!important}")
        y = 0
        while y < await pg.evaluate("document.documentElement.scrollHeight"):
            await pg.evaluate(f"window.scrollTo(0,{y})"); await pg.wait_for_timeout(120); y += 400
        h = await pg.evaluate("document.documentElement.scrollHeight")
        await pg.wait_for_timeout(1500)
        await pg.evaluate("window.scrollTo(0,0)"); await pg.wait_for_timeout(300)
        await pg.screenshot(path=f"shots/local{W}.png", full_page=True)
        print("height", h, "errors", errs)
        await b.close()
    im = Image.open(f"shots/local{W}.png").convert("RGB")
    step = 1800 if W > 800 else 2400
    n = 0
    for y in range(0, im.height, step):
        c = im.crop((0, y, im.width, min(im.height, y + step)))
        sc = 760 / c.width if W > 800 else 1
        c.resize((round(c.width * sc), round(c.height * sc))).save(f"shots/l{W}_{n}.jpg", quality=72); n += 1
    print("chunks", n)
asyncio.run(main())
