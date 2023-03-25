import os
import json
import uuid
from sqlalchemy import (create_engine, Column, String, ForeignKey, TEXT,
    UniqueConstraint, MetaData, Table)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()

class Card(Base):
    __tablename__ = 'card'
    uuid = Column(String, primary_key=True)
    json = Column(TEXT)

    fields = relationship("Field", back_populates="card")

class Field(Base):
    __tablename__ = 'field'
    uuid = Column(String, ForeignKey('card.uuid'), primary_key=True)
    key = Column(String(32), primary_key=True)
    value = Column(TEXT)

    card = relationship("Card", back_populates="fields")

    __table_args__ = (UniqueConstraint('uuid', 'key', name='uix_uuid_key'),)

db_url = os.environ.get('COGNIXDB', 'sqlite:///../cognix.db')
engine = create_engine(db_url)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

def add_card(card_uuid, card_dict):

    if card_uuid is None:
        card_uuid = str(uuid.uuid4())

    card_json = json.dumps(card_dict)
    card = Card(uuid=card_uuid, json=card_json)
    session.add(card)

    for key, value in card_dict.items():
        field = Field(uuid=card_uuid, key=key, value=str(value))
        session.add(field)

    session.commit()

def get_tables():
    metadata = MetaData()
    metadata.reflect(bind=engine)

    tables = {}
    for table_name in metadata.tables:
        table = Table(table_name, metadata, autoload=True, autoload_with=engine)
        result = session.query(table).all()
        keys = table.columns.keys()
        rows = [dict(zip(keys, row)) for row in result]
        tables[table_name] = rows

    return tables
