from sql_config import Config

from flask import Flask, render_template, url_for, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from sqlalchemy import or_

import os
from math import sqrt
from statistics import mean
from faker import Faker
import csv
import requests


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

class Customers(db.Model):
	# __tablename__ = 'customers'
    id = db.Column(db.Integer, primary_key=True)
    FirstName = db.Column(db.String(64), unique=False)
    LastName = db.Column(db.String(64), unique=False)
    Email = db.Column(db.String(64), unique=False)
    
    def __repr__(self):
    	return '<Customers %r>' % self.FirstName

class Sales(db.Model):
	# __tablename__ = 'sales'
    id = db.Column(db.Integer, primary_key=True)
    Transaction_date = db.Column(db.Date)
    Product = db.Column(db.String(64), unique=False)
    Price = db.Column(db.Integer)
    Payment_Type = db.Column(db.String(64), unique=False)

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/numbers/', defaults={'number': 4})
@app.route('/numbers/<int:number>')
def square_root(number):
	return str(sqrt(number))

@app.route('/names/')
def unique_names_query_repr():
	query = db.session.query(Customers.FirstName.distinct().label("FirstName"))
	firstnames = [row.FirstName for row in query.all()]
	return str(len(firstnames))
	#return type(Customers.query.all())

@app.route('/requirements/')
def requirements_view_function():
	os.system("pip freeze > requirements.txt")
	"""
	with open('requirements.txt', 'r') as file:
		requirements = file.read()
	
	return requirements
	"""
	requirements = dict()

	with open('requirements.txt', 'r') as file:
		for line in file.read().split():
			b = line.split('==')
			temp_line = dict([(b[0], b[1])])
			requirements.update(temp_line)

	return render_template('requirements.html', requirements=requirements.items())

@app.route('/generate-users/', defaults={'number': 100})
@app.route('/generate-users/<int:number>')
def fake_users(number):
	fake = Faker()
	fake_users = dict()
	for i in range(number):
		temp_line = dict([(fake.name(), fake.email())])
		fake_users.update(temp_line)
	return render_template('generate-users.html', fake_users=fake_users.items())

@app.route('/mean/')
def mean_height_and_weight():
	height, weight = [], []
	with open('hw.csv') as file:
		reader = csv.DictReader(file)

		for row in reader:
			height.append(float(row[' "Height(Inches)"'])), weight.append(float(row[' "Weight(Pounds)"']))
		
	return f'{mean(height) * 2.54} ????, {mean(weight) / 2.205} ????'

@app.route('/space/')
def astronauts():
	url = 'http://api.open-notify.org/astros.json'
	response = requests.get(url)
	return f"For now it's {response.json().get('number')} astronauts at the Earth's orbit"
	# return f"For now it's {len(response.json().get('people'))} astronauts at the Earth's orbit"

@app.route('/summary/')
def summary():

	query = db.session.query(Sales.Transaction_date.label("Transaction_date"),
							func.sum(Sales.Price).label("Summary")).group_by(Sales.Transaction_date).all()
	summary = {i[0].isoformat():i[1] for i in query}

	# return str(query)

	return render_template('summary.html', summary=summary.items())

@app.route('/sales')
def sales():
	product = request.args.get('product')
	payment_type = request.args.get('payment_type')

	query = Sales.query
	if product:
		query = query.filter(Sales.Product == product)
	if payment_type:
		query = query.filter(Sales.Payment_Type == payment_type)

	rows = query.all()
	headings = ['Transaction date', 'Product', 'Price', 'Payment type']
	sales = [(row.Transaction_date.isoformat(), row.Product, row.Price, row.Payment_Type) for row in rows]
	sales.sort(key = lambda x:x[0])

	return render_template('sales.html', sales=sales, headings=headings, product=product, payment_type=payment_type, lenght=len(sales))

