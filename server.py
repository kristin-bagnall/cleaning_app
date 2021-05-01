from flask import Flask, render_template, request, make_response, redirect, session, flash
import crud
from model import connect_to_db

app = Flask(__name__)

#To-do, create a secret.ssh file to save this info and do not check that into version control 
app.secret_key = 'my_temporary_secret_key'

@app.route('/')
def hompage():
  """Returns rendered homepage """
  return render_template('homepage.html');


@app.route('/handle-login', methods=['POST'])
def handle_login():
  """Check accuracy of log in information and redirect accordingly """

  email = request.form['email']
  password = request.form['password']

  user = crud.get_user_by_email(email)

  if crud.is_correct_password(email, password):
    session['user'] = user.user_id

    print(user)
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

@app.route('/customer')
def customer_login():
  if session['role'] != 'customer':
    return redirct('/')
  user = crud.get_user_by_id(session['user'])
  
  return render_template('customer.html', user=user)


@app.route('/employee')
def employee_login():

  if session['role'] != 'employee':
    return redirect('/')

  user = crud.get_user_by_id(session['user'])

  return render_template('employee.html', user=user)


if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)