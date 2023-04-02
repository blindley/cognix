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

try:
    db_url = os.environ.__getitem__('COGNIXDB')
except KeyError:
    raise ValueError('The COGNIXDB environment variable is not set')

engine = create_engine(db_url)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

def add_card(card_uuid, card_dict):
    errors = []

    if not card_uuid: # Check for None or empty string
        card_uuid = str(uuid.uuid4())

    card_json = json.dumps(card_dict)

    card = session.query(Card).filter(Card.uuid == card_uuid).first()
    if card is None:
        # Create a new card if it doesn't exist
        card = Card(uuid=card_uuid, json=card_json)
        session.add(card)
    else:
        # Update the existing card's JSON data
        card.json = card_json

    # Delete existing fields for the card
    session.query(Field).filter(Field.uuid == card_uuid).delete()

    # Add or update fields for the card
    for key, value in card_dict.items():
        field = Field(uuid=card_uuid, key=key, value=str(value))
        session.add(field)

    session.commit()

    if not errors:
        errors = None
    if errors:
        card_uuid = None
    return {"uuid": card_uuid, "errors": errors }

def delete_cards(card_uuids):
    session.query(Field).filter(Field.uuid.in_(card_uuids)).delete(synchronize_session='fetch')
    session.query(Card).filter(Card.uuid.in_(card_uuids)).delete(synchronize_session='fetch')
    session.commit()

def get_tables():
    metadata = MetaData()
    metadata.reflect(bind=engine)

    tables = {}
    for table_name in metadata.tables:
        table = Table(table_name, metadata, autoload=True, autoload_with=engine)
        keys = table.columns.keys()
        result = session.query(table).all()
        rows = [dict(zip(keys, row)) for row in result]
        tables[table_name] = {'column_names': keys, 'rows': rows}

    return tables


def get_card_by_uuid(card_uuid):
    card = session.query(Card).filter(Card.uuid == card_uuid).one_or_none()
    if card:
        card_dict = json.loads(card.json)
        return card_dict
    else:
        return None

def search_cards(search_dict):
    # Find cards that match the search criteria
    matching_card_uuids = set([card.uuid for card in session.query(Card).all()])
    
    for key, value in search_dict.items():
        uuids_for_key_value = set([field.uuid for field in session.query(Field).filter(Field.key == key, Field.value == value).all()])
        matching_card_uuids.intersection_update(uuids_for_key_value)

    # Retrieve Card objects for the matching UUIDs
    matching_cards = session.query(Card).filter(Card.uuid.in_(matching_card_uuids)).all()
    return matching_cards
