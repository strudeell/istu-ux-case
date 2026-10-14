import asyncio
from playwright.async_api import async_playwright
BASE = "https://strudeell.github.io/istu-redesign/"
async def shot(pg, url, name, click=None):
    await pg.goto(BASE + url, wait_until="networkidle")
    if click:
        await pg.click(click); await pg.wait_for_timeout(800)
    await pg.evaluate("window.scrollTo(0, document.body.scrollHeight)"); await pg.wait_for_timeout(600)
    await pg.evaluate("window.scrollTo(0, 0)"); await pg.wait_for_timeout(600)
    await pg.screenshot(path=f"shots/{name}.png", full_page=True)
    f = await pg.evaluate("(() => { const f = document.querySelector('footer'); if(!f) return null; const r = f.getBoundingClientRect(); return [r.top + scrollY, r.height]; })()")
    h = await pg.evaluate("document.documentElement.scrollHeight")
    print(name, h, "footer", f)
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={"width": 1440, "height": 900})
        await shot(pg, "index.html", "final1")
        await shot(pg, "programs.html", "final2")
        await shot(pg, "programs.html", "final3", click=".view-btn:nth-of-type(2)")
        await shot(pg, "program.html?id=80", "final4")
        await b.close()
asyncio.run(main())
