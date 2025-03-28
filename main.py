from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

# Mount the static files directory
app.mount("/static", StaticFiles(directory="frontend"), name="static")

# Set up Jinja2 templates
templates = Jinja2Templates(directory="frontend")

@app.get("/signup", response_class=HTMLResponse)
async def signup_page(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})

@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/signup")
async def signup(username: str = Form(...), email: str = Form(...), password: str = Form(...)):
    try:
        # Debugging: Return a simple "hello" response
        print(f"Received signup request: username={username}, email={email}, password={password}")
        return {"message": "hello"}
    except Exception as e:
        print(f"Error during signup: {e}")
        return {"message": "Signup failed", "error": str(e)}, 500

@app.post("/login")
async def login(username: str = Form(...), password: str = Form(...)):
    # Handle login logic here
    return {"message": "Login successful", "username": username}