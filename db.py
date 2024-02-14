from sqlalchemy import Column, Integer, LargeBinary, String, create_engine, DateTime, func
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "postgresql://postgres:1@localhost:5432/menu"

engine = create_engine(DATABASE_URL)
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class Menu(Base):
    __tablename__ = 'menu_taom'

    id = Column(Integer, primary_key=True)
    name = Column(String(300))
    callback_data = Column(String(300))
    price = Column(String(300))
    food_id = Column(Integer, nullable=True)
    # datetime_add = Column(DateTime, default=func.now(), nullable=True)


class MainMenu(Base):
    __tablename__ = 'main_menu'

    id = Column(Integer, primary_key=True)
    name = Column(String(300))
    food_picture = Column(LargeBinary, nullable=True)
    price = Column(String(300))


Base.metadata.create_all(engine)
