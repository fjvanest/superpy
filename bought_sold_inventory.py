from superpy import *

#  Function that writes bought items to csv

def bought_csv():
    id = args.id
    #product_name = args.product_name
    buy_price = args.buy_price
    today = date.today()
    set_date = 0
    set_date = args.set_bought_date
    expiration_date = pd.to_datetime(args.expiration_date).date()
    bought_id = 0

    if set_date is not None: bought_date = set_date
    else: bought_date = today

    product_name = available_products.get(id)
    
    if expiration_date > bought_date:
        with open(path_bought, 'a', newline='') as f:
            writer = csv.writer(f)
            rowcount = 0
            try:
                for row in open(path_bought):
                    rowcount+= 1
                bought_id = rowcount

                row_bought_product = [id, bought_id, product_name, buy_price, bought_date, expiration_date]
                writer.writerow(row_bought_product)
            except csv.Error as e:
                sys.exit('file {}, line {}: {}'.format(path_bought, reader.line_num, e))
        print('Bought product added to bought.csv (and updated to inventory.csv')
    else: 
        print("Product expires today or is already expired. Can not be bought")
    dfbought = pd.read_csv(path_bought)
    print(dfbought)


    with open(path_inventory, newline='') as f:
        reader_i = csv.reader(f)
        next(f)
        inventory_data = list(reader_i)

    if not inventory_data:
        # inventory requires product_id, product_name and amount
        product_id = row_bought_product[0] 
        amount = 1
        inventory_data.append([product_id, product_name, amount])
    
    else:
        # list with all product id's in inventory
        in_inventory = [ele[0] for ele in inventory_data]
        product_id = str(row_bought_product[0])

        # check if new product id is already in inventory
        if product_id in in_inventory:
            for inventory_product in inventory_data:
                product_id = row_bought_product[0]
                item_index_forloop = 0
                inventory_id = inventory_product[item_index_forloop][0]
                int_inventory_id = int(inventory_id)

                if product_id == int_inventory_id:
                    if  int(inventory_product[2]) > 0:
                        # Update amount for product already in inventory
                        amount = int(inventory_product[2])
                        amount += 1
                        inventory_product[2] = amount
                item_index_forloop += 1

        product_id = str(row_bought_product[0])
        if product_id not in in_inventory:
            # Add product to list
            amount = 1
            inventory_data.append([product_id, product_name, amount])
 

    #inventory_data = sorted(inventory_data, key=lambda x: (x[2], x[0], x[1]), reverse=False)
    # #Save data to inventory.csv

    file = open(path_inventory, 'w', newline ='')
    with file:
        headers = ['id', 'product_name', 'amount']
        writer = csv.DictWriter(file, delimiter=',', lineterminator='\n', fieldnames=headers)
        writer.writeheader()   
        write = csv.writer(file)
        write.writerows(inventory_data)

# Function that writes sold items to csv file

def sold_csv():
    # Sold product via argparse
    # Check if product is in stock in inventory.csv
    # Remove from inventory
    # Add sold product to sold.csv

    # id,product_name,sell_price,sell_date

    id = str(args.id)
    product_name = available_products.get(int(id))
    print(product_name)
    sell_price = args.sell_price
    today = date.today()
    set_date = 0
    set_date = args.set_sold_date

    if set_date is not None: sell_date = set_date
    else: sell_date = today

    # Update inventory (remove sold item)
    with open(path_inventory, newline='') as f:
        reader_i = csv.reader(f)
        next(f)
        inventory_data = list(reader_i)

    ids_inventory = [element[0] for element in inventory_data]
    if id in ids_inventory:
        index_id = ids_inventory.index(id)
        amount = int(inventory_data[index_id][2])
        if amount > 0:
            inventory_data[index_id][2] = amount - 1
            
            file = open(path_inventory, 'w', newline ='')
            with file:
                headers = ['id', 'product_name', 'amount']
                writer = csv.DictWriter(file, delimiter=',', lineterminator='\n', fieldnames=headers)
                writer.writeheader()   
                write = csv.writer(file)
                write.writerows(inventory_data)

            with open(path_sold, 'a', newline='') as f:
                    writer = csv.writer(f)
                    try:
                        row = [id, product_name, sell_price, sell_date]
                        writer.writerow(row)
                    except csv.Error as e:
                        sys.exit('file {}, line {}: {}'.format(path_sold, reader.line_num, e))
            print('Sold product added to sold.csv')
            dfsold = pd.read_csv(path_sold)
            print(dfsold)


        else: print('This product is not in stock, can not be sold!')

    else: print('This product is not in stock, can not be sold!')

# Function that displays inventory_csv
def inventory_csv():
    dfinventory = pd.read_csv(path_inventory)
    print(dfinventory)

