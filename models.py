from flask import app
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class NewPerson(db.Model):
  __tablename__ = 'person_list'
  id = db.Column(db.Integer, primary_key=True)
  password = db.Column(db.String(64))
  userid = db.Column(db.String(32))
  username = db.Column(db.String(8))

import psycopg2
from psycopg2 import pool
import csv 

def postgre():
  connection = psycopg2.connect(
  host="castor.db.elephantsql.com",
  database="ksscqlnz",
  user="ksscqlnz",
  password="b60wugaYTpdHgnMDucQAENPIFSkMLncg")

  cur = connection.cursor()
  return connection, cur
