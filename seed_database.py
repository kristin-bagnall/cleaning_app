"""Script to seed database."""

import os
import json
from datetime import datetime

import crud
import model
import server

os.system('dropdb cleaning')
os.system('createdb cleaning')

model.connect_to_db(server.app)
model.db.create_all()

def create_fake_users():
  crud.create_user(1, 'Bob', 'Marley', '1@gmail.com', 'password1', 'customer')
  crud.create_user(2, 'Rita', 'Anderson', '2@gmail.com', 'password2', 'employee')

def create_fake_addresses():
  crud.create_address(1, 1, 'primary residence', '123 Coconut Grove', 'Bend', 'OR', 97702)
  crud.create_address(2, 1, 'vacation', '456 Coconut Grove', 'Bend', 'OR', 97702)
  crud.create_address(3, 2, 'primary', '123 Aloha Drive', 'Bend', 'OR', 97702)

def create_employee_job():
  crud.create_employee_job(2, 1)
  crud.create_employee_job(2, 2)

def create_job():
  crud.create_job(1,1,1,'2021-01-01 12:00:00','2021-01-01 01:00:00')
  crud.create_job(2,1,1,'2021-02-01 12:00:00','2021-02-01 01:00:00')

create_fake_users()
create_fake_addresses()
create_job()
create_employee_job()
