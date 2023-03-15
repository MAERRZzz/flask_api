from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, VARCHAR, Text, ForeignKey, DateTime, SmallInteger, Boolean, ARRAY
from sqlalchemy.orm import declarative_base
from sqlalchemy.dialects.postgresql import UUID, JSON
from sqlalchemy.orm import sessionmaker
import uuid

import os
# from dotenv import load_dotenv
#
# load_dotenv()

HOST = 'localhost'
USER = 'postgres'
PSW = 'admin'
DB = 'cepu_qr'

# HOST = os.getenv('HOST')
# USER = os.getenv('USER')
# PSW = os.getenv('PSW')
# DB = os.getenv('DB')

db_url = f"postgresql+psycopg2://{USER}:{PSW}@{HOST}/{DB}"
# db_url = f"postgresql//{USER}:{PSW}@{HOST}/{DB}"
db = create_engine(db_url, echo=True)
# db = create_engine(db_url)
base = declarative_base()


class VisitList(base):
    __tablename__ = 'visit_list'

    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('student.id'))
    visit_time = Column(Integer, nullable=False)
    lecture_room = Column(Integer, nullable=False)

    def __init__(self, student_id, visit_time, lecture_room):
        self.student_id = student_id
        self.visit_time = visit_time
        self.lecture_room = lecture_room

    def __repr__(self):
        return f'<Student_ID: "{self.student_id}", Visit_Time: "{self.visit_time}">'


class Student(base):
    __tablename__ = 'student'

    id = Column(Integer, primary_key=True)
    email = Column(Text, nullable=False)
    display_name = Column(Text, nullable=False)
    google_id = Column(Text, nullable=False)
    public_key = Column(Text, nullable=False)
    private_key = Column(Text, nullable=False)

    def __init__(self, email, display_name, google_id, public_key, private_key):
        self.email = email
        self.display_name = display_name
        self.google_id = google_id
        self.public_key = public_key
        self.private_key = private_key

    def __repr__(self):
        return f'<Student "{self.display_name}" Email "{self.email}">'


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
