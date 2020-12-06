from models import SQLITE3_NAME, User, Task
import db
from db import Base

import os
from datetime import datetime

if __name__ == "__main__":
    path = SQLITE3_NAME
    if not os.path.isfile(path):
        Base.metadata.create_all(db.engine)

    admin = User(username='admin',
                 password='fastapi',
                 mail='admin@example.com')
    db.session.add(admin)
    db.session.commit()

    task = Task(
        user_id=admin.id,
        content='○○の締め切り',
        deadline=datetime(2020, 12, 6, 12, 0, 0),
    )
    print(task)
    db.session.add(task)
    db.session.commit()

    db.session.close()
