from fastapi import FastAPI, Request, Form, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
from starlette.middleware.sessions import SessionMiddleware
from dbcon import Base, engine, get_db
from models import User
import bcrypt

app = FastAPI()

# Add session middleware
app.add_middleware(SessionMiddleware, secret_key="your_secret_key")

# Mount the static files directory
app.mount("/static", StaticFiles(directory="frontend"), name="static")

# Set up Jinja2 templates
templates = Jinja2Templates(directory="frontend")

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        # Create tables if they don't exist
        await conn.run_sync(Base.metadata.create_all)

@app.on_event("shutdown")
async def shutdown():
    await engine.dispose()

def is_logged_in(request: Request):
    """Check if the user is logged in."""
    return request.session.get("user_id") is not None

@app.get("/signup", response_class=HTMLResponse)
async def signup_page(request: Request):
    if is_logged_in(request):
        return RedirectResponse(url="/dashboard", status_code=302)
    return templates.TemplateResponse("signup.html", {"request": request})

@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    if is_logged_in(request):
        return RedirectResponse(url="/dashboard", status_code=302)
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/signup")
async def signup(
    request: Request,
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    db: AsyncSession = Depends(get_db)
):
    try:
        # Hash the password
        hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
        # Create a new user
        new_user = User(username=username, email=email, password=hashed_password.decode("utf-8"))
        db.add(new_user)
        await db.commit()

        # Log the user in by storing their session
        request.session["user_id"] = new_user.id
        return RedirectResponse(url="/dashboard", status_code=302)
    except SQLAlchemyError as e:
        await db.rollback()
        print(f"Error during signup: {e}")
        return {"message": "Signup failed", "error": str(e)}, 500

@app.post("/login")
async def login(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    db: AsyncSession = Depends(get_db)
):
    # Verify user credentials by email
    result = await db.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()
    if user and bcrypt.checkpw(password.encode("utf-8"), user.password.encode("utf-8")):
        # Store user session
        request.session["user_id"] = user.id
        return RedirectResponse(url="/dashboard", status_code=302)
    raise HTTPException(status_code=401, detail="Invalid credentials")

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    if not is_logged_in(request):
        return RedirectResponse(url="/login", status_code=302)
    return templates.TemplateResponse("main/dashboard.html", {"request": request, "user_id": request.session["user_id"]})

@app.get("/logout")
async def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/login", status_code=302)