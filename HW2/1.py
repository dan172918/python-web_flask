#!/usr/bin/python
# coding:utf-8
import sys,os
from pyspark import SparkContext
from pyspark.sql import SQLContext
from pyspark.sql.types import *
from datetime import datetime, timedelta
from pyspark.sql.functions import to_timestamp
from pyspark.sql.functions import *
from pyspark.sql.functions import avg, round
import pyspark.sql.functions as f
from pyspark.sql import Window
from pyspark import *
import pandas as pd
import matplotlib.pyplot as plt

sc = SparkContext.getOrCreate()
spark = SQLContext(sc)
df = spark.read.format("csv").option("encoding","BIG5").option("header", "true").option("inferSchema", "true")\
.load("./HW2_DATA.csv")

# df.show()
df1 = df.filter((df['year']=="93") | (df['year']=="94") | (df['year']=="95") | (df['year']=="96") | (df['year']=="97")).select("year","month","Average_Asset","Average_Net_worth")
table1 = df1.groupBy("year").agg(f.min("Average_Asset").alias("Min"),f.max("Average_Asset").alias("Max"),round(f.mean("Average_Asset"),2).alias("Average")).sort("year")
table1.show(truncate=False)

data = df1.groupBy("year").agg(round(f.mean("Average_Asset"),2).alias("Average")).sort("year").toPandas()
ax=data.plot(kind='bar',x='year',y='Average',color='r')
ax.set_ylabel('Average')

plt.ylabel("Average")
plt.title("Average_Asset")

plt.xticks(rotation=45)
plt.tight_layout()
plt.show()