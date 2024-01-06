import csv
import gspread
from datetime import datetime
import time

files = {
    "lj" : ["LJ_capOne_2022.csv", "LJ_capOne_2023.csv"],
    "jh" : ["JH_capOne_2022.csv", "JH_capOne_2023.csv"]
}
sheets = {
    "lj" : ["Lindsey_2022", "Lindsey_2023"],
    "jh" : ["Jared_2022", "Jared_2023"]
}
months = ["January", "February", "March", "April", "May", 
          "June", "July", "August", "September", "October", 
          "November", "December"
]
categories = {
        "merchandise": [],
        "dining": [],
        "gas/automotive": [],
        "other": [],
        "lodging": [],
        "internet": [],
        "airfare": [],
        "health care": [],
        "entertainment": [],
        "payment/credit": []
}

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

# Will be used to sort by category
def category_sort(transaction):
    category = transaction[2]
    category_lower = category.lower()
    if category_lower == "other services":
        category_lower = "other"
    if category_lower in categories:
        categories[category_lower].append(category)
    else:
        print("Invalid category.")

    return categories

# Opens a .csv file and extracts each transaction
def financeTracker(file):
    sum = total_sum = 0.0
    transactions = []

    with open(file, mode='r') as csv_file:
        csv_reader = csv.reader(csv_file)

        for row in csv_reader:
            date = row[0]
            month = switch(date)
            name = row[3]
            amount = float(row[5] if row[5] != '' else '-'+ row[6])
            sum += amount if amount > 0 else 0
            total_sum = round(sum, 2)
            category = row[4] 
            transaction = ((month, name, category, amount))
            transactions.append(transaction)

        return transactions
        
# Connects to a Google Spreadsheet and inserts transactions       
def upload(worksheet, file):
    gc = gspread.service_account()
    sh = gc.open("Finances")
    wksh = sh.worksheet(worksheet)
    rows = financeTracker(file)

    for row in rows:
        wksh.insert_row([row[0], row[1], row[2], row[3]], 3)
        # Used to space out uploads per Google Sheets requirements
        time.sleep(2) 

# Uploads each file to its associated sheet
def run():
    for key in set(sheets.keys()).union(files.keys()):
        for i in range(2):
            upload(sheets[key][i], files[key][i])

# Call to run the program
run()