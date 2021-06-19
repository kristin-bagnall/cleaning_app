"""Models for cleaning app."""

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref
from datetime import datetime

db = SQLAlchemy()


class User(db.Model):
    """A user."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True, 
                        unique=True)
    first_name = db.Column(db.Text,
                    nullable=False)  
    last_name = db.Column(db.Text,
                    nullable=False)  
    email = db.Column(db.Text, 
                        unique=True,
                        nullable=False)
    password = db.Column(db.Text, 
                        nullable=False)
    role = db.Column(db.Text,
                        nullable=False)  
    customer_jobs = db.relationship('Job', order_by='Job.start_time')
    

    def __repr__(self):
        return f'<User user_id={self.user_id} email={self.email}>'


class Address(db.Model):
    """An address."""

    __tablename__ = "addresses"

    address_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True, 
                        unique=True)
    customer_id = db.Column(db.Integer,
                            db.ForeignKey('users.user_id'),
                            nullable=False,)
    address_type = db.Column(db.Text,
                        nullable=False,)
    street = db.Column(db.Text,
                        nullable=False,)
    city = db.Column(db.Text,
                        nullable=False,)
    state = db.Column(db.Text,
                        nullable=False,)
    zip_code = db.Column(db.Integer,
                        nullable=False,)

    customer = db.relationship('User', backref='address') 

    def __repr__(self):
        return f'<Address address_id={self.address_id} street_address={self.street}>'

class Job(db.Model):
    """A job."""
    
    __tablename__ = "jobs"

    job_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True,
                        unique=True,)

    customer_id = db.Column(db.Integer,
                            db.ForeignKey('users.user_id'),
                            nullable=False)
    address_id = db.Column(db.Integer,
                            db.ForeignKey('addresses.address_id'),
                            nullable=False)
    start_time = db.Column(db.DateTime,)

    end_time = db.Column(db.DateTime,)

    amount = db.Column(db.Integer)

    status = db.Column(db.Text)

    customer = db.relationship('User', foreign_keys=[customer_id])

    employees = db.relationship('User', 
                                secondary="employees_jobs", 
                                backref=backref('jobs',order_by="Job.start_time"))

    address = db.relationship('Address', backref='employee_jobs')

    def __repr__(self):
      return f'<Job job_id={self.job_id} customer={self.customer_id} start_time={self.start_time}>'

class EmployeeJob(db.Model):
    """ An employee <> Job association table"""

    __tablename__ = "employees_jobs"

    employee_id = db.Column(db.Integer,
                            db.ForeignKey('users.user_id'),
                            primary_key=True,
                            nullable=False)
    
    job_id = db.Column(db.Integer,
                            db.ForeignKey('jobs.job_id'),
                            primary_key=True,
                            nullable=False)


    def __repr__(self):
        return f'<Job Employee Association job_id={self.job_id} Employee={self.employee_id}'

class Image(db.Model):
    """An Image."""

    __tablename__ = "images"

    image_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True,
                        unique=True,)
    job_id = db.Column(db.Integer,
                        db.ForeignKey('jobs.job_id'),
                        nullable=False)
    user_id = db.Column(db.Integer,
                            db.ForeignKey('users.user_id'),
                            nullable=False)
    image_url = db.Column(db.Text,
                            nullable=False)
    uploaded_at = db.Column(db.DateTime,
                            nullable=False)

    creator = db.relationship('User', backref='images')
    job = db.relationship('Job', backref='images')

    def __repr__(self):
        return f'<Image image_id={self.image_id} job_id={self.job_id}>'

class Invoice(db.Model):
    """An invoice"""

    __tablename__ = "invoices"

    invoice_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True,
                        unique=True,)
    
    job_id = db.Column(db.Integer,
                        db.ForeignKey('jobs.job_id'),
                        nullable=False)
    
    payment_method = db.Column(db.Text,)

    is_paid = db.Column(db.Boolean,)
    
    job = db.relationship('Job', backref='invoices')

    def __repr__(self):
        return f'<Invoice invoice_id={self.invoice_id} job_id={self.job_id}>'

class Review(db.Model):
    """A review"""

    __tablename__ = "reviews"

    review_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True,
                        unique=True,)
    job_id = db.Column(db.Integer,
                        db.ForeignKey('jobs.job_id'),
                        nullable=False)
    customer_id = db.Column(db.Integer,
                            db.ForeignKey('users.user_id'),
                            nullable=False)
    star_rating = db.Column(db.Integer,
                            nullable=False,)
    review_text = db.Column(db.Text,)

    job = db.relationship('Job', backref='reviews')
    customer = db.relationship('User', backref='reviews')


    def __repr__(self):
        return f'<Review review_id={self.review_id} job_id={self.job_id} customer_id={self.customer_id}>'



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