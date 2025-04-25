"""Database configuration and session initializer"""

from sqlmodel import SQLModel, Session, create_engine


# SQLite database file
sqlite_file_name = "Crickter_Tracker.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"


# Required for SQLite with SQLMod
connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)


def create_db_and_tables():
    """Creates database and tables"""
    SQLModel.metadata.create_all(engine)


def get_session():
    """Yields a session to interact with the database"""
    with Session(engine) as session:
        yield session
