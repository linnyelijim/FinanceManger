import csv
import gspread
from datetime import datetime
import time

lindsey = ["LJ_capOne_2022.csv", "LJ_capOne_2023.csv"]
jared = ["JH_capOne_2022.csv", "JH_capOne_2023.csv"]
months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
transactions = []

# Changes the date to a month
def switch(date):
    try:
        parsed_date = datetime.strptime(date, '%Y-%m-%d')
        month_number = parsed_date.month
        month = months[month_number - 1]
        return month
    
    except ValueError:
        print("Invalid date format. Please use 'YYYY-MM-DD'.")
        return "undefined"

# Will sort transactions into category groups
def category_sort(transaction):
    category = transaction[2]
    category_lists = {
        "merchandise": [],
        "dining": [],
        "gas/automotive": [],
        "other": [],
        "lodging": [],
        "internet": [],
        "airfare": [],
        "health care": [],
        "entertainment": [],
        "other services": [],
        "payment/credit": []
    }
    category_lower = category.lower()
    if category_lower in category_lists:
        category_lists[category_lower].append(category)
    else:
        print("Invalid category.")
    return category_lists
    
# Opens a .csv file and extracts each transaction
def financeTracker(file):
    sum = 0.0
    with open(file, mode='r') as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            date = row[0]
            month = switch(date)
            name = row[3]
            amount = float(row[5] if row[5] != '' else '-'+ row[6])
            sum += amount if amount > 0 else 0
            category = row[4] 
            transaction = ((month, name, category, amount))
            print(transaction)
            transactions.append(transaction)
        print(sum)
        return transactions

# Connects to a Google Spreadsheet         
def upload(worksheet, file):
    gc = gspread.service_account()
    sh = gc.open("Finances")
    wksh = sh.worksheet(worksheet)
    rows = financeTracker(file)

# Exports each transaction into the spreadsheet
    for row in rows:
        wksh.insert_row([row[0], row[1], row[2], row[3]], 8)
        time.sleep(2)

financeTracker(jared[0])
#upload("Jared_2022", jared[0])
#upload("Jared_2023", jared[1])
#upload("Lindsey_2022", lindsey[0])
#upload("Lindsey_2023", lindsey[1])