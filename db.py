# (SQLAlchemy + Pydantic) -> SQLModel
# from __future__ import annotations
from sqlmodel import SQLModel, Field, create_engine, Session, select, or_, Relationship


class HeroTeamLink(SQLModel, table=True):
    hero_id: int | None = Field(default=None, primary_key=True, foreign_key='hero.id')
    team_id: int | None = Field(default=None, primary_key=True, foreign_key='team.id')


class Team(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    heroes: list["Hero"] = Relationship(back_populates='teams', link_model=HeroTeamLink)


class Hero(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    secret_name: str
    age: int | None = None
    teams: list[Team] = Relationship(back_populates='heroes', link_model=HeroTeamLink)


database_name = "heros.db"
sql_url = f"sqlite:///{database_name}"
engine = create_engine(sql_url, echo=True)


def create_db():
    SQLModel.metadata.create_all(engine)


def create_hero_team():
    with Session(engine) as session:
        team_preventers = Team(name='Preventers')
        team_z_force = Team(name='Z-Force')

        hero_spider_boy = Hero(name='Spider-boy', secret_name='Piter', age=18, teams=[team_preventers, team_z_force])
        hero_rusty = Hero(name='Rusty-Man', secret_name='Devid', age=22, teams=[team_preventers])
        hero_sit = Hero(name='Sit-Ice', secret_name='Animal', age=4, teams=[team_z_force, team_preventers])
        session.add(hero_spider_boy)
        session.add(hero_rusty)
        session.add(hero_sit)

        session.commit()


def hero_teams():
    with Session(engine) as session:
        hero = session.exec(select(Hero).where(Hero.name == 'Spider-boy')).one()
        print(hero.teams)
        team = session.exec(select(Team).where(Team.name == 'Preventers')).one()
        print(team)
        print(team.heroes)

def main():
    create_db()
    # create_hero_team()
    hero_teams()


if __name__ == '__main__':
    main()
