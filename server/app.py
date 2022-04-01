from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import requests


app = FastAPI()


app.mount("/static", StaticFiles(directory="../static"), name="static")

templates = Jinja2Templates(directory="../templates")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})


@app.get("/cep", response_class=HTMLResponse)
async def find_cep(request: Request, cep: int):
    url = f"https://cep.awesomeapi.com.br/json/{cep}"

    res = requests.get(url)
    res = res.json()

    address = res["address"]
    district = res["district"]
    city = res["city"]

    return templates.TemplateResponse(
        "searchResult.html", {
            "request": request, 
            "address": address, 
            "city": city,
            "district": district,            
        }
    )
