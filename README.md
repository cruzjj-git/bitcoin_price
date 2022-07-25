# bitcoin_prices V1
fetches BitCoin close price in USD and generates the last 7-day rolling average in EUR for the last year using the reference exchange rate from the European Central Bank. The application should produce two outputs:
4 columns: the reference date, the original USD price, the converted EUR price, and last 7-day rolling average.
A visualization of the 7-day average over time.

Important:
in order to retrieve data from the Coin base API you will need to add the key in coin_api.key
'X-CoinAPI-Key' : ''

How to run the scripts
Retrieves a CSV for the last year of rates between USD and EURO
python3 euro_rates.py

Can run in parallel, retrieves a JSON file with the last year of data for Bitcoin prices in USD
python3 crypto_price.py

Read previously created files and joins them to get the last 7 days average in Euro currency, stores the data as parquet
spark-submit xfm_euro_price.py

Reads the parquet files and create a graphic and saves it as an image
spark-submit data_visualization.py
