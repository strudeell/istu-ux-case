import asyncio
from playwright.async_api import async_playwright
from PIL import Image
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={"width": 1714, "height": 900}, device_scale_factor=1)
        await pg.goto("http://localhost:8765/", wait_until="networkidle")
        await pg.wait_for_timeout(2500)
        await pg.screenshot(path="shots/hero.png")
        await b.close()
    im = Image.open("shots/hero.png").convert("RGB")
    im.resize((1200, 630), Image.LANCZOS).save("../assets/img/og-cover.jpg", quality=88)
asyncio.run(main())
