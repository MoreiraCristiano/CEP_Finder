import requests
import uvicorn
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


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
    parsed_res = res.json()
    
    if (res.status_code != 200):
        return templates.TemplateResponse("home.html", {"request": request})

    address = parsed_res["address"]
    district = parsed_res["district"]
    city = parsed_res["city"]

    return templates.TemplateResponse(
        "searchResult.html",
        {
            "request": request,
            "address": address,
            "city": city,
            "district": district,
        },
    )


if __name__ == "__main__":
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
