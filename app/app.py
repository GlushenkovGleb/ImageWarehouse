from fastapi import FastAPI

from .api import image, auth

app = FastAPI()

app.include_router(image.router)
app.include_router(auth.router)
