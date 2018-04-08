import sys
from pyspark import SparkContext
from csv import reader
from pyspark.sql import SparkSession, Row, functions as f
from pyspark.sql.functions import udf
from datetime import datetime,date,timedelta
from pyspark.sql.types import StringType

#register the dataset
def register(file_path, name):
	name_str = name
	df = spark.read.format('csv').options(header = 'true',inferschema='true').load(file_path)
	df.createOrReplaceTempView(name)
	string_cols = []
	int_cols = []
	timestamp = []
	for colName, dtype in df.dtypes:
		if dtype == 'string':
			string_cols.append(colName)
		elif dtype == 'timestamp':
			timestamp.append(colName)
	string_metadata(name, string_cols, name_str)

#finding the string metadata for all columns
def string_metadata(df, string_cols, name):
	name = name+'_string_metadata.csv'
	for col in string_cols:
		query = "SELECT {} as col_value, count(*) as cnt FROM {} GROUP BY {}".format(col, df, col) 
		x = spark.sql(query)
		y = x.select(f.format_string(col+'\t%.2f, %.2f', x.col_value, x.cnt))
		x.select(f.format_string(col+', %s, %d', x.col_value, x.cnt)).write.mode("append").save(name,format="text")

if __name__ == "__main__":
	spark = spark = SparkSession.builder.appName("task7-sql").config("spark.some.config.option", "some-value").getOrCreate()
	name = sys.argv[2]
	file_path = sys.argv[1]
	register(file_path, name)



