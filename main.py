from typing import Union

from fastapi import FastAPI, Request, Depends, Form, HTTPException
from fastapi.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
from sqlalchemy.orm import Session


from connection import base, engine, sess_db
from models import UserModel
from repositoryuser import UserRepository, SendEmailVerif
from scurity import get_password_hash, create_access_token

template = Jinja2Templates(directory="templates")

app = FastAPI()
app.mount(path="/static", app=StaticFiles(directory="static", html=True), name="static")

base.metadata.create_all(bind=engine)

@app.get("/")
def home(request: Request):
    return template.TemplateResponse("/index.html", {"request": request})

@app.get("/about")
def about(request: Request):
    return template.TemplateResponse("/about.html", {"request": request})

@app.get("/user/signin")
def signin(request: Request):
    return template.TemplateResponse("/signin.html", {"request": request})

@app.get("/user/signup")
def signup(request: Request):
    return template.TemplateResponse("/signup.html", {"request": request})

@app.post("/signupuser")
def signup_user(db: Session = Depends(sess_db), username: str = Form(), email: str = Form(), password: str = Form()):
    print(username)
    print(email)
    print(password)
    user_repository = UserRepository(db)

    db_user = user_repository.get_user_by_username(username)
    if db_user:
        return 'username is not valid'

    sign_up = UserModel(email=email, username=username, password=get_password_hash(password))
    success = user_repository.create_user(signup=sign_up)
    #token = create_access_token(user=sign_up)
    #print("token", token)
    # SendEmailVerif.send_verif(token)


    if success:
        return "create user successfully"
    else:
        raise HTTPException(status_code=401, detail="Credentials not correct")
