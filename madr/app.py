from fastapi import FastAPI

from madr.routers.contas import router as contas_router

app = FastAPI()
app.include_router(contas_router)
