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
from pyspark.ml.linalg import Vectors
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.regression import LinearRegression

sc = SparkContext.getOrCreate()
spark = SQLContext(sc)
df = spark.read.format("csv").option("encoding","BIG5").option("header", "true").option("inferSchema", "true")\
.load("./HW2_DATA.csv")

assembler = VectorAssembler(inputCols=['Average_Asset','Average_Net_worth'],outputCol='features')
output = assembler.transform(df).select('features','Surplus_before_tax')
A,B=output.randomSplit([0.7,0.3])
lm = LinearRegression(featuresCol='features',labelCol='Surplus_before_tax')
model = lm.fit(A)
unlabeled_data = A.select('features')
pre = model.transform(unlabeled_data)
res = model.evaluate(B)
data = res.predictions
data.show()

x=data.select('prediction').toPandas()['prediction'].values.tolist()
y=data.select('Surplus_before_tax').toPandas()['Surplus_before_tax'].values.tolist()
plt.plot(y,y,c="red")
plt.scatter(x,y)

plt.show()
