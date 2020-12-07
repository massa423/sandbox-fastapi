from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from starlette.templating import Jinja2Templates, _TemplateResponse
from starlette.requests import Request
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_405_METHOD_NOT_ALLOWED

import db
from models import User, Task

import hashlib
import re

from mycalendar import MyCalendar
from datetime import datetime, timedelta

pattern = re.compile(r'\w{4,20}')
pattern_pw = re.compile(r'\w{6,20}')
pattern_mail = re.compile(r'^\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$')

app = FastAPI(
    title='FastAPIで作るToDoアプリケーション',
    description='FastAPiチュートリアル:FastAPI(とstarlette)でシンプルなToDoアプリを作りましょう。',
    version='0.9 beta')

templates = Jinja2Templates(directory="templates")
jinja_env = templates.env

security = HTTPBasic()


def index(request: Request) -> _TemplateResponse:
    """
    index
    """
    return templates.TemplateResponse('index.html', {'request': request})


def admin(
    request: Request, credentials: HTTPBasicCredentials = Depends(security)
) -> _TemplateResponse:
    """
    admin
    """
    username = credentials.username
    password = hashlib.sha256(credentials.password.encode()).hexdigest()

    user = db.session.query(User).filter(User.username == username).first()
    task = db.session.query(Task).filter(
        Task.user_id == user.id).all() if user is not None else []
    db.session.close()

    if user is None or user.password != password:
        error = 'ユーザ名かパスワードが間違ってます'
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED,
                            detail=error,
                            headers={"WWW-Authentication": "Basic"})

    today = datetime.now()
    next_w = today + timedelta(days=7)

    cal = MyCalendar(username,
                     {t.deadline.strftime('%Y%m%d'): t.done
                      for t in task})
    c: str = cal.formatyear(today.year, 4)

    task = [t for t in task if today <= t.deadline <= next_w]
    links = [
        t.deadline.strftime('/todo/' + username + '/%Y/%m/%d') for t in task
    ]

    return templates.TemplateResponse(
        'admin.html', {
            'request': request,
            'user': user,
            'task': task,
            'links': links,
            'calendar': c
        })


async def register(request: Request) -> _TemplateResponse:
    """
    register
    """
    if request.method == 'GET':
        return templates.TemplateResponse('register.html', {
            'request': request,
            'username': '',
            'error': []
        })

    if request.method == 'POST':
        data = await request.form()
        username = data.get('username')
        password = data.get('password')
        password_tmp = data.get('password_tmp')
        mail = data.get('mail')

        error = []

        tmp_user = db.session.query(User).filter(
            User.username == username).first()

        if tmp_user is not None:
            error.append('同じユーザ名が存在します。')

        if password != password_tmp:
            error.append('入力したパスワードが一致しません。')

        if pattern.match(username) is None:
            error.append('ユーザ名は4〜20文字の半角英数字にしてください。')

        if pattern_pw.match(password) is None:
            error.append('パスワードは6〜20文字の半角英数字にしてください。')

        if pattern_mail.match(mail) is None:
            error.append('正しくメールアドレスを入力してください。')

        if error:
            return templates.TemplateResponse('register.html', {
                'request': request,
                'username': username,
                'error': error
            })

        user = User(username, password, mail)
        db.session.add(user)
        db.session.commit()
        db.session.close()

        return templates.TemplateResponse('complete.html', {
            'request': request,
            'username': username
        })

    msg = '許可されていません。'
    raise HTTPException(status_code=HTTP_405_METHOD_NOT_ALLOWED, detail=msg)
