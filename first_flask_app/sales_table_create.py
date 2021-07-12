from app import db, Sales
import csv
from datetime import datetime

def parse_to_lists():

	# transaction_date, product, price, payment_type = [], [], [], []
	# transaction_date.append(row['Transaction_date'])
	# product.append(row['Product'])
	# price.append(row['Price'])
	# payment_type.append(row['Payment_Type'])

	sales_records = []
	with open('homework3sales.csv') as file:
		reader = csv.reader(file)
		# reader = csv.DictReader(file, delimiter='\t')
		for i, row in enumerate(reader):
			if i > 0:

				salestring = row[0].split(';')
				salestring[0] = datetime.strptime(salestring[0], '%m/%d/%Y %H:%M')
				salestring[0] = salestring[0].date()
				salestring[2] = int(salestring[2])
				sales_records.append(salestring)

	return sales_records

db.create_all()

sales_records = parse_to_lists()
for r in sales_records:
	sale_record = Sales(Transaction_date=r[0], Product=r[1] ,Price=r[2] ,Payment_Type=r[3])
	db.session.add(sale_record)

db.session.commit()