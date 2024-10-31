from fastapi import FastAPI

from madr.routers.auth import router as auth_router
from madr.routers.contas import router as contas_router
from madr.routers.romancistas import router as romancista_router

app = FastAPI()
app.include_router(auth_router)
app.include_router(contas_router)
app.include_router(romancista_router)
