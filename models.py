from datetime import datetime

from db import Base

from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.sql.functions import current_timestamp
from sqlalchemy.dialects.mysql import INTEGER, BOOLEAN

import hashlib

SQLITE3_NAME = "./db.sqlite3"


class User(Base):
    """
    Userテーブル

    id: 主キー
    username: ユーザ名
    password: パスワード
    mail: メールアドレス
    """

    __tablename__ = 'user'
    id = Column('id',
                INTEGER(unsigned=True),
                primary_key=True,
                autoincrement=True)
    username = Column('username', String(256))
    password = Column('password', String(256))
    mail = Column('mail', String(256))

    def __init__(self, username: str, password: str, mail: str):
        self.username = username
        self.password = hashlib.sha256(password.encode()).hexdigest()
        self.mail = mail

    def __str__(self) -> str:
        return str(self.id) + ':' + self.username


class Task(Base):
    """
    ToDoタスク

    id: 主キー
    user_id: 外部キー
    content: 内容
    deadline: 締め切り
    date: 作成日
    done: タスクを終了したか
    """

    __tablename__ = 'task'
    id = Column(
        'id',
        INTEGER(unsigned=True),
        primary_key=True,
        autoincrement=True,
    )

    user_id = Column('user_id', ForeignKey('user.id'))
    content = Column('column', String(256))
    deadline = Column(
        'deadline',
        DateTime,
        default=None,
        nullable=False,
    )
    date = Column(
        'date',
        DateTime,
        default=datetime.now(),
        nullable=False,
        server_default=current_timestamp(),
    )
    done = Column('done', BOOLEAN, default=False, nullable=False)

    def __init__(self,
                 user_id: int,
                 content: str,
                 deadline: datetime,
                 date: datetime = datetime.now()):
        self.user_id = user_id
        self.content = content
        self.deadline = deadline
        self.date = date
        self.done = False

    def __str__(self) -> str:
        return str(self.id) + \
            ': user_id -> ' + str(self.user_id) + \
            ', content -> ' + str(self.content) + \
            ', deadline -> ' + self.deadline.strftime('%Y/%m/%d - %H%M%S') + \
            ', date -> ' + self.date.strftime('%Y/%m/%d - %H%M%S') + \
            ', done -> ' + str(self.done)
