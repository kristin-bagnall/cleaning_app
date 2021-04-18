"""Models for cleaning app."""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class User(db.Model):
    """A user."""

    __tablename__ = "user"

    user_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True, 
                        unique=True)
    name = db.Column(db.Text,
                    nullable=False)  
    email = db.Column(db.Text, 
                     unique=True,
                     nullable=False)
    password = db.Column(db.Text, 
                        nullable=False)
    role = db.Column(db.Text,
                      nullable=False)  

    def __repr__(self):
        return f'<User user_id={self.user_id} email={self.email}>'


class Address(db.Model):
    """An address."""

    __tablename__ = "address"

    address_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True, 
                        unique=True)
    customer_id = db.Column(db.Integer,
                          db.ForeignKey('user.user_id'),
                          nullable=False,)
    type = db.Column(db.Text,
                      nullable=False,)
    street_address_1 = db.Column(db.Text,
                      nullable=False,)
    street_address_2 = db.Column(db.Text,
                      )
    city = db.Column(db.Text,
                      nullable=False,)
    state = db.Column(db.Text,
                      nullable=False,)
    zip_code = db.Column(db.Integer,
                      nullable=False,)

    user = db.relationship('User', backref='address') 

    def __repr__(self):
        return f'<Address address_id={self.address_id} street_address={self.street_address_1}>'

class Job(db.Model):
    """A job."""
    
    __tablename__ = "job"

    job_id = db.Column(db.Integer,
                      autoincrement=True,
                      primary_key=True,
                      unique=True,)

    
    employee_id = db.Column(db.Integer,
                            db.ForeignKey('user.user_id'),
                            nullable=False)
    customer_id = db.Column(db.Integer,
                            db.ForeignKey('user.user_id'),
                            nullable=False)
    address_id = db.Column(db.Integer,
                            db.ForeignKey('user.user_id'),
                            nullable=False)
    start_time = db.Column(db.datetime,)

    end_time = db.Column(db.datetime,)

    payment_method = db.Column(db.Text,)

    is_paid = db.Column(db.Boolean,)

    employee = db.relationship('User', backref='jobs')
    customer = db.relationship('User', backref='jobs')
    address = db.relationship('Address', backref='jobs')

    def __repr__(self):
      return f'<Job job_id={self.job_id} customer={self.customer_id} employee={self.employee_id}>'


def connect_to_db(flask_app, db_uri='postgresql:///cleaning', echo=True):
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    flask_app.config['SQLALCHEMY_ECHO'] = echo
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.app = flask_app
    db.init_app(flask_app)

    print('Connected to the db!')


if __name__ == '__main__':
    from server import app

    connect_to_db(app)



""" To implement in the future:
- Invoices
- Job's FK relationship to Invoices

- Images
- Job's FK relationship to Images

- Reviews?
- Job's FK relationship
- User's FK relationship
""""