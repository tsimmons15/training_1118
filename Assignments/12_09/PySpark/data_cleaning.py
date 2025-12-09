from pyspark.sql import SparkSession
from pyspark.sql.functions import array, concat, dense_rank, desc, lit, col, to_date, max as maximum, month, year, datediff, countDistinct, when, current_date as now, sum as spark_sum
from pyspark.sql.types import IntegerType, StringType, DateType, DoubleType
from pyspark.sql.window import Window

spark = SparkSession.builder.appName("Orders").getOrCreate()

df = spark.read.option("header","true").option("inferSchema", "true").csv(r"orders.csv")

df = df.withColumnRenamed("sum", "order_total")

df = df.withColumn("order_id", col("order_id").cast(IntegerType()))

# Try to coerce the date column into a date format, not a string
# With the date format applied, invalid dates are turned into nulls, so the null fill
# should handle them.
df = df.withColumn("order_date", to_date(col("order_date"), "dd-MM-yyyy"))

df = df.withColumn("order_customer_id", col("order_customer_id").cast(IntegerType()))
df = df.withColumn("order_total", col("order_total").cast(DoubleType()))

df = df.na.fill({"order_date": "1970-01-01","order_total":-1,"order_status":"UNKNOWN"})

print("Duplicates: ")
df.groupBy("order_id").count().filter("count > 1").show()

print("Dates out of range:")
df.filter(datediff(now(), col("order_date")) < 0).show()

df.show()

print("Transformation #1 -- How can you rank customers based on total revenue?")
windowConf = Window.orderBy(desc("order_total"))
df.filter(col("order_total") > 0).withColumn("rank", dense_rank().over(windowConf)).show()

print("Transformation #2 -- How do you pivot order status so each status becomes a column?")
df.filter(col("order_total") > 0).groupBy("order_customer_id").pivot("order_status").sum("order_total").show()

print("Transformation #3 -- How do you calculate monthly revenue trends from order_date? ")
df.filter((col("order_total") > 0) & (col("order_date") > to_date(lit("1970-01-01"), "yyyy-MM-dd"))).groupBy(concat(month("order_date"), lit(" "), year("order_date"))).sum("order_total").show()

print("Transformation #4 -- How can you identify customers who have churned (no orders in last X days)?")
churn_date = 10
df.printSchema()
df.filter((col("order_total") > 0) & (col("order_date") > to_date(lit("1970-01-01"), "yyyy-MM-dd"))).groupBy("order_customer_id") \
    .agg(maximum("order_date")).filter(datediff(now(),to_date("max(order_date)", "yyyy-MM-dd")) > churn_date) \
    .withColumn("churn", datediff(now(),to_date("max(order_date)", "yyyy-MM-dd")).cast(IntegerType())).orderBy("churn", ascending=False).show()