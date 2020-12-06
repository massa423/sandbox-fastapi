from fastapi import FastAPI
from starlette.requests import Request
from starlette.templating import Jinja2Templates, _TemplateResponse

app = FastAPI(
    title='FastAPIで作るToDoアプリケーション',
    description='FastAPiチュートリアル:FastAPI(とstarlette)でシンプルなToDoアプリを作りましょう。',
    version='0.9 beta')

templates = Jinja2Templates(directory="templates")
jinja_env = templates.env


def index(request: Request) -> _TemplateResponse:
    """
    index
    """
    return templates.TemplateResponse('index.html', {'request': request})


def admin(request: Request) -> _TemplateResponse:
    """
    admin
    """
    return templates.TemplateResponse('admin.html', {
        'request': request,
        'username': 'admin'
    })
