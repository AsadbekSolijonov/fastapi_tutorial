# (SQLAlchemy + Pydantic) -> SQLModel
from __future__ import annotations
from sqlmodel import SQLModel, Field, create_engine


class Hero(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    secret_name: str
    age: int | None = None


# Dbeaver(Yengil, Mysql, Sql, Postgres, MongoDb), Pgadmin 4 (Interface)

database_name = "heros.db"
sql_url = f"sqlite:///{database_name}"
engine = create_engine(sql_url, echo=True)

if __name__ == '__main__':
    SQLModel.metadata.create_all(engine)
