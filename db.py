from sqlalchemy import Boolean, Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base

SQLALCHEMY_DATABASE_URI = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URI, connect_args={"check_same_thread": False}, echo=True
)

Base = declarative_base()


class Todo(Base):
    """
    Todo
    """

    __tablename__ = "todos"
    id = Column("id", Integer, primary_key=True)
    title = Column("title", String(200))
    done = Column("done", Boolean, default=False)


Base.metadata.create_all(bind=engine)
