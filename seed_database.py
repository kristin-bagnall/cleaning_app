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
  crud.create_user(1, 'Bob', 'Marley', 'test100', 'test100', 'customer')
  crud.create_user(2, 'Rita', 'Anderson', 'test101', 'password101', 'customer')

  crud.create_user(3, 'Damien', 'Marley', 'test200', 'password200', 'employee')
  crud.create_user(4, 'Makeda', 'Jahnesta', 'test201', 'password201', 'employee')
  crud.create_user(5, 'Ziggy', 'Marley', 'test202', 'password202', 'employee')

def create_fake_addresses():
  crud.create_address(1, 1, 'primary residence', '123 Coconut Grove', 'Bend', 'OR', 97702)
  crud.create_address(2, 1, 'vacation', '456 Coconut Grove', 'Bend', 'OR', 97702)
  crud.create_address(3, 2, 'primary', '123 Aloha Drive', 'Bend', 'OR', 97702)

def create_employee_job():
  crud.create_employee_job(3, 1)
  crud.create_employee_job(4, 1)
  crud.create_employee_job(5, 1)
  crud.create_employee_job(3, 2)
  crud.create_employee_job(3, 3)
  crud.create_employee_job(5, 4)
  crud.create_employee_job(4, 4)

def create_job():
  crud.create_job(1,1,1,'2021-07-01 12:00:00','2021-07-01 01:00:00','Standard Clean', 100)
  crud.create_job(2,1,1,'2021-08-01 12:00:00','2021-08-01 01:00:00','Standard Clean', 100)
  crud.create_job(3,1,2,'2021-07-15 12:00:00','2021-07-15 01:00:00','Vacation Home Clean', 200)

  crud.create_job(4,2,3,'2021-07-12 2:30:00','2021-07-12 5:00:00','Standard Clean', 150)
  crud.create_job(5,2,3,'2021-07-18 2:30:00','2021-07-18 5:00:00','Standard Clean', 150)


create_fake_users()
create_fake_addresses()
create_job()
create_employee_job()
crud.create_invoices()
