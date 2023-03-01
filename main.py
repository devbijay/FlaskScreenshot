import base64

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from PIL import Image
from io import BytesIO
import asyncio
from pyppeteer import launch

app = FastAPI()
templates = Jinja2Templates(directory="templates")


async def take_screenshot(url):
    try:
        browser = await launch(headless=True)
        page = await browser.newPage()
        await page.setViewport({'width': 1920, 'height': 1080})
        await page.goto(url)
        await asyncio.sleep(2)
        ss_img = await page.screenshot({'type': 'png', 'fullPage': False})
        await browser.close()
        return Image.open(BytesIO(ss_img))
    except Exception:
        with open("404.png", 'rb') as f:
            img_bytes = f.read()
        return Image.open(BytesIO(img_bytes))


@app.get("/", response_class=HTMLResponse)
async def form(request: Request):
    title = """🅟🅨🅢🅒🅡🅔🅔🅝🅢🅗🅞🅣"""
    return templates.TemplateResponse("index.html", {"request": request, "title": title})


@app.get("/screenshot")
async def take_screenshot_endpoint(url: str):
    print(f"Received URL: {url}")
    cropped_image = await take_screenshot(url)
    buffered = BytesIO()
    cropped_image.save(buffered, format="PNG")
    return {"data": base64.b64encode(buffered.getvalue()).decode()}
