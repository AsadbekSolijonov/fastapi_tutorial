# (SQLAlchemy + Pydantic) -> SQLModel
# from __future__ import annotations
from sqlmodel import SQLModel, Field, create_engine, Session, select, or_, Relationship, text


class Team(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    heroes: list["Hero"] = Relationship(back_populates='team', cascade_delete=True)


class Hero(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    secret_name: str
    age: int | None = None
    team_id: int | None = Field(default=None, foreign_key='team.id', ondelete='CASCADE')
    team: Team | None = Relationship(back_populates='heroes')

    # address: "Address" = Relationship(back_populates='hero')


# class Address(SQLModel, table=True):
#     hero_id: int | None = Field(default=None, foreign_key='hero.id', unique=True)
#     hero: Hero = Relationship(back_populates='address')
#
#
# class HeroTeam(SQLModel, table=True):
#     hero_id: int = Field(foreign_key='hero.id')
#     team_id: int = Field(foreign_key='team.id')


# SELECT * FROM users Where id=2; DROP table users;  # hujumchi client


# Dbeaver(Yengil, Mysql, Sql, Postgres, MongoDb), Pgadmin 4 (Interface)

database_name = "heros.db"
sql_url = f"sqlite:///{database_name}"
engine = create_engine(sql_url, echo=True)


def create_db():
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        session.execute(text('pragma foreign_keys=on'))  # only for sqlite


def create_team_hero():
    with Session(engine) as session:
        team_stars = Team(name='Stars')
        team_sun = Team(name='Sun')
        session.add(team_stars)
        session.add(team_sun)
        session.commit()

        hero_spiderman = Hero(name='Spiderman', secret_name='Piter', team_id=team_stars.id)
        hero_hulk = Hero(name='Hulk', secret_name='Bruse', team_id=team_stars.id)
        hero_amerika = Hero(name='Capitan America', secret_name='Stiff', team_id=team_sun.id)

        session.add(hero_spiderman)
        session.add(hero_hulk)
        session.add(hero_amerika)
        session.commit()


def create_team_hero_with_related_attributes():
    with Session(engine) as session:
        team_ocean = Team(name='Ocean')
        team_mountain = Team(name='Mountain')

        hero_spiderman = Hero(name='Kunfu panda', secret_name='Po', team=team_ocean)
        hero_hulk = Hero(name='Shifu', secret_name='Ustoz', team=team_mountain)
        hero_amerika = Hero(name='Ugvay', secret_name='Turtle', team=team_ocean)

        session.add(hero_spiderman)
        session.add(hero_hulk)
        session.add(hero_amerika)
        session.commit()


def create_hero_team():
    with Session(engine) as session:
        hero_sit = Hero(name='Sit', secret_name='Yalqov sit', age=5)
        hero_mamunt = Hero(name='Mamunt', secret_name='Elephent', age=7)

        team_ice = Team(name='Ice', heroes=[hero_sit, hero_mamunt])
        session.add(team_ice)
        session.commit()


def get_heroes():
    with Session(engine) as session:
        statement = select(Hero)
        results = session.exec(statement).all()
        for result in results:
            print(result)


def get_heroes_limit():
    with Session(engine) as session:
        statement = select(Hero).limit(3)
        results = session.exec(statement)
        for result in results:
            print(result)


def get_heroes_limit_offset():
    with Session(engine) as session:
        statement = select(Hero).limit(3).offset(1)
        results = session.exec(statement)
        for result in results:
            print(result)


def update_hero():
    with Session(engine) as session:
        statement = select(Hero).where(Hero.name == 'Sit')
        result = session.exec(statement)
        hero_sit = result.one()
        hero_sit.name = 'Sit ice'
        session.add(hero_sit)
        session.commit()
        session.refresh(hero_sit)
        print(F"Hero sit:", hero_sit)


def delete_team():
    with Session(engine) as session:
        statement = select(Team).where(Team.name == 'Ice')
        result = session.exec(statement)
        team_ice = result.one()
        session.delete(team_ice)
        session.commit()


def main():
    create_db()
    create_team_hero()
    create_team_hero_with_related_attributes()
    create_hero_team()
    # get_heroes()
    # get_heroes_limit()
    # get_heroes_limit_offset()
    # update_hero()
    # delete_team()   # orm


if __name__ == '__main__':
    main()
