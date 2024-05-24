from sqlalchemy import Integer, Column, String, DateTime, Float, create_engine, ForeignKey
from sqlalchemy.orm import relationship, declarative_base
import datetime
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

Base = declarative_base()

class Item(Base):
    __tablename__ = 'item'
    id = Column(Integer, primary_key=True)
    item_name = Column(String)
    item_quantity = Column(Float)
    item_quantity_units = Column(String)
    item_discount = Column(Float)
    item_price = Column(Float)
    cart_id = Column(Integer, ForeignKey('cart.id'))
    created_ts = Column(DateTime, default=datetime.datetime.utcnow)

    def __init__(self, item_name, item_quantity, item_quantity_units, item_discount, item_price, cart_id=None):
        self.item_name = item_name
        self.item_quantity = item_quantity
        self.item_quantity_units = item_quantity_units
        self.item_discount = item_discount
        self.item_price = item_price
        self.cart_id = cart_id


class Cart(Base):
    __tablename__ = 'cart'
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    store_name = Column(String)
    currency = Column(String)
    purchase_total = Column(Float)
    purchase_total_tax = Column(Float)
    identifier = Column(String)
    filename = Column(String)
    created_ts = Column(DateTime, default=datetime.datetime.utcnow)
    items = relationship("Item")

    def __init__(self, store_name, currency, purchase_total, purchase_total_tax, identifier, filename):
        self.store_name = store_name
        self.currency = currency
        self.purchase_total = purchase_total
        self.purchase_total_tax = purchase_total_tax
        self.identifier = identifier
        self.filename = filename


if __name__ == "__main__":
    # connect to the database
    db_name = config.get('DATABASE', 'Name')

    # connect to the database
    engine = create_engine(f"sqlite:///{db_name}")
    Base.metadata.create_all(engine)
