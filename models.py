import os
from sqlalchemy import Column, String, Integer, create_engine
from flask_sqlalchemy import SQLAlchemy
import json

database_path = os.environ["DATABASE_URL"]
if database_path.startswith("postgres://"):
    database_path = database_path.replace("postgres://", "postgresql://", 1)

db = SQLAlchemy()

"""
setup_db(app)
    binds a flask application and a SQLAlchemy service
"""


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


def db_drop_and_create_all():
    db.drop_all()
    db.create_all()


"""
Customer
Have title and release year
"""


class Customer(db.Model):
    id = Column(db.Integer, primary_key=True)
    name = Column(String)
    address = Column(String)
    orders = db.relationship(
        "Order", lazy="select", backref=db.backref("customer", lazy="joined")
    )

    def __init__(self, name, address=""):
        self.name = name
        self.address = address

    """
  insert()
      inserts a new model into a database
      the model must have a unique name
      the model must have a unique id or null id
  """

    def insert(self):
        db.session.add(self)
        db.session.commit()

    """
  delete()
      deletes a new model into a database
      the model must exist in the database
  """

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    """
  update()
      updates a new model into a database
      the model must exist in the database
  """

    def update(self):
        db.session.commit()

    def format(self):
        return {"id": self.id, "name": self.name, "address": self.address}


"""
Waiter
Have title and release year
"""


class Waiter(db.Model):
    id = Column(db.Integer, primary_key=True)
    name = Column(String)
    address = Column(String)
    orders = db.relationship(
        "Order", lazy="select", backref=db.backref("waiter", lazy="joined")
    )

    def __init__(self, name, address=""):
        self.name = name
        self.address = address

    """
  insert()
      inserts a new model into a database
      the model must have a unique name
      the model must have a unique id or null id
  """

    def insert(self):
        db.session.add(self)
        db.session.commit()

    """
  delete()
      deletes a new model into a database
      the model must exist in the database
  """

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    """
  update()
      updates a new model into a database
      the model must exist in the database
  """

    def update(self):
        db.session.commit()

    def format(self):
        return {"id": self.id, "name": self.name, "address": self.address}


order_detail = db.Table(
    "order_detail",
    db.Column("order_id", db.Integer, db.ForeignKey("order.id"), primary_key=True),
    db.Column("drink_id", db.Integer, db.ForeignKey("drink.id"), primary_key=True),
)


class Drink(db.Model):
    # Autoincrementing, unique primary key
    id = Column(db.Integer, primary_key=True)
    # String Title
    title = Column(String(80), unique=True)
    # the ingredients blob - this stores a lazy json blob
    # the required datatype is [{'color': string, 'name':string, 'parts':number}]
    recipe = Column(String(180), nullable=False)

    """
    long()
        long form representation of the Drink model
    """

    def get(self):
        return {"id": self.id, "title": self.title, "recipe": json.loads(self.recipe)}

    """
    insert()
        inserts a new model into a database
        the model must have a unique name
        the model must have a unique id or null id
        EXAMPLE
            drink = Drink(title=req_title, recipe=req_recipe)
            drink.insert()
    """

    def insert(self):
        db.session.add(self)
        db.session.commit()

    """
    delete()
        deletes a new model into a database
        the model must exist in the database
    """

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    """
    update()
        updates a new model into a database
        the model must exist in the database
    """

    def update(self):
        db.session.commit()

    def __repr__(self):
        return json.dumps(self.short())


class Order(db.Model):
    # Autoincrementing, unique primary key
    id = Column(db.Integer, primary_key=True)
    # Customer ID
    customer_id = Column(db.Integer, db.ForeignKey("customer.id"), nullable=False)
    # Waiter ID
    waiter_id = Column(db.Integer, db.ForeignKey("waiter.id"), nullable=False)
    drinks = db.relationship(
        "Drink",
        secondary=order_detail,
        lazy="subquery",
        backref=db.backref("orders", lazy=True),
    )

    """
    insert()
        inserts a new model into a database
        the model must have a unique name
        the model must have a unique id or null id
    """

    def insert(self):
        db.session.add(self)
        db.session.commit()

    """
    delete()
        deletes a new model into a database
        the model must exist in the database
    """

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    """
    update()
        updates a new model into a database
        the model must exist in the database
    """

    def update(self):
        db.session.commit()

    def format(self):
        return {
            "id": self.id,
            "customer_id": self.customer_id,
            "waiter_id": self.waiter_id,
        }
