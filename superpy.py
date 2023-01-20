# Imports
import argparse
import csv
import os
import sys
from matplotlib import pyplot as plt
import datetime
from datetime import date
from datetime import datetime as dt
import json
import urllib.request
from PIL import Image
import pandas as pd
from bought_sold_inventory import *
from create_read import *
from profit_revenue import *





# Do not change these lines.
__winc_id__ = "a2bc36ea784242e4989deb157d527ba0"
__human_name__ = "superpy"


''' MAIN GOAL - this superpy file is a command-line tool for a supermarket to keep track of their inventory. '''
# The program has the following uses:

# Show which products the supermarket offers and how many of each type of product the supermarket holds currently (inventory);
# How much each product was bought for, and what its expiry date is;
# How much each product was sold for or if it expired, the fact that it did;
'''
How to use: type the next line in the terminal:
py ./superpy/superpy.py -h
    You will then see a help screen with the features of this program
    Select one of the features, for example: py .\superpy\superpy.py buy -h
'''
# Code below this line.

available_products = {1:'Sinas',2:'Cola',3:'Casis',4:'Melk',5:'Water',6:'Limonade',7:'Appelsap',8:'Sinasappelsap',9:'Perensap',10:'Bier'}

directory = 'superpy'
parent_dir = os.getcwd()
path_b_name = 'bought.csv'
path_bought = os.path.join(parent_dir, directory, path_b_name)
path_s_name = 'sold.csv'
path_sold = os.path.join(parent_dir, directory, path_s_name)
path_i_name = 'inventory.csv'
path_inventory = os.path.join(parent_dir, directory, path_i_name)
path_e_name = 'expired.csv'
path_expired = os.path.join(parent_dir, directory, path_e_name)

parser = argparse.ArgumentParser(
    prog= 'superpy', 
    description='Inventory system supermarket. Buy and sell products. See the inventory. Do expiration check and more.',
    formatter_class=argparse.ArgumentDefaultsHelpFormatter,)

subparsers = parser.add_subparsers(dest='task')

#Parser for buying items
# bought.csv	id,product_name,buy_price,expiration_date
buy = subparsers.add_parser('buy', help='register bought items, based on product id, productname, buy price and expiration date.')
buy.add_argument('-id', required=True,
                choices=[1,2,3,4,5,6,7,8,9,10], 
                type=int, metavar='', 
                help='insert bought item id here (# only). Available products are 1:Sinas,2:Cola,3:Casis,4:Melk,5:Water,6:Limonade,7:Appelsap,8:Sinasappelsap,9:Perensap,10:Bier')
buy.add_argument('-bp', '--buy_price', type=float, metavar='', required=True, help='insert item price here (x.xx')  
buy.add_argument('-ed', '--expiration_date', type=datetime.date.fromisoformat, metavar='', required=True, help='insert expiration date here (yyyy-mm-dd)')  
buy.add_argument('-sbd', '--set_bought_date', type=datetime.date.fromisoformat, metavar='', required=False, help='if bought date is not today, insert date here (yyyy-mm-dd)')  
#fromisoformat() = The date string in ISO format – yyyy-mm-dd


#sold.csv	id,sell_price
sell = subparsers.add_parser('sell', help='register sold item based on product id, bought id and sell price')
sell.add_argument('-id', required=True,
                choices=[1,2,3,4,5,6,7,8,9,10], 
                type=int, metavar='', 
                help='insert solditem id here (# only). Available products to sell are 1:Sinas,2:Cola,3:Casis,4:Melk,5:Water,6:Limonade,7:Appelsap,8:Sinasappelsap,9:Perensap,10:Bier / unless sold out, see inventory')
sell.add_argument('-sp', '--sell_price', type=float, metavar='', required=True, help='insert sold item price here (x.xx)')   
sell.add_argument('-ssd', '--set_sold_date', type=datetime.date.fromisoformat, metavar='', required=False, help='if sell date is not today, insert date here (yyyy-mm-dd)')  

inventory = subparsers.add_parser('inventory', help='see inventory with items in stock')
#inventory.add_argument('--inventory', metavar='', required=True, help='see inventory') 

