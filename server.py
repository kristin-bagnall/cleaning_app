from flask import Flask, render_template, request, make_response, redirect, session, flash, send_file, jsonify
import crud
from model import connect_to_db
from secrets import flask_secret_key, GOOGLE_API_KEY, ClOUDINARY_API_KEY, ClOUDINARY_API_SECRET, CLOUDINARY_CLOUD_NAME
from datetime import datetime
import requests
from math import cos, asin, sqrt, pi
import cloudinary.uploader


app = Flask(__name__)
app.secret_key = flask_secret_key

@app.route('/')
def hompage():
  """Returns rendered homepage """
  return render_template('index.html');

@app.route('/login')
def login():
  """Returns rendered login page"""

  if 'user' in session.keys():
    return redirect('/customer')

  return render_template('login.html');


@app.route('/handle-login', methods=['POST'])
def handle_login():
  """Check accuracy of log in information and redirect accordingly """
  
  email = request.form['email']
  password = request.form['password']

  user = crud.get_user_by_email(email)

  if crud.is_correct_password(email, password):
    if not user:
      return redirect('/')

    session['user'] = user.user_id

    if user.role == 'employee':
      session['role'] = 'employee'
      return redirect('/employee')

    if user.role == 'customer':
      session['role'] = 'customer'
      return redirect('/customer')

    else:
      flash('Database error: Incorrect role type. Please reach out to support.','warning')


  else:
    flash("You entered the wrong password.  Please try again", "danger")
    return redirect("/")

@app.route('/create_account')
def create_account():
  return render_template('create_account.html')

@app.route('/create_user', methods=['POST'])
def create_user():
  first_name = request.form['first_name']
  last_name = request.form['last_name']
  email = request.form['email']
  password = request.form['password']

  if crud.get_user_by_email(email):
    flash('Looks like you already have an account. Please login here.','warning')
    return redirect('/login')
  
  crud.create_user(first_name=first_name, last_name=last_name, email=email, password=password, role='customer')
  
  user = crud.get_user_by_email(email)
  session['user'] = user.user_id
  session['role'] = 'customer'

  flash('Account successfully created','success')
  return redirect('/customer')


@app.route('/customer')
def customer_login():

  if 'role' not in session.keys():
    return redirect('/')
  elif session['role'] == 'employee':
    return redirect('/employee')
    
  user_id = session['user']
  user = crud.get_user_by_id(user_id)

  date_now = datetime.now()
  
  return render_template('customer.html', user=user, date_now=date_now)


@app.route('/post-form-data', methods=['POST'])
def cloudinary_upload():

  user_id = session.get('user')

  if not user_id:
    return redirect('/')

  job_id = request.form['job_id']

  image = request.files['customer-image']
  
  result = cloudinary.uploader.upload(file=image,
                                      api_key=ClOUDINARY_API_KEY,
                                      api_secret=ClOUDINARY_API_SECRET,
                                      cloud_name=CLOUDINARY_CLOUD_NAME)

  crud.create_image(job_id=job_id, user_id=user_id, image_url=result['secure_url'], uploaded_at=datetime.now())

  return redirect('/customer')


@app.route('/request_clean')
def request_clean():
  """ Renders clean request template """
  if 'user' not in session.keys():
    flash('Please log in to request clean','info')
    return redirect('/login')
  
  user = crud.get_user_by_id(session['user'])

  return render_template('request_clean.html', user=user)


@app.route('/create_clean', methods=['POST'])
def create_clean():
  """Creates clean job with pending status and redirects customer to portal"""
  
  address_id = request.form['address_id']

  if not address_id:
    flash('You must select an address.','danger')
    return redirect('/request_clean')

  customer_id = session.get('user')
  
  start_time = request.form['start_time']

  crud.create_job(customer_id, address_id, start_time, end_time=None, amount=0, status='Pending')

  flash('Thank you for your request. We will respond soon.','success')
  return redirect('/customer')


@app.route('/create_address')
def create_address():
  """ Renders create address template """
  user = crud.get_user_by_id(session['user'])

  return render_template('create_address.html', user=user)


@app.route('/add_address', methods=['POST','GET'])
def add_address():
  """Checks to see if an address is in a served area and returns appropriate response """
  customer_id = session.get('user')
  address_type = request.form['address-type']
  address = request.form['address']
  city = request.form['city']
  state = request.form['state']
  zip_code = request.form['zip-code']
  
  # get lng/lat coordinates of address to compare to Bend lng/lat
  params = {"key": GOOGLE_API_KEY, 
          "address": f"{address} {city}, {state} {zip_code}"}

  response = requests.get('https://maps.googleapis.com/maps/api/geocode/json', params)

  if not response.json()['results']:
    flash('Address is not valid. Please enter a new address.','danger')
    return redirect('/create_address')

  request_lng = response.json()['results'][0]['geometry']['location']['lng']
  request_lat = response.json()['results'][0]['geometry']['location']['lat']

  def distance_from_bend_center(lat1, lon1, lat2=44.0581728, lon2=-121.3153096):
      p = pi/180
      a = 0.5 - cos((lat2-lat1)*p)/2 + cos(lat1*p) * cos(lat2*p) * (1-cos((lon2-lon1)*p))/2
      return 12742 * asin(sqrt(a)) #2*R*asin...

  distance = distance_from_bend_center(request_lat, request_lng)

  if distance < 50:
    crud.create_address(customer_id, address_type, address, city, state, zip_code)
    flash('Address has been successfully added.','success')
    return redirect('/request_clean')

  else:
    flash('Address is not currently in our service area. Please enter a new address.', 'danger')
    return redirect('/create_address')

@app.route('/employee')
def employee_login():

  if session['role'] != 'employee':
    return redirect('/')

  user = crud.get_user_by_id(session['user'])

  pending_jobs = crud.get_all_pending_jobs()
  
  date_now = datetime.now()
  
  return render_template('employee.html', user=user, date_now=date_now, pending_jobs=pending_jobs)


@app.route('/download/<invoice_id>')
def download_invoice(invoice_id):
  
  user_id = session.get('user')

  if not user_id:
    return redirect('/')
  
  crud.generate_invoices()
  
  return send_file(f'invoices/{user_id}/{invoice_id}.pdf')


@app.route('/job_status', methods=['POST'])
def update_job_status():

  user_id = session.get('user')
  job_id = request.form['job_id']
  status = request.form['status']

  crud.update_job_status(job_id, status)
  crud.update_job_estimate(job_id)

  if status == 'Confirmed':
    crud.create_employee_job(user_id,job_id)
    crud.generate_invoices()
    flash('Job has been confirmed.', 'info')
  elif status == 'Denied':
    flash('Job has been denied.', 'info')

  return redirect('/employee')


@app.route('/logout')
def logout_user():
    session.clear()

    return redirect('/')


@app.route('/create_rating', methods=['POST'])
def create_rating():
  customer_id = session.get('user')
  job_id = request.form['job_id']
  star_rating = request.form['star_rating']
  review_text = request.form['review_text']

  crud.create_review(job_id, customer_id, star_rating, review_text)

  flash('Thank you for your review! We value your feedback.', 'success')
  return redirect('/customer')

if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)