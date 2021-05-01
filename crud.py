"""CRUD operations."""

from model import db, User, Address, Job, Image, Invoice, Review, EmployeeJob, connect_to_db

# User functions
def create_user(user_id, first_name, last_name, email, password, role):
  """Create and return a new user"""

  user = User(user_id=user_id, 
              first_name=first_name, 
              last_name=last_name, 
              email=email, 
              password=password, 
              role=role
              )

  db.session.add(user)
  db.session.commit()

  return user


def get_user_by_email(email):
  """ Takes an email, and returns the user record.  If email doesn't exist, returns empty list. """

  return User.query.filter(User.email==email).first()
  
def get_user_by_id(user_id):
  """ Takes a user ID, returns the user record. """

  return User.query.get(user_id)

def is_correct_password(email, password):
  """ Takes an email and password. Returns true if password correct. Returns false if password is incorrect."""

  User = get_user_by_email(email)

  if User is None:
    return False
  
  return User.password == password
  
# Address functions
def create_address(address_id, customer_id, address_type, street, city, state, zip_code):
  """Create and return a new address"""

  address = Address(address_id=address_id, 
                    customer_id=customer_id, 
                    address_type=address_type, 
                    street=street, 
                    city=city, 
                    state=state, 
                    zip_code=zip_code
                    )

  db.session.add(address)
  db.session.commit()

  return address

def create_job(job_id, customer_id, address_id, start_time, end_time):
  """Create and return a new job"""

  job = Job(job_id=job_id, 
            customer_id=customer_id,
            address_id=address_id, 
            start_time=start_time, 
            end_time=end_time
            )

  db.session.add(job)
  db.session.commit()

  return job

def create_employee_job(employee_id, job_id):
  """Create and return a new employee job relationship"""

  employee_job = EmployeeJob(employee_id=employee_id,
                              job_id=job_id
                              )

  db.session.add(employee_job)
  db.session.commit()

  return employee_job
  
def create_image(image_id, job_id, creator_id, uploaded_at):
  """Create and return a new image"""

  image = Image(image_id=image_id, 
                job_id=job_id, 
                creator_id=creator_id, 
                uploaded_at=uploaded_at
                )

  db.session.add(image)
  db.session.commit()

  return image

def create_invoice(invoice_id, job_id, payment_method, is_paid):
  """Create and return a new invoice"""

  invoice = Invoice(invoice_id=invoice_id, 
                    job_id=job_id, 
                    payment_method=payment_method, 
                    is_paid=is_paid
                    )

  db.session.add(invoice)
  db.session.commit()

  return invoice

def create_review(review_id, job_id, customer_id, star_rating, review_text):
  """Create and return a new review"""

  review = Review(review_id=review_id, 
                  job_id=job_id, 
                  customer_id=customer_id, 
                  star_rating=star_rating, 
                  review_text=review_text
                  )

  db.session.add(review)
  db.session.commit()

  return review


if __name__ == '__main__':
    from server import app
    connect_to_db(app)