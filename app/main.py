from datetime import date
from typing import List

from fastapi import FastAPI
from fastapi import Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

from portfolio.controllers import get_symbols_data


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    market_data = None
    return templates.TemplateResponse("index.html", {"request": request})


class Symbol(BaseModel):
    name: str
    allocation: float


class SymbolsQuery(BaseModel):
    date_from: date
    initial_balance: int
    symbols: List[Symbol]


# async def handle_symbols_data(*, date_from: datetime, balance: int, symbols: List[Symbol]):
@app.post("/symbols")
async def handle_symbols_data(*, query: SymbolsQuery):
    symbols_data = await get_symbols_data(
        symbols=query.symbols, date_from=query.date_from,
        initial_balance=query.initial_balance,
        limit=500
    )
    return {"data": symbols_data}
