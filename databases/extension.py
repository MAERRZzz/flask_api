from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, VARCHAR, Text, ForeignKey, DateTime, SmallInteger, Boolean
from sqlalchemy.orm import declarative_base
from sqlalchemy.dialects.postgresql import UUID, JSON
from sqlalchemy.orm import sessionmaker
import uuid

import os
from dotenv import load_dotenv

load_dotenv()

HOST = os.getenv('HOST')
USER = os.getenv('USER')
PSW = os.getenv('PSW')
DB = os.getenv('DB')

db_url = f"postgresql+psycopg2://{USER}:{PSW}@{HOST}/{DB}"
db = create_engine(db_url, echo=True)
# db = create_engine(db_url)
base = declarative_base()


class User(base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(Text)
    display_name = Column(Text)
    google_id = Column(Text)
    public_key = Column(Text)
    private_key = Column(Text)

    def __init__(self, email, display_name, google_id, public_key, private_key):
        self.email = email
        self.display_name = display_name
        self.google_id = google_id
        self.public_key = public_key
        self.private_key = private_key

    def __repr__(self):
        return f'<User "{self.email}" - "{self.display_name}">'


class Event(base):
    __tablename__ = 'event'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    location = Column(VARCHAR, nullable=False)
    description = Column(VARCHAR, nullable=False)
    start = Column(Text, nullable=False)
    end = Column(Text, nullable=False)

    summaryId = Column(UUID(as_uuid=True), ForeignKey("class.id"))

    def __repr__(self):
        return f'<Room "{self.location}" Time "{self.start}" - "{self.end}">'


class Class(base):
    __tablename__ = 'class'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(VARCHAR, nullable=False)

    def __repr__(self):
        return f'<Lesson "{self.name}">'


Session = sessionmaker(db)
session = Session()