csvjson = subparsers.add_parser("csvjson", help="csvjson convert, insert file name to convert (don't include .csv extension)")
csvjson.add_argument('-csvjson', '--csvjson', metavar='', required=True, type=str, help='csvjson insert file name to convert (bought, sold, inventory, expired (without extension)')

profitrevenue = subparsers.add_parser('profitrevenue', help='see profit and revenue, can be specified for certain time frame')
profitrevenue.add_argument('-start', '--set_start_date', type=datetime.date.fromisoformat, metavar='', required=False, help='Set start date, default is first sold item(yyyy-mm-dd)')  
profitrevenue.add_argument('-stop', '--set_stop_date', type=datetime.date.fromisoformat, metavar='', required=False, help='Set stop date, default is last sold item(yyyy-mm-dd)')  

set_date = subparsers.add_parser('set_date', help='set standard date for this program (yyyy-mm-dd).')
set_date.add_argument('-sd', '--set_date', type=datetime.date.fromisoformat, metavar='', required=True, help='insert date here (yyyy-mm-dd)')  

showproductps = subparsers.add_parser('showproduct', help='register sold item based on product id, bought id and sell price')
showproductps.add_argument('-id', required=True,
                choices=[1,2,3,4,5,6,7,8,9,10], 
                type=int, metavar='', 
                help='insert item id here (# only) to see picture of said product. Available products to sell are 1:Sinas,2:Cola,3:Casis,4:Melk,5:Water,6:Limonade,7:Appelsap,8:Sinasappelsap,9:Perensap,10:Bier')

args = parser.parse_args()


# Function that converts CSV file to JSON file

'''
    I HAVE NO IDEA HOW BUT ERROR MESSAGE BELOW KEEPS POPPING UP WHEN THIS FUNCTION IS IN ANOTHER FILE (create_ready.py) AND IMPORTED
                 NameError: name 'args' is not defined
    HENCE I HAVE PLACED IT IN THE MAIN FILE BECAUSE IT ONLY WORKS THIS WAY AND I CANT FIGURE OUT HOW TO FIX IT
    HOPE FOR YOUR UNDERSTANDMENT OR BETTER, YOUR IMPUT ON HOW TO FIX THIS

'''
def csvtojson():
    file_to_convert = args.csvjson
    path = os.path.join(parent_dir, directory, file_to_convert)

    csv_file_path = path + '.csv'
    json_file_path = path + '.json' 

    json_array = []
    
    try:
        #read csv file
        with open(csv_file_path, encoding='utf-8') as csvf: 
            #load csv file data using csv library's dictionary reader
            csvReader = csv.DictReader(csvf) 

            #convert each csv row into python dict
            for row in csvReader: 
                #add this python dict to json array
                json_array.append(row)
        
        #convert python jsonArray to JSON String and write to file
        with open(json_file_path, 'w', encoding='utf-8') as jsonf: 
            json_string = json.dumps(json_array, indent=4)
            jsonf.write(json_string)
        print(f'json file made for {file_to_convert}.csv')
    except FileNotFoundError: print('No csv file found with this name.')



'''
    FOR THIS PART OF MY CODE BELOW AN ERROR MESSAGE ALSO KEEPS POPPING UP WHEN THIS FUNCTION IS IN ANOTHER FILE (profit_revenue.py) AND IMPORTED
                 NameError: name 'profit_revenue' is not defined. Did you mean: 'profitrevenue'?
    HENCE I HAVE PLACED IT IN THE MAIN FILE BECAUSE IT ONLY WORKS THIS WAY AND I CANT FIGURE OUT HOW TO FIX IT
    HOPE FOR YOUR UNDERSTANDMENT OR BETTER, YOUR IMPUT ON HOW TO FIX THIS

'''

