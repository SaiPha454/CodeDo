from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.middleware.sessions import SessionMiddleware
from starlette.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from dbcon import Base, engine
from routers import auth
from routers.participant import participant_router
from routers.questioner import questioner_router

templates = Jinja2Templates(directory="frontend/main")

app = FastAPI()

# Add session middleware
app.add_middleware(SessionMiddleware, secret_key="your_secret_key")

# Mount StaticFiles middleware
app.mount("/static", StaticFiles(directory="frontend"), name="static")

# Include routers
app.include_router(auth.router)
# app.include_router(dashboard.router)

# Include participant and questioner routers
app.include_router(participant_router)
app.include_router(questioner_router)

@app.exception_handler(404)
async def not_found_handler(request, exc):
    print("hello 404")
    return templates.TemplateResponse("404.html", {"request": request}, status_code=404)

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    if exc.status_code == 403:
        print("hello 403")
        return templates.TemplateResponse("403.html", {"request": request}, status_code=403)
    raise exc

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.on_event("shutdown")
async def shutdown():
    await engine.dispose()