"""API instance runner."""

from fastapi import FastAPI

from .routers import auth, stock_market


app = FastAPI()

app.include_router(auth.router)
app.include_router(stock_market.router)
