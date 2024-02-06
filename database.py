import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#


#Ucitavanje podataka iz .env fajla (funckija importovana iz dotenv)
load_dotenv()

#Preuzimanje verednosti database_url iz .env fajla preko funkcije os.getenv
DATABASE_URL = os.getenv("DATABASE_URL")

#Pravljenje sqllalchemy engina preko Database_url
engine = create_engine(DATABASE_URL)
#Pravljenje fabrike sesija pomocu funckije sessionamker.Fabrika sesija je odgovorna za stvaranje pojedinacnih sesija baze podataka.U zagradi se prosledjuju komande za ponasanje sesija
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#Pravljenje "base clase"Pravljenjee database modela preko SQLAlcheemy object relational mapping (ORM) aproach
Base = declarative_base()

#Pravljenje database tabele definisanih preko modela
Base.metadata.create_all(bind=engine)

#Pravljenje seije i zatvaranje sesije nakon zavrsetka odredjenee funckije
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
