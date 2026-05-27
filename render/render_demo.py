"""Render demo.html to webm via headless Chromium for 62 seconds."""
import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

HTML_PATH = "/Users/dtribe/Projects/job-search-agent/render/demo.html"
OUT_DIR = "/tmp/svg_render"


async def main():
    Path(OUT_DIR).mkdir(exist_ok=True)
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            viewport={"width": 1920, "height": 1080},
            device_scale_factor=2,
            record_video_dir=OUT_DIR,
            record_video_size={"width": 1920, "height": 1080},
        )
        page = await context.new_page()
        await page.goto(f"file://{HTML_PATH}")
        await page.wait_for_timeout(62_000)
        await context.close()
        await browser.close()


asyncio.run(main())
