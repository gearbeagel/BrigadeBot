from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class VoiceMessage(Base):
    __tablename__ = 'voice_messages'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    file_id = Column(String)

engine = create_engine('sqlite:///voice_messages.db')

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()
