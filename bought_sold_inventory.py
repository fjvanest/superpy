from superpy import *

#  Function that writes bought items to csv

def bought_csv():
    id = args.id
    #product_name = args.product_name
    buy_price = args.buy_price
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


# Function that updates date in .txt file (only works here, not in superpy.py or create_ready.py (?))
from datetime import datetime
def set_new_date():
    snw = args.set_date
    snw_string = str(snw)
    
    try:
        new_date= datetime.strptime(snw_string, "%Y-%m-%d")
        
        str_type = str(type(new_date))
        datetime_type = "<class 'datetime.datetime'>"
        if str_type == datetime_type:
            file = open(path_date, "w") 
            file.write(snw_string) 
            file.close() 
            print(f"Date has been set to {new_date} in set_date.txt")    
        else: print('Datea not correct, use the format yyyy-mm-dd')
        
    except ValueError: print('Date not correct, use the format yyyy-mm-dd')

def show_product():
    #1:Sinas,2:Cola,3:Casis,4:Melk,5:Water,6:Limonade,7:Appelsap,8:Sinasappelsap,9:Perensap,10:Bier

    id = args.id

    if id == 1:
        urllib.request.urlretrieve(
        'https://hollandshopper.nl/2482-large_default/fanta-sinas-zero-fles-500-ml.jpg',
        "sinasafbeelding")
        img = Image.open("sinasafbeelding")
        img.show()

    if id == 2:
        urllib.request.urlretrieve(
        'https://static.ah.nl/dam/product/AHI_43545239393030353033?revLabel=3&rendition=800x800_JPG_Q90&fileType=binary',
        "afbeeldingcola")
        img = Image.open("afbeeldingcola")
        img.show()


    if id == 3:
        urllib.request.urlretrieve(
        'https://goedkoopdrank.nl/image/cache/catalog/Frisdrank/pet%20klein/fanta-cassis-50cl-pet-flesjes-800x800.jpg',
        "afbeeldingcasis")
        img = Image.open("afbeeldingcasis")
        img.show()


    if id == 4:
        urllib.request.urlretrieve(
        'https://www.dekweker.nl/image-service/_jcr_content.product.08712800001157.image/1/large.jpeg',
        "afbeeldingmelk")
        img = Image.open("afbeeldingmelk")
        img.show()


    if id == 5:
        urllib.request.urlretrieve(
        'http://best4office.nl/uploads/products/600x450/051795_p.jpg',
        "afbeeldingwater")
        img = Image.open("afbeeldingwater")
        img.show()


    if id == 6:
        urllib.request.urlretrieve(
        'https://media.s-bol.com/q2vq9W0JGrA2/544x840.jpg',
        "afbeeldinglimonade")
        img = Image.open("afbeeldinglimonade")
        img.show()


    if id == 7:
        urllib.request.urlretrieve(
        'https://cdn.webshopapp.com/shops/299068/files/324930529/1600x2048x2/appelsap-1-ltr.jpg',
        "afbeeldingappelsap")
        img = Image.open("afbeeldingappelsap")
        img.show()


    if id == 8:
        urllib.request.urlretrieve(
        'https://static.ah.nl/dam/product/AHI_43545239383738373030?revLabel=1&rendition=800x800_JPG_Q90&fileType=binary',
        "afbeeldingsinasappelsap")
        img = Image.open("afbeeldingsinasappelsap")
        img.show()


    if id == 9:
        urllib.request.urlretrieve(
        'https://cdn.webshopapp.com/shops/99398/files/46441654/800x600x2/perensap-1l.jpg',
        "afbeeldingperensap")
        img = Image.open("afbeeldingperensap")
        img.show()


    if id == 10:
        urllib.request.urlretrieve(
        'https://cdn11.bigcommerce.com/s-54jmfzthvf/images/stencil/1280w/products/994/2049/8.6_Original_blik_50cl__29869.1671187964.jpg',
        "afbeeldingbier")
        img = Image.open("afbeeldingbier")
        img.show()

    print(f'image for {id} has been opened on your screen')