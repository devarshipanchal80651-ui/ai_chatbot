from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import pymysql

pymysql.install_as_MySQLdb()

DATABASE_URL = "mysql+mysqldb://root:root@localhost/ai_chatbot"

engine = create_engine(
    DATABASE_URL,
    connect_args={"charset": "utf8mb4"}
)

SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()