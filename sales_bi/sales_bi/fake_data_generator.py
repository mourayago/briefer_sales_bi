import random
from collections import defaultdict
from datetime import datetime, timedelta

from sellers import get_state_sales, set_sellers

# set the sellers list
sellers = set_sellers(5)

# sales range
start_date = datetime.strptime('2023-12-31', '%Y-%m-%d')  # sales start date
end_date = datetime.strptime('2024-10-13', '%Y-%m-%d')  # sales end date
sales_range = abs(end_date - start_date).days  # size of sales data

# creating sales data
sales_data = []
for sales in range(1, sales_range + 1):
    start_date += timedelta(days=1)
    for seller in sellers:
        new_seller = seller.copy()  # making copy of the original dict
        new_seller['state'] = get_state_sales()
        new_seller['sales_date'] = start_date
        new_seller['sales_value'] = random.randint(500, 1000)
        sales_data.append(new_seller)

# creating targets based on sales data


calculated_data = defaultdict(lambda: {'total_sales': 0, 'count': 0})

for entry in sales_data:
    seller_id = entry['seller_id']
    date_ref = entry['sales_date'].replace(day=1)  # target date ref
    calculated_data[(seller_id, date_ref)]['total_sales'] += entry['sales_value']
    calculated_data[(seller_id, date_ref)]['count'] += 1

targets = []
for (seller_id, date_ref), values in calculated_data.items():
    avg_sales = values['total_sales'] / values['count']
    # adding 10% of margin over the average of sales on each month
    target_value = avg_sales * 1.1
    targets.append({
        'seller_id': seller_id,
        'date_ref': date_ref,
        'target_value': round(target_value, 0),
    })
