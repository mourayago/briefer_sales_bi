import os
import random
from collections import defaultdict
from datetime import datetime, timedelta

from dotenv import load_dotenv
from schemas import Sales, Targets
from sellers import get_state_sales, set_sellers
from sqlalchemy import create_engine, insert
from sqlalchemy.orm import Session, sessionmaker

load_dotenv()

host = os.getenv('RENDER_HOST')
user = os.getenv('RENDER_USER')
pswd = os.getenv('RENDER_PASSWORD')
database = os.getenv('RENDER_DATABASE')

engine = create_engine(f'postgresql+psycopg2://{user}:{pswd}@{host}/{database}', echo=True)

Session = sessionmaker(bind=engine)


class SalesDataGenerator:
    """
    Class to generate sales and target data for a specified number of sellers.
    """

    def __init__(self, num_sellers, start_date='2024-01-01', end_date='2024-10-31'):
        """
        Initialize the generator with a specified number of sellers and sales date range.
        :param num_sellers: Number of sellers to generate data for
        :param start_date: Start date for sales data (format: 'YYYY-MM-DD')
        :param end_date: End date for sales data (format: 'YYYY-MM-DD')
        """
        self.sellers = set_sellers(num_sellers)  # list of sellers
        self.start_date = datetime.strptime(start_date, '%Y-%m-%d')
        self.end_date = datetime.strptime(end_date, '%Y-%m-%d')
        self.sales_data = []
        self.targets = []


    def generate_sales_data(self):
        """
        Generates sales data for each seller across the defined date range.
        """
        current_date = self.start_date
        sales_range = abs((self.end_date - self.start_date).days)

        for day in range(sales_range + 1):
            for seller in self.sellers:
                sale_entry = seller.copy()
                sale_entry['state'] = get_state_sales()
                sale_entry['sales_date'] = current_date
                sale_entry['sales_value'] = random.randint(500, 1000)
                self.sales_data.append(sale_entry)
            current_date += timedelta(days=1)

    def calculate_targets(self, margin=0.1, multiplier=30):
        """
        Calculates monthly sales targets for each seller based on sales data.
        :param margin: Percentage margin added to the average sales for target calculation
        :param multiplier: Multiplier applied to the target value (default: 30)
        """
        calculated_data = defaultdict(lambda: {'total_sales': 0, 'count': 0})

        for entry in self.sales_data:
            seller_id = entry['seller_id']
            date_ref = entry['sales_date'].replace(day=1)
            calculated_data[(seller_id, date_ref)]['total_sales'] += entry['sales_value']
            calculated_data[(seller_id, date_ref)]['count'] += 1

        for (seller_id, date_ref), values in calculated_data.items():
            avg_sales = values['total_sales'] / values['count']
            target_value = avg_sales * (1 + margin) * multiplier
            self.targets.append({
                'seller_id': seller_id,
                'date_ref': date_ref,
                'target_value': round(target_value, 0),
            })

    def get_targets(self):
        """
        Returns the list of calculated targets.
        :return: List of target dictionaries
        """
        return self.targets

    def get_sales(self):
        """
        Returns sales fake data.
        :return: List of target dictionaries
        """
        return self.sales_data

    def insert_sales_data(self):
        """
        insert sales data into postgresql database
        """
        sales_data_fake = self.get_sales()
        with engine.connect() as conn:
            conn.execute(
                insert(Sales),
                sales_data_fake
            )
            conn.commit()
            print('sales data inserted!')

    def insert_targets_data(self):
        """
        insert sales data into postgresql database
        """
        target_data_fake = self.get_targets()
        with engine.connect() as conn:
            conn.execute(
                insert(Targets),
                target_data_fake
            )
            conn.commit()
            print('target data inserted!')


# Usage example
if __name__ == '__main__':

    # generating the sellers list
    generator = SalesDataGenerator(5, start_date='2023-01-01', end_date='2024-12-31')

    # inserting sales data
    generator.generate_sales_data()
    generator.insert_sales_data()


    # inserting target data
    generator.calculate_targets()
    generator.insert_targets_data()