from sqlmodel import SQLModel


class User(SQLModel, table=True):
    pass
