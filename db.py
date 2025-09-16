# (SQLAlchemy + Pydantic) -> SQLModel
# from __future__ import annotations

from typing import Optional, cast, Any

from sqlmodel import SQLModel, Relationship, Field, create_engine, Session, select, col, text


class Team(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    headquarters: str
    # heroes: list["Hero"] = Relationship(back_populates='team', cascade_delete=True)  # python tomondan o'chirish
    heroes: list["Hero"] = Relationship(back_populates='team')  # SET NULL


class Hero(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    secret_name: str
    age: int | None = Field(default=None, index=True)
    # team_id: int | None = Field(default=None, foreign_key='team.id', ondelete='CASCADE')  # SQL tomondan o'chirish
    team_id: int | None = Field(default=None, foreign_key='team.id', ondelete='SET NULL')  # SQL tomondan SET NULL
    team: Team | None = Relationship(back_populates='heroes')


# Dbeaver(Yengil, Mysql, Sql, Postgres, MongoDb), Pgadmin 4 (Interface)

database_name = "heros.db"
sql_url = f"sqlite:///{database_name}"
engine = create_engine(sql_url, echo=True)


def creata_db_or_tabales():
    SQLModel.metadata.create_all(engine)
    with engine.connect() as connection:
        connection.execute(text("PRAGMA foreign_keys=ON"))  # bu faqat SQLite uchun.


def create_heroes():
    with Session(engine) as session:
        team_preventers = Team(name='Preventers', headquarters='Sharp Tower')
        team_z_force = Team(name='Z-force', headquarters='Sister Margaret`s Bar')
        session.add(team_preventers)
        session.add(team_z_force)
        session.commit()

        hero_deadpond = Hero(name='Deadpond', secret_name='Dive Wilson', team_id=team_z_force.id)
        hero_rusty_man = Hero(name='Rusty-Man', secret_name='Tommy Sharp', age=48, team_id=team_preventers.id)
        hero_spider_boy = Hero(name='Spider-boy', secret_name='Pedro Parqueador')
        session.add(hero_deadpond)
        session.add(hero_rusty_man)
        session.add(hero_spider_boy)
        session.commit()

        session.refresh(hero_deadpond)
        session.refresh(hero_rusty_man)
        session.refresh(hero_spider_boy)

        print(f"\tCreated hero:", hero_deadpond)
        print(f"\tCreated hero:", hero_rusty_man)
        print(f"\tCreated hero:", hero_spider_boy)


def create_with_relation_attr():
    with Session(engine) as session:
        team_oracle = Team(name='Oracle', headquarters='Deamon Oracle')
        team_model = Team(name='Model', headquarters='I have a pen')

        hero_betman = Hero(name='Betman', secret_name='Olga Cleis', age=34, team=team_oracle)
        hero_moonstart = Hero(name='MoonStar', secret_name='Rust Yoluign', age=25, team=team_oracle)
        hero_superman = Hero(name='Superman', secret_name='Devid Martin', age=28, team=team_model)

        session.add(hero_betman)
        session.add(hero_moonstart)
        session.add(hero_superman)

        session.commit()

        print("\tBefore refresh Hero objects")
        print(f"\tHero 1:", hero_betman)
        print(f"\tHero 2:", hero_superman)
        print(f"\tHero 3:", hero_moonstart)

        session.refresh(hero_betman)
        session.refresh(hero_superman)
        session.refresh(hero_moonstart)

        print("\tAfter refresh Hero objects")
        print(f"\tHero 1:", hero_betman)
        print(f"\tHero 2:", hero_superman)
        print(f"\tHero 3:", hero_moonstart)

        print("\tBefore refresh Team objects")
        print(f"\tTeam 1:", team_model)
        print(f"\tTeam 2:", team_oracle)

        session.refresh(team_model)
        session.refresh(team_oracle)

        print("\tAfter refresh Team objects")
        print(f"\tTeam 1:", team_model)
        print(f"\tTeam 2:", team_oracle)


def relation_ship_assign():
    with Session(engine) as session:
        team_oracle = session.exec(select(Team).where(col(Team.name) == 'Preventers')).first()

        hero_betman = session.exec(select(Hero).where(col(Hero.name) == 'Betman')).first()
        hero_betman.team = team_oracle
        session.add(hero_betman)
        session.commit()
        session.refresh(hero_betman)
        print(f"\tHero Betman:", hero_betman)


def create_heroes_with_team():
    with Session(engine) as session:
        hero_black_lion = Hero(name='Black Lion', secret_name='Trevor Challa', age=35)
        hero_sure_e = Hero(name='Princess Sure-E', secret_name='Sure-E')
        team_wakaland = Team(name='Wakaland', headquarters='Wakaland Capital City',
                             heroes=[hero_black_lion, hero_sure_e])
        session.add(team_wakaland)
        session.commit()
        session.refresh(team_wakaland)
        print(f"\tTeam 1: ", team_wakaland)

        print(f"\tAfter Refresh hero objects")
        print(f"\tHero 1: ", hero_black_lion)
        print(f"\tHero 2: ", hero_sure_e)

        session.refresh(hero_sure_e)
        session.refresh(hero_black_lion)
        print(f"\tAfter Refresh hero objects")
        print(f"\tHero 1: ", hero_black_lion)
        print(f"\tHero 2: ", hero_sure_e)


def create_heroes_from_team_side():
    with Session(engine) as session:
        team_preventers = session.exec(select(Team).where(Team.name == 'Preventers')).first()

        hero_trantula = Hero(name='Trantula', secret_name='Natalia Roman-on', age=32)
        hero_dr_weird = Hero(name='Dr. Weird', secret_name='Steve Weird', age=36)
        hero_cap = Hero(name='Capitan North America', secret_name='Esteban Rogelios', age=93)

        team_preventers.heroes.append(hero_trantula)
        team_preventers.heroes.append(hero_dr_weird)
        team_preventers.heroes.append(hero_cap)
        session.add(team_preventers)
        session.commit()


def read_relationship():
    with Session(engine) as session:
        statement = select(Hero).where(Hero.name == "Spider-boy")
        result = session.exec(statement)
        hero_spirder_boy = result.one()
        print(f"\tHero:", hero_spirder_boy)

        # 1-usul: Team ni olish
        statement = select(Team).where(Team.id == hero_spirder_boy.team_id)
        result = session.exec(statement)
        team = result.first()
        print(F"\tSpider boy's Team:", team)

        # 2-usul: Team ni olish
        print(f"\tSpider boy's Team:", hero_spirder_boy.team)

        # 3-usul: Heroes ni olish
        statement = select(Team).where(Team.name == 'Preventers')
        result = session.exec(statement)
        another_team = result.first()
        print("\tTeam:", another_team)
        for num, hero in enumerate(another_team.heroes, start=1):
            print(f"\t{num}. Heroe:", hero)


def update_heroes():
    with Session(engine) as session:
        statement = select(Hero).where(Hero.name == 'Trantula')
        result = session.exec(statement)
        hero_spider_boy = result.one()
        hero_spider_boy.team = None
        session.add(hero_spider_boy)
        session.commit()
        session.refresh(hero_spider_boy)
        print("\tHero:", hero_spider_boy)


def delete_team():
    with Session(engine) as session:
        statement = select(Team).where(Team.name == 'Wakaland')
        team = session.exec(statement).one()
        session.delete(team)
        session.commit()
        print(f"\tDelete: ", team)


def select_deleted_heroes():
    with Session(engine) as session:
        statement = select(Hero).where(Hero.name == 'Black Lion')
        result = session.exec(statement)
        hero = result.first()
        print(F"\tBlack Lion not found:", hero)

        statement = select(Hero).where(Hero.name == 'Princess Sure-E')
        result = session.exec(statement)
        hero = result.first()
        print(f"\tPrincess Sure-E not found:", hero)


def main():
    creata_db_or_tabales()
    create_heroes()
    create_with_relation_attr()
    relation_ship_assign()
    create_heroes_with_team()
    create_heroes_from_team_side()
    read_relationship()
    update_heroes()
    # delete_team()
    # select_deleted_heroes()


if __name__ == '__main__':
    main()