def profit_revenue():
  
    with open(path_bought, newline='') as f:
        reader_b = csv.reader(f)
        next(f)
        bought_data = list(reader_b)

    with open(path_sold, newline='') as g:
        reader_s = csv.reader(g)
        next(g)
        sold_data = list(reader_s)

    start_date = args.set_start_date
    stop_date = args.set_stop_date
    bought_items_prices = []
    if start_date is None: 
        min_date = '2000-01-01'
        start_date = dt.strptime(min_date, "%Y-%m-%d")           
    else: start_date = dt.strptime(start_date, "%Y-%m-%d")
        
    if stop_date is None:
        max_date = '9999-01-01'
        stop_date = dt.strptime(max_date, "%Y-%m-%d")       
    else: stop_date = dt.strptime(stop_date, "%Y-%m-%d")


    for each_product_b in bought_data:
        buy_date = each_product_b[4]
        buy_date =dt.strptime(buy_date, "%Y-%m-%d")

        if (buy_date >= start_date) & (buy_date <= stop_date):
            bought_price_item = each_product_b[3]
            bought_items_prices.append(bought_price_item)
    
    expenses = float(0)
    for each in range(0, len(bought_items_prices)):
        expenses = expenses + float(bought_items_prices[each])


    sold_items_prices = []

    for each_product_s in sold_data:
        sell_date = each_product_s[3]
        sell_date =dt.strptime(sell_date, "%Y-%m-%d")	
        
        if (sell_date >= start_date) & (sell_date <= stop_date):
            sold_price_item = each_product_s[2]
            sold_items_prices.append(sold_price_item)

    revenue = float(0)
    for each in range(0, len(sold_items_prices)):
        revenue = revenue + float(sold_items_prices[each])

    profit = revenue - expenses
    date_first_item = bought_data[0][4]
    date_today = date.today()

    if (start_date in locals()) & (stop_date in locals()):
        print(f'Figures below calculated between {start_date} and {stop_date}')
    if (start_date in locals()) & (stop_date not in locals()):
        print(f'Figures below calculated between {start_date} and {date_today}')
    if (start_date not in locals()) & (stop_date in locals()):
        print(f'Figures below calculated between {date_first_item} and {stop_date}')
    if (start_date not in locals()) & (stop_date not in locals()):
        print(f'Figures below calculated between {date_first_item} and {date_today}')

    profit_rounded = "{:.2f}".format(profit)
    revenue_rounded = "{:.2f}".format(revenue)
    expenses_rounded = "{:.2f}".format(expenses)
    print(f'Profit during this period was: €{profit_rounded}')
    print(f'Based on revenue of: €{revenue_rounded}')
    print(f'Based on expenses of: €{expenses_rounded}')

    #input a matplotlib function that displays this on a graph of some sort
    fig, ax = plt.subplots()
    
    horizontaal = ['profit', 'revenue', 'expenses'] 
    counts = [profit_rounded, revenue_rounded, expenses_rounded]
    bar_labels = ['profit', 'revenue', 'expenses']
    bar_colors = ['tab:blue', 'tab:green', 'tab:red']

    ax.bar(horizontaal, counts, label=bar_labels, color=bar_colors, align ='center', alpha=0.5)
    ax.set_ylabel('Amount')
    ax.set_title('Visualisation revenue')
    ax.legend(title='Chart')

    plt.show()
        

if __name__ == "__main__":
    # print("This program is operated by command lines using argpar\n")
    # to start type: python superpy\superpy.py --help 

    # creates necessary csv files, if they already exist then program continues
    create_csv_files()

    # set today if not set with function below
    today = date.today()
    # get date to use with superpy (set by user)
    if os.path.exists(path_date):
        get_date()
        today = datetime.datetime.today().strftime("%Y-%m-%d")
        print(f"Current date is set to {get_date()}\tToday's actual date is {today}\n\t\tIf you want to change this, adjust with argparse command set_date\n")

    if args.task == 'set_date':
        set_new_date()

    if args.task == 'buy':
        bought_csv()

    if args.task == 'sell':
        sold_csv()

    if args.task == 'inventory':
        inventory_csv()

    if args.task == 'csvjson':
        csvtojson()
        
    if args.task == 'profitrevenue':
        profit_revenue()

    if args.task == 'showproduct':
        show_product()