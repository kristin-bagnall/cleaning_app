from flask import Flask, render_template, request, make_response, redirect, session, flash, send_file
import crud
from model import connect_to_db
import os
from secrets import flask_secret_key
import invoice_generator
from datetime import datetime

app = Flask(__name__)
app.secret_key = flask_secret_key

@app.route('/')
def hompage():
  """Returns rendered homepage """
  return render_template('index.html');

@app.route('/login')
def login():
  """Returns rendered login page"""

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
      flash('Database error: Incorrect role type. Please reach out to support.')


  else:
    flash("You entered the wrong password.  Please try again")
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
  
  crud.create_user(user_id=405, first_name=first_name, last_name=last_name, email=email, password=password, role='customer')
  
  user = crud.get_user_by_email(email)
  session['user'] = user.user_id
  session['role'] = 'customer'

  return redirect('/customer')


@app.route('/customer')
def customer_login():

  if session['role'] != 'customer':
    return redirct('/')
  user = crud.get_user_by_id(session['user'])

  date_now = datetime.now()
  
  return render_template('customer.html', user=user, date_now=date_now)


@app.route('/employee')
def employee_login():

  if session['role'] != 'employee':
    return redirect('/')

  user = crud.get_user_by_id(session['user'])

  return render_template('employee.html', user=user)


@app.route('/download/<invoice_id>')
def download_invoice(invoice_id):
  
  user_id = session.get('user')

  if not user_id:
    return redirect('/')

  user = crud.get_user_by_id(user_id)
  
  crud.generate_invoices()
  
  return send_file(f'invoices/{user_id}/{invoice_id}.pdf')

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

  return redirect('/customer')

if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)