from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
from starlette.staticfiles import StaticFiles
from dbcon import Base, engine
from routers import auth, dashboard

app = FastAPI()

# Add session middleware
app.add_middleware(SessionMiddleware, secret_key="your_secret_key")

# Mount StaticFiles middleware
app.mount("/static", StaticFiles(directory="frontend"), name="static")

# Include routers
app.include_router(auth.router)
app.include_router(dashboard.router)

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.on_event("shutdown")
async def shutdown():
    await engine.dispose()