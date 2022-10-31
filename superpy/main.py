# Imports
import argparse
import csv
from itertools import count
import os
from re import A
import sys
import datetime
from operator import itemgetter
from xmlrpc.client import INVALID_ENCODING_CHAR
import json



# Do not change these lines.
__winc_id__ = "a2bc36ea784242e4989deb157d527ba0"
__human_name__ = "superpy"


''' MAIN GOAL - build a command-line tool that a supermarket will use to keep track of their inventory. '''

#1 Which products the supermarket offers;
#2 How many of each type of product the supermarket holds currently;
#3 How much each product was bought for, and what its expiry date is;
#4 How much each product was sold for or if it expired, the fact that it did;
'''
1. bought and sales files (make if dont excist)
    add items to bought list
2. read files and import 
3. Make an inventory
    remove items (sell) from inventory
4. Show inventory to user 
5. Add or remove bought/sold items from inventory 


Filename	Columns
bought.csv	id,product_name,buy_price,expiration_date
sold.csv	id,sell_price
'''
# Your code below this line.
def main():
    pass

# Get the date today, yesterday, tomorrow
today = datetime.datetime.today().strftime("%Y-%m-%d")
set_day = today
yesterday = (datetime.datetime.today() - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
tomorrow = (datetime.datetime.today() + datetime.timedelta(days=1)).strftime("%Y-%m-%d")

parser = argparse.ArgumentParser(
    prog= 'superpy', 
    description='Inventory system supermarket',
    formatter_class=argparse.ArgumentDefaultsHelpFormatter,)
subparsers = parser.add_subparsers(dest='task')

#Parser for buying items
# bought.csv	id,product_name,buy_price,expiration_date
buy = subparsers.add_parser('buy', help='register bought items')
buy.add_argument('-id', type=int, metavar='', required=True, help='insert bought item id here')  
buy.add_argument('-n', '--product_name', type=str, metavar='', required=True, help='insert bought item product_name here')  
buy.add_argument('-bp', '--buy_price', type=float, metavar='', required=True, help='insert item price here')  
buy.add_argument('-ed', '--expiration_date', type=datetime.date.fromisoformat, metavar='', required=True, help='insert expiration date here (yyyy-mm-dd)')  
#fromisoformat() = The date string in ISO format – yyyy-mm-dd

#Parser for selling items
#sold.csv	id,sell_price
sell = subparsers.add_parser('sell', help='register sold item')
sell.add_argument('-id', type=int, metavar='', required=True, help='insert sold item id here') 
sell.add_argument('-bi', '--bought_id', type=int, metavar='', help='insert sold item bought id here') 
sell.add_argument('-sp', '--sell_price', type=float, metavar='', required=True, help='insert sold item price here')   

inventory = subparsers.add_parser('inventory', help='inventory items in stock')
inventory.add_argument('--inventory', metavar='', required=True, help='see inventory') 

expiration_check = subparsers.add_parser('expiration', help='check if products are expired')
expiration_check.add_argument('--expiration', metavar='', required=True, help='check if products are expired') 

csvtojson = subparsers.add_parser('json', help='csv to json convert')
csvtojson.add_argument('-json', '--csvtojson', metavar='', required=True, type=str, help='insert file name to convert (bought, sold, inventory, expired')

args = parser.parse_args()

#function to change the day used for the report
def change_day(n_days): #n days from today (positive is future, negative is past)
    if args.task == 'change_day':
        days_from_now = (datetime.datetime.today() + 
                        datetime.timedelta(days=n_days)).strftime("%Y-%m-%d")
        set_day = days_from_now
        return set_day

#Function to create csv files, if they don't exist, that are needed for this program 
def create_csv_files():
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
    
    if not os.path.exists(path_bought):
        with open(path_bought, 'a') as bought_file:
            headers = ['id', 'bought_id', 'product_name', 'buy_price', 'bought_date','expiration_date']
            writer = csv.DictWriter(bought_file, delimiter=',', lineterminator='\n', fieldnames=headers)
            writer.writeheader()
            print("bought.csv has been made in your directory")
            pass
    if not os.path.exists(path_sold):
        with open(path_sold, 'a') as sold_file:
            headers = ['id', 'bought_id', 'sell_price']
            writer = csv.DictWriter(sold_file, delimiter=',', lineterminator='\n', fieldnames=headers)
            writer.writeheader()
            print("sold.csv has been made in your directory")
            pass
    if not os.path.exists(path_inventory):
        with open(path_inventory, 'w') as inventory_file:
            headers = ['id', 'product_name', 'amount']
            writer = csv.DictWriter(inventory_file, delimiter=',', lineterminator='\n', fieldnames=headers)
            writer.writeheader()
            print("inventory.csv has been made in your directory")
            pass
    if not os.path.exists(path_expired):
        with open(path_expired, 'w') as expired_file:
            headers = ['id', 'product_name', 'amount']
            writer = csv.DictWriter(expired_file, delimiter=',', lineterminator='\n', fieldnames=headers)
            writer.writeheader()
            print("expired.csv has been made in your directory")
            pass
    return


def read_csv(x):
    file = x
    directory = 'superpy'
    parent_dir = os.getcwd()
    path = os.path.join(parent_dir, directory, file)

    with open(path, newline='') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        print(file)
        for row in csv_reader:
            print(', '.join(row))
    print('\n')

    return

# Function that writes bought items to csv
def bought_csv():
    if args.task == 'buy':
        directory = 'superpy'
        parent_dir = os.getcwd()
        path_b_name = 'bought.csv'
        path_bought = os.path.join(parent_dir, directory, path_b_name)

        id = args.id
        product_name = args.product_name
        buy_price = args.buy_price
        bought_date = set_day
        expiration_date = args.expiration_date
        bought_id = 0
        
        with open(path_bought, 'a', newline='') as f:
            writer = csv.writer(f)
            rowcount = 0
            try:
                for row in open(path_bought):
                    rowcount+= 1
                bought_id = rowcount

                row = [id, bought_id, product_name, buy_price, bought_date, expiration_date]
                writer.writerow(row)
            except csv.Error as e:
                sys.exit('file {}, line {}: {}'.format(path_bought, reader.line_num, e))
        print('Bought product added to bought.csv')
    return

# Function that writes sold items to csv
def sold_csv():
    if args.task == 'sell':
        directory = 'superpy'
        parent_dir = os.getcwd()
        path_s_name = 'sold.csv'
        path_sold = os.path.join(parent_dir, directory, path_s_name)

        id = args.id
        bought_id = args.bought_id
        sell_price = args.sell_price
        
        with open(path_sold, 'a', newline='') as f:
            writer = csv.writer(f)
            try:
                row = [id,bought_id,sell_price]
                writer.writerow(row)
            except csv.Error as e:
                sys.exit('file {}, line {}: {}'.format(path_sold, reader.line_num, e))
        print('Sold product added to sold.csv')
    return

# Function that creates inventory_csv
def inventory_csv():
    if args.task == 'inventory':
        directory = 'superpy'
        parent_dir = os.getcwd()
        path_b_name = 'bought.csv'
        path_bought = os.path.join(parent_dir, directory, path_b_name)
        path_s_name = 'sold.csv'
        path_sold = os.path.join(parent_dir, directory, path_s_name)
        path_i_name = 'inventory.csv'
        path_inventory = os.path.join(parent_dir, directory, path_i_name)

        with open(path_bought, newline='') as f:
            reader_b = csv.reader(f)
            next(f)
            bought_data = list(reader_b)

        with open(path_sold, newline='') as g:
            reader_s = csv.reader(g)
            next(g)
            sold_data = list(reader_s)

        # bought items list -> set for all unique products
        item_list = []
        for x in bought_data:
            item_list.append(x[2])
        #item_set = set(item_list) --> backupplan, not included in final code

        # Compare lists (bought vs sold) based on bought_ID 
        bid_bought = [b[1] for b in bought_data]
        bid_sold = [s[1] for s in sold_data]

        #difference between two lists (bought vs sold -> what is in stock based on bought_id)
        bid_stock = (list(set(bid_bought) ^ set(bid_sold)))

        bid_stock_len = len(bid_stock)
        inventory_list = []

        for x in range(bid_stock_len):
            bid_index = bid_bought.index(bid_stock[x])
            inventory_list.append(bought_data[bid_index])

        #sort inventory list (by id, bought_date, bought_id)
        inventory_list = sorted(inventory_list, key=lambda x: (x[0], x[4], x[1]), reverse=False)

        #make inventory list with needed values [id, product_name]
        inventory_list_filtered = []

        for x in inventory_list:
            inventory_list_filtered.append(x[0:3])

        #remove bought_id from inventory list
        for x in range(len(inventory_list_filtered)):
            del inventory_list_filtered[x][1]
        
        # Amount (count amount of each product in list)
        inventory_list_filtered2 = []
        for products in inventory_list_filtered:
                if products not in inventory_list_filtered2:
                    item = products[1]
                    amount = sum(x.count(item) for x in inventory_list_filtered)
                    products.append(amount)
                    inventory_list_filtered2.append(products)

        # Only unique values
        inventory_list_final = []
        for x in inventory_list_filtered2:
            if x not in inventory_list_final:
                inventory_list_final.append(x)

        #Save data to inventory.csv
        data = inventory_list_final
        
        file = open(path_inventory, 'w', newline ='')
        with file:
            headers = ['id', 'product_name', 'amount']
            writer = csv.DictWriter(file, delimiter=',', lineterminator='\n', fieldnames=headers)
            writer.writeheader()   
            write = csv.writer(file)
            write.writerows(data)
        print('Inventory updated to inventory.csv')
    return
  

# Function for revenue
def revenue():
    if args.task == 'revenue':
    #read bought and sold items
        directory = 'superpy'
        parent_dir = os.getcwd()
        path_b_name = 'bought.csv'
        path_bought = os.path.join(parent_dir, directory, path_b_name)
        path_s_name = 'sold.csv'
        path_sold = os.path.join(parent_dir, directory, path_s_name)

        with open(path_bought, newline='') as f:
            reader_b = csv.reader(f)
            next(f)
            bought_data = list(reader_b)

        # list with bought_id's
        bought_id_list = []
        for x in bought_data:
            bought_id_list.append(x[1])
    
        with open(path_sold, newline='') as g:
            reader_s = csv.reader(g)
            next(g)
            sold_data = list(reader_s)

        # list with sold id's
        sold_id_list = []
        for x in sold_data:
            sold_id_list.append(x[1])

        profit_total = 0
        for sid in sold_id_list:
            if sid in bought_id_list:
                # minus 1 since id's start at one but list starts counting at 0
                b = int(sid) - 1
                bprice = float(bought_data[b][3])
                
                sid_len = len(sold_id_list)
                s = 0
                while sid_len > s:
                    if sold_data[s][1] == sid:
                        sprice = float(sold_data[s][2])
                    s += 1

                profit = sprice - bprice
                
                profit_total = profit_total + profit
                profit_total_r = "{:.2f}".format(profit_total)
        print('Total profit is:', profit_total_r)
    return    



# Function that checks for expired products and removes them from inventory_csv
def expiration_check():
    if args.task == 'expire':
    #read bought and sold items
        directory = 'superpy'
        parent_dir = os.getcwd()
        path_b_name = 'bought.csv'
        path_bought = os.path.join(parent_dir, directory, path_b_name)
        path_s_name = 'sold.csv'
        path_sold = os.path.join(parent_dir, directory, path_s_name)

        with open(path_bought, newline='') as f:
            reader_b = csv.reader(f)
            next(f)
            bought_data = list(reader_b)

        with open(path_sold, newline='') as g:
            reader_s = csv.reader(g)
            next(g)
            sold_data = list(reader_s)

        # list with all bought_ids in sold_items list
        sold_data_bid = []
        sold_data_len = len(sold_data)

        for sold_items in range(sold_data_len):
            sid_index = sold_data.index(sold_data[sold_items])
            sold_data_bid.append(sold_data[sid_index][1])
    
        #read expiration date and compare with current day
        bought_len = len(bought_data)
        counter = 0
        expired_data = []
        
        while bought_len > counter:
            for each in bought_data:
                expiration_date = bought_data[counter][5]
                if expiration_date < set_day:
                    if bought_data[counter][1] not in sold_data_bid:
                        # write expired item to sold.csv (for revenue calculation)
                        with open(path_sold, 'a', newline='') as f:
                            writer = csv.writer(f)
                            row = []
                            expired_id = bought_data[counter][0]
                            expired_boughtid = bought_data[counter][1]
                            expired_product_name = bought_data[counter][2]
                            expired_sellprice = 0
                            row = [expired_id, expired_boughtid, expired_sellprice]
                            writer.writerow(row)
                            expired_data.append([expired_id, expired_product_name])
                            print('Expired product added to sold.csv with sold price 0')
                counter += 1
        
        directory = 'superpy'
        parent_dir = os.getcwd()
        path_e_name = 'expired.csv'
        path_expired = os.path.join(parent_dir, directory, path_e_name)
        with open(path_expired, newline='') as e:
                reader_e = csv.reader(e)
                next(e)
                expired_file_data = list(reader_e)

        with open(path_expired, 'r') as expired_f:
            expired_file = csv.reader(expired_f)
            expired_list = list(expired_file)

        if expired_list == []:
            pass
        elif expired_list[0] == ['id', 'product_name', 'amount']:
            expired_list.pop(0)
            pass
        else:
            # # flatten nested list
            # for item in expired_file_data:
            #    expired_data.append(item)
            expired_data.append(expired_file_data)
    
        expired_list_new = []

        for product in expired_data:
            if product not in expired_list:
                    item = product[1]
                    amount = sum(x.count(item) for x in expired_data)
                    product.append(amount)  
                    expired_list_new.append(product)

        unique_expired = []

        for x in expired_list_new:
            if x not in unique_expired:
                unique_expired.append(x)

        # write expired item(s) to expired.csv 
        expired_file = open(path_expired, 'a')
        with expired_file as ae:
            writer = csv.writer(ae)
            writer.writerows(unique_expired)
            print('Expired product(s) updated to expired.csv')   

        return

# Function that converts Python CSV to JSON
def csv_to_json():
    if args.task == 'json':
        directory = 'superpy'
        parent_dir = os.getcwd()
        file_name = args.csvtojson
        path = os.path.join(parent_dir, directory, file_name)

        csv_file_path = path + '.csv'
        json_file_path = path + '.json' 

        json_array = []
        
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
        print(f'json file made for {file_name}')

# Function that checks if a product is out of stock / almost out of stock
def outofstock():
    #decided to skip this because excerise has taken more time than planned
    return



if __name__ == "__main__":
    main()

# print("This program is operated by command lines using argpar\n")
# type: python superpy\main.py --help

#read_csv("bought.csv")
#read_csv("sold.csv")
#read_csv("inventory.csv")

create_csv_files()
bought_csv()
sold_csv()
inventory_csv()
revenue()
expiration_check()
csv_to_json()

