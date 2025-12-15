from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


# TODO: utilizar variável de ambiente ou arquivo .env
# Não é a forma correta de fazer
DATABASE_URL = "mysql+pymysql://root:admin@127.0.0.1:3306/mercado"

engine = create_engine(url=DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# py -m venv env
# env\Scripts\activate

# pip install -r requirements.txt
# pip install SQLAlchemy
# pip freeze > requirements.txt