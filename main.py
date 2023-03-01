import base64

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from PIL import Image
from io import BytesIO
import time
import asyncio
from pyppeteer import launch

app = FastAPI()
templates = Jinja2Templates(directory="templates")


async def take_screenshot(url):
    browser = await launch()
    page = await browser.newPage()
    await page.setViewport({'width': 1920, 'height': 1080})
    await page.goto(url)
    await asyncio.sleep(2)  # wait for page to load completely
    element = await page.querySelector('body')
    bounding_box = await element.boundingBox()
    ss_img = await element.screenshot({'clip': bounding_box})
    await browser.close()
    return Image.open(BytesIO(ss_img))


@app.get("/", response_class=HTMLResponse)
async def form(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/screenshot")
async def take_screenshot_endpoint(url: str):
    print(f"Received URL: {url}")
    cropped_image = await take_screenshot(url)
    buffered = BytesIO()
    cropped_image.save(buffered, format="PNG")
    return {"data": base64.b64encode(buffered.getvalue()).decode() }
