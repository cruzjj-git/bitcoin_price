from pyspark.sql.functions import col, max, avg, datediff, last
from pyspark.sql.types import StructType, StructField, StringType, DecimalType, DateType, TimestampType
from components.spark_utilities import get_spark_session, get_csv


euro_exr_schema = StructType([
    StructField('key', StringType(), False),
    StructField('frequency', StringType(), False),
    StructField('from_currency', StringType(), False),
    StructField('to_currency', StringType(), False),
    StructField('exr_type', StringType(), False),
    StructField('exr_suffix', StringType(), False),
    StructField('time_period', DateType(), False),
    StructField('exr_value', DecimalType(7,4), False)
])


bitcoin_schema = StructType([
    StructField('rate_close',DecimalType(11,2), False),
    StructField('rate_high',DecimalType(11,2), False),
    StructField('rate_low',DecimalType(11,2), False),
    StructField('rate_open',DecimalType(11,2), False),
    StructField('time_close',TimestampType(), False),
    StructField('time_open',TimestampType(), False)
])


def main():
    path = '/app'
    spark = get_spark_session('Get Euro Bitcoin price')
    euro_rates_df = get_csv(spark, f'{path}/*.csv', euro_exr_schema, header=True)
    if not euro_rates_df:
        raise Exception('Could not read Euro exr csv')
    
    euro_rates_df = euro_rates_df.selectExpr(
        'time_period AS reference_date',
        'exr_value AS euro_exchange_rate'
    )

    try:
        bitcoin_price_df = spark.read.options(multiLine=True).schema(bitcoin_schema).json(f'{path}/*.json')
    except Exception as e:
        print(f'Error while reading JSON files')
        raise Exception(f'Error while reading JSON files')
    
    bitcoin_price_df = bitcoin_price_df.select(
        col('rate_close').alias('price_usd'),
        col('time_open').cast(DateType()).alias('reference_date')
    )
    
    bitcoin_euro_price = bitcoin_price_df.alias('btc').join(
        euro_rates_df.alias('ecb'), (
            (datediff(col('btc.reference_date'), col('ecb.reference_date'))  >= 0) &
            (datediff(col('btc.reference_date'), col('ecb.reference_date'))  < 7)
        ),
        'inner'
    ).selectExpr(
        'btc.*',
        'ecb.reference_date AS rolling_dates',
        'CAST(btc.price_usd / ecb.euro_exchange_rate as decimal(11,2)) AS price_euro'
    )
    
    bitcoin_euro_avg_price = bitcoin_euro_price.groupBy('reference_date').agg(
        max('rolling_dates').alias('rolling_dates'),
        last('price_usd').cast(DecimalType(11,2)).alias('price_usd'),
        last('price_euro').cast(DecimalType(11,2)).alias('price_euro'),
        avg('price_euro').cast(DecimalType(11,2)).alias('euro_7_day_avg')
    ).drop('rolling_dates')

    bitcoin_euro_avg_price.coalesce(1).write.mode('overwrite').parquet(f'{path}/bitcoin_euro')
    spark.stop()


if __name__ == '__main__':
    main()
