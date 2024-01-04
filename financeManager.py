import csv
import gspread
from datetime import datetime
import time

lindsey = ["LJ_capOne_2022.csv", "LJ_capOne_2023.csv"]
months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
transactions = []


# Opens a .csv file and extracts each transaction
def financeTracker(file):
    with open(file, mode='r') as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            date = row[0]
            name = row[3]
            amount = float(row[5] if row[5] != '' else '-'+ row[6])
            category = row[4] 
            transaction = ((date, name, category, amount))
            print(transaction)
            transactions.append(transaction)
        return transactions

# Connects to a Google Spreadsheet         
gc = gspread.service_account()
sh = gc.open("Finances")
wksh = sh.worksheet("Lindsey_2022")
rows = financeTracker(lindsey[0])

# Exports each transaction into the spreadsheet
for row in rows:
        wksh.insert_row([row[0], row[1], row[2], row[3]], 8)
        time.sleep(2)