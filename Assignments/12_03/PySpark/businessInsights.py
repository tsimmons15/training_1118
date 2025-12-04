from pyspark.sql import SparkSession
from pyspark.sql import Row
from pyspark.sql.functions import lit, col

import csv

spark = SparkSession.builder \
.master("local[*]") \
.appName("businessInsight") \
.getOrCreate()

events_ds = []
order_items_ds = []
orders_ds = []
products_ds = []
reviews_ds = []
users_ds = []

with open(r'C:\Users\Timothy Simmons\Documents\Resources\ecommerce_dataset\events.csv', mode='r') as fh:
    csv_reader = csv.reader(fh)
    for line in csv_reader:
        events_ds.append(line)
with open(r'C:\Users\Timothy Simmons\Documents\Resources\ecommerce_dataset\order_items.csv', mode='r') as fh:
    csv_reader = csv.reader(fh)
    for line in csv_reader:
        order_items_ds.append(line)
with open(r'C:\Users\Timothy Simmons\Documents\Resources\ecommerce_dataset\orders.csv', mode='r') as fh:
    csv_reader = csv.reader(fh)
    for line in csv_reader:
        orders_ds.append(line)
with open(r'C:\Users\Timothy Simmons\Documents\Resources\ecommerce_dataset\products.csv', mode='r') as fh:
    csv_reader = csv.reader(fh)
    for line in csv_reader:
        products_ds.append(line)
with open(r'C:\Users\Timothy Simmons\Documents\Resources\ecommerce_dataset\reviews.csv', mode='r') as fh:
    csv_reader = csv.reader(fh)
    for line in csv_reader:
        reviews_ds.append(line)
with open(r'C:\Users\Timothy Simmons\Documents\Resources\ecommerce_dataset\users.csv', mode='r') as fh:
    csv_reader = csv.reader(fh)
    for line in csv_reader:
        users_ds.append(line)

#custom_schema = StructType([
#        StructField("name", StringType(), True),
#        StructField("age", IntegerType(), False),
#        StructField("city", StringType(), True)
#])
#events_schema = "event_id string user_id string product_id string event_type string event_timestamp timestamp"
#order_items_schema = "order_item_id string order_id string product_id string quantity int item_price double"
#orders_schema = "order_id string user_id string order_date date order_status string total_amount double"
#products_schema = "product_id string product_name string category string price double rating double"
#reviews_schema = "review_id string user_id string product_id string rating int review_text string review_date date"
#users_schema = "user_id string name string email string gender string city string signup_date date"

events_df = spark.createDataFrame(events_ds, inferSchema=True)
order_items_df = spark.createDataFrame(order_items_ds, order_items_schema)
orders_df = spark.createDataFrame(orders_ds, order_schema)
products_df = spark.createDataFrame(products_ds, products_schema)
reviews_df = spark.createDataFrame(reviews_ds, reviews_schema)
users_df = spark.createDataFrame(users_ds, users_schema)