import os
from sqlalchemy import create_engine, MetaData, Table, Column, ForeignKey, Integer, String, insert

DB_LOGIN = os.getenv("DB_LOGIN")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_IP = os.getenv("DB_IP")
DB_PORT = os.getenv("DB_PORT")
DB_BASE = os.getenv("DB_BASE")

meta_data = MetaData()

# engine = create_engine(f"postgresql+psycopg2://m1tr:39742Arte@192.168.0.246:5432/timtable_db")
engine = create_engine(f"postgresql+psycopg2://{DB_LOGIN}:{DB_PASSWORD}@{DB_IP}:{DB_PORT}/{DB_BASE}")

users = Table('users', meta_data,
              Column('user_id', Integer(), primary_key=True),
              Column('nickname', String(), nullable=False)
              )

selected_student = Table('selected_student', meta_data,
                         Column('id', Integer(), primary_key=True),
                         Column('user_id', Integer(), ForeignKey('users.user_id')),
                         Column('faculty', Integer(), nullable=False),
                         Column('course', Integer(), nullable=False),
                         Column('group', Integer(), nullable=False)
                         )

selected_teacher = Table('selected_teacher', meta_data,
                         Column('id', Integer(), primary_key=True),
                         Column('user_id', Integer(), ForeignKey('users.user_id')),
                         Column('faculty', Integer(), nullable=False),
                         Column('chair', Integer(), nullable=False),
                         Column('teacher_id', Integer(), nullable=False)
                         )

meta_data.create_all(engine)

