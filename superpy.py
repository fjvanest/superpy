# Imports
import argparse
import csv
import os
import sys
import datetime
from datetime import date
from datetime import datetime as dt
import json
import pandas as pd
from bought_sold_inventory import *
from createcsv_csvtojson_readcsv import *


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

# Get the date today, yesterday, tomorrow
today = datetime.datetime.today().strftime("%Y-%m-%d")
yesterday = (datetime.datetime.today() - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
tomorrow = (datetime.datetime.today() + datetime.timedelta(days=1)).strftime("%Y-%m-%d")

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
#buy.add_argument('-id', type=int, metavar='', required=True, help='insert bought item id here')  
#buy.add_argument('-n', '--product_name', type=str, metavar='', required=True, help='insert bought item product_name here')  
buy.add_argument('-bp', '--buy_price', type=float, metavar='', required=True, help='insert item price here (x.xx')  
buy.add_argument('-ed', '--expiration_date', type=datetime.date.fromisoformat, metavar='', required=True, help='insert expiration date here (yyyy-mm-dd)')  
buy.add_argument('-sbd', '--set_bought_date', type=datetime.date.fromisoformat, metavar='', required=False, help='if bought date is not today, insert date here (yyyy-mm-dd)')  

#fromisoformat() = The date string in ISO format – yyyy-mm-dd

#Parser for selling items
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

csvtojson = subparsers.add_parser('json', help='csv to json convert')
csvtojson.add_argument('-json', '--csvtojson', metavar='', required=True, type=str, help='insert file name to convert (bought, sold, inventory, expired (without extension)')

profitrevenue = subparsers.add_parser('profitrevenue', help='see profit and revenue, can be specified for certain time frame')
#profitrevenue.add_argument('-pr', '--profit_revenue', required=True, action='store_true',help='See profit and revenue for the store') 
profitrevenue.add_argument('-start', '--set_start_date', type=datetime.date.fromisoformat, metavar='', required=False, help='Set start date, default is first sold item(yyyy-mm-dd)')  
profitrevenue.add_argument('-stop', '--set_stop_date', type=datetime.date.fromisoformat, metavar='', required=False, help='Set stop date, default is last sold item(yyyy-mm-dd)')  

args = parser.parse_args()

if __name__ == "__main__":
    # print("This program is operated by command lines using argpar\n")
    # to start type: python superpy\superpy.py --help 

    #creates necessary csv files, if they already exist then program continues
    create_csv_files()

    if args.task == 'buy':
        bought_csv()

    if args.task == 'sell':
        sold_csv()

    if args.task == 'inventory':
        inventory_csv()

    if args.task == 'json':
        csv_to_json()
        
    if args.task == 'profitrevenue':
        profit_revenue()


