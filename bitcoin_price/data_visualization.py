import plotly.express as px
from components.spark_utilities import get_spark_session


def main():
    path = '/app'
    spark = get_spark_session('data_viz')
    df = spark.read.parquet(f'{path}/bitcoin_euro/')
    data = df.orderBy('reference_date').toPandas()
    fig = px.line(
        data,
        x='reference_date',
        y='euro_7_day_avg'
    )
    
    fig.write_image('bitcoin_euro_price.png')
    spark.stop()


if __name__ == '__main__':
    main()
