from sqlalchemy import Column, DateTime, String, create_engine ,Integer ,Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field
from marshmallow import Schema, fields
from datetime import date

Base = declarative_base()

class UserRequestSchema(Schema):
    
    name = fields.Str()
    Type = fields.Str()
    age = fields.Integer()
    description = fields.Str()
    checked = fields.Boolean()

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True,index=True)
    name = Column(String(100))
    checked = Column(Boolean,default=True)
    Type = Column(String(100))
    date = Column(DateTime())
    age = Column(Integer)
    description = Column(String(100))


class UserSchema(SQLAlchemySchema):
    class Meta:
        model = User
        load_instance = True  

    id = auto_field()
    name = auto_field()
    date = auto_field()
    age = auto_field()
    description = auto_field()
    date = auto_field()
    Type = Column(String(100))

class UserResponseSchema(SQLAlchemySchema):
    class Meta:
        model = User
        load_instance = True  

    id = auto_field()
    name = auto_field()
    date = auto_field()

def init_db(uri):
    engine = create_engine(uri, convert_unicode=True)
    db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
    Base.query = db_session.query_property()
    Base.metadata.create_all(bind=engine)
    return db_session
