from superpy import *

def profit_revenue():
    #input by argparse for which start date / end date
    #no input means all items (or from /  till given date)

    #sort all bought items on above info 
    #buy/sell date is entered when buying/selling item so can be read from bought/sold.csv
    #for loop all items
    #compare row with bought date to input dates
    #write bought/sold price to list

    #read bought and sold items
    
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
    print(f'Profit: {profit_rounded}')
    print(f'Based on revenue of: {revenue_rounded}')
    print(f'Based on expenses of: {expenses_rounded}')

