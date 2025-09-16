# (SQLAlchemy + Pydantic) -> SQLModel
from __future__ import annotations
from sqlmodel import SQLModel, Field, create_engine, Session, select, or_


class Team(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str


class Hero(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    secret_name: str
    age: int | None = None
    team_id: int | None = Field(default=None, foreign_key='team.id')


# SELECT * FROM users Where id=2; DROP table users;  # hujumchi client
# Dbeaver(Yengil, Mysql, Sql, Postgres, MongoDb), Pgadmin 4 (Interface)

database_name = "heros.db"
sql_url = f"sqlite:///{database_name}"
engine = create_engine(sql_url, echo=True)


def create_db():
    SQLModel.metadata.create_all(engine)


def creating_hero():
    with Session(engine) as session:
        hero_spiderman = Hero(name='Spiderman', secret_name='Piter Parker', age=18)
        print(f"\tSession ga qo'shilishidan avval:")
        print(f"\tSpiderman: {hero_spiderman}")

        session.add(hero_spiderman)
        print(f"\tSession ga qo'shilishidan keyin:")
        print(f"\tSpiderman: {hero_spiderman}")

        session.commit()
        print(f"\tCommitga qo'shilishidan keyin:")
        print(f"\tSpiderman: {hero_spiderman}")
        print(f"\tSpiderman ID: {hero_spiderman.id}")

        session.refresh(hero_spiderman)
        print(f"\tRefresh qilinganda keyin:")
        print(f"\tSpiderman: {hero_spiderman}")
        print(f"\tSpiderman ID: {hero_spiderman.id}")


def read_hero():
    with Session(engine) as session:
        # AND
        # statement = select(Hero).where(Hero.name == 'Spiderman').where(Hero.age==18)
        # statement = select(Hero).where(Hero.name == 'Spiderman', Hero.age == 18)

        # OR
        # statement = select(Hero).where(or_(Hero.name == 'Spiderman', Hero.age == 18))

        # get
        hero_spiderman = session.get(Hero, 1)
        # result = session.exec(statement)
        # hero_spiderman = result.first()
        print(F"\tHero: {hero_spiderman}")


def update_hero():
    with Session(engine) as session:
        hero_spiderman = session.get(Hero, 1)
        print(F"\tHero: {hero_spiderman}")
        hero_spiderman.age = 25
        print(f"\tSessionga qo'shilishidan avval:")
        print(f"\tHero: {hero_spiderman}")

        session.add(hero_spiderman)
        print(f"\tSessionga qo'shilishidan keyin:")
        print(f"\tHero: {hero_spiderman}")

        session.commit()
        print(f"\tCommit qilingandan keyin:")
        print(f"\tHero: {hero_spiderman}")

        session.refresh(hero_spiderman)
        print(f"\tRefresh qilingandan keyin:")
        print(f"\tHero: {hero_spiderman}")


def delete_hero():
    with Session(engine) as session:
        hero_spiderman = session.get(Hero, 1)
        print(F"\tObyekt o'chirilishidan avval:")
        print(F"\tHero: {hero_spiderman}")
        session.delete(hero_spiderman)
        print(F"\tObyekt o'chirilishidan keyin:")
        print(F"\tHero: {hero_spiderman}")
        session.commit()
        print(F"\tCommit qilingandan keyin:")
        print(F"\tHero: {hero_spiderman}")
        hero_spiderman.age = 35
        session.add(hero_spiderman)
        session.commit()
        session.refresh(hero_spiderman)
        print(hero_spiderman)
    print(f"\tSessiondan tashqaridagi xolat:")
    print(F"\tHero: {hero_spiderman}")


def main():
    create_db()
    # creating_hero()
    # read_hero()
    # update_hero()
    # delete_hero()


if __name__ == '__main__':
    main()
