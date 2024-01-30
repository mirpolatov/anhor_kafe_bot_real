from sqlalchemy import Column, Integer, LargeBinary, String, create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = 'sqlite:///food.db'

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class FoodItem(Base):
    __tablename__ = 'food_item'

    id = Column(Integer, primary_key=True)
    food_picture = Column(LargeBinary)
    food_name = Column(String)

    amount = Column(Integer)


class Salat(Base):
    __tablename__ = 'salat'

    id = Column(Integer, primary_key=True)
    salat_picture = Column(LargeBinary)
    salat_name = Column(String)

    salat_amount = Column(Integer)


class Ichimliklar(Base):
    __tablename__ = 'ichimlik'

    id = Column(Integer, primary_key=True)
    ichimlik_picture = Column(LargeBinary)
    ichimlik_name = Column(String)

    ichimlik_amount = Column(Integer)


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
