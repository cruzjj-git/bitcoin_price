from pyspark.sql import SparkSession
from pyspark.sql import DataFrame
from pyspark.sql.types import StructType
from typing import Optional


def get_spark_session(app_name: str) -> SparkSession:
    return SparkSession \
        .builder \
        .appName(app_name) \
        .getOrCreate()


def get_csv(spark: SparkSession, path: str, schema: StructType, **kwargs) -> Optional[DataFrame]:
    delimiter = kwargs.get('delimiter', ',')
    mode = kwargs.get('mode', 'FAILFAST')
    header = kwargs.get('header', False)
    try:
        return spark.read.options(delimiter=delimiter, mode=mode, header=header).schema(schema).csv(path)
    except Exception as e:
        print(f"Issue while trying to get CSV into DataFrame: [{e}]")
        return None
