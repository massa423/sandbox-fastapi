from models import SQLITE3_NAME, User, Task
from db import Base, session, engine

import os
from datetime import datetime

if __name__ == "__main__":
    path = SQLITE3_NAME
    if not os.path.isfile(path):
        Base.metadata.create_all(engine)

    admin = User(username='admin',
                 password='fastapi',
                 mail='admin@example.com')
    session.add(admin)
    session.commit()

    task = Task(
        user_id=admin.id,
        content='○○の締め切り',
        deadline=datetime(2020, 12, 6, 12, 0, 0),
    )
    print(task)
    session.add(task)
    session.commit()

    session.close()
