from pyspark.sql import SparkSession
from pyspark.sql.functions import col,when
from pyspark.sql.types import ( StructType,StructField,StringType,DoubleType )


spark=SparkSession.builder \
    .appName("BeginnerGuide") \
    .master("local[*]") \
    .getOrCreate()

df=spark.read.csv("pyspark_interview_mock_transactions.csv",header=True,inferSchema=True)

schema=StructType([
    StructField("transaction_id", StringType(), True),
    StructField("customer_id", StringType(), True),
    StructField("txn_timestamp", StringType(), True),
    StructField("amount", DoubleType(), True),
    StructField("category", StringType(), True),
    StructField("payment_method", StringType(), True),
    StructField("city", StringType(), True),
    StructField("status", StringType(), True),
    StructField("metadata_json", StringType(), True)


])

df =spark.read.csv("pyspark_interview_mock_transactions.csv",header=True,schema=schema)

df.printSchema()

df.show(5,truncate=False)

print(f"Total records:{df.count()}")

print(df.columns)
print(df.dtypes)

df.filter(col("status")=="Success").show(5)