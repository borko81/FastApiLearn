from fastapi import FastAPI, Depends, Response
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_login import LoginManager
from fastapi_login.exceptions import InvalidCredentialsException

from datetime import timedelta


app = FastAPI()
SECRET = "cd8a438980c40eaef20a263bb0062d0989f30ac2229f784a"
manager = LoginManager(
    SECRET, "/login", use_cookie=True, default_expiry=timedelta(minutes=10)
)
manager.cookie_name = "borko"


DB = {"borko": {"password": "borko"}}


@manager.user_loader
def load_user(username: str):
    return DB.get(username)


@app.post("/login")
def login(response: Response, data: OAuth2PasswordRequestForm = Depends()):
    username = data.username
    password = data.password

    user = load_user(username)
    if not user:
        raise InvalidCredentialsException
    elif password != user["password"]:
        raise InvalidCredentialsException

    access_token = manager.create_access_token(data={"sub": username})
    manager.set_cookie(response, access_token)
    return access_token


@app.post("/logout")
async def logout(
    response: Response,
):
    response.delete_cookie("borko")
    return {"status": "success"}


@app.get("/protected")
def protected_url(_=Depends(manager)):
    return {"message": "success"}
