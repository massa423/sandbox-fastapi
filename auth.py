import hashlib
import db
from fastapi.security import HTTPBasicCredentials
from models import User
from starlette.status import HTTP_401_UNAUTHORIZED
from fastapi import HTTPException


def auth(credentials: HTTPBasicCredentials) -> str:
    """
    Basic認証チェック
    """
    username = credentials.username
    password = hashlib.sha256(credentials.password.encode()).hexdigest()

    user = db.session.query(User).filter(User.username == username).first()
    db.session.close()

    if user is None or user.password != password:
        error = "ユーザ名かパスワードが間違ってます"
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail=error,
            headers={"WWW-Authentication": "Basic"},
        )
    return username
