import uvicorn
from fastapi import FastAPI
import os
from starlette.staticfiles import StaticFiles
from app.config import settings
from app.autentification.routers import user_router, own_router, roof_calculations


app = FastAPI()
app.mount(
    "/static",
    StaticFiles(directory=os.path.join(os.path.dirname(__file__), "static")),
    name="static",
)
app.include_router(user_router)
app.include_router(own_router)
app.include_router(roof_calculations)

if __name__ == "__main__":
    uvicorn.run("main:app", host=settings.HOST, port=settings.PORT, reload=True)
