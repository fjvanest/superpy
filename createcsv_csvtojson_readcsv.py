from superpy import *

#directory and paths are defined because without these, errors kept occuring
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

#Function to create csv files, if they don't exist, that are needed for this program 
def create_csv_files():
    if not os.path.exists(path_bought):
        with open(path_bought, 'w') as bought_file:
            headers = ['id', 'bought_id', 'product_name', 'buy_price', 'buy_date','expiration_date']
            writer = csv.DictWriter(bought_file, delimiter=',', lineterminator='\n', fieldnames=headers)
            writer.writeheader()
            print("bought.csv has been made in your directory")
            pass
    if not os.path.exists(path_sold):
        with open(path_sold, 'w') as sold_file:
            headers = ['id', 'product_name', 'sell_price', 'sell_date']
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



# Function that converts CSV file to JSON file
def csv_to_json():
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


#Function that makes it possbile to read csv file in code editor
def read_csv(x):
    file = x
    path = os.path.join(parent_dir, directory, file)

    with open(path, newline='') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        print(file)
        for row in csv_reader:
            print(', '.join(row))
    print('\n')

    return
