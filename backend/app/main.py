from fastapi import FastAPI

from app.api.routes import router

app = FastAPI(title="AidScout API", version="0.1.0", docs_url="/docs", redoc_url=None)
app.include_router(router)
