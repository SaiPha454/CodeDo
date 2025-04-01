from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.middleware.sessions import SessionMiddleware
from starlette.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from config.dbcon import Base, engine

from routers import auth_router
from routers import questioner_router
from routers import questioner_challenge_router

templates = Jinja2Templates(directory="templates")

app = FastAPI()

# Add session middleware
app.add_middleware(SessionMiddleware, secret_key="your_secret_key")

# Mount StaticFiles middleware
app.mount("/static", StaticFiles(directory="static"), name="static")

# Include routers
app.include_router(auth_router.router)
# app.include_router(questioner_router.router)
app.include_router(questioner_challenge_router.router)


@app.exception_handler(401)
async def not_found_handler(request, exc):
    print("hello 404")
    return templates.TemplateResponse("401.html", {"request": request}, status_code=401)

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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)