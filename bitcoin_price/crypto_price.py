import json
from datetime import date, timedelta
from coin_api import get_coin_api_history_request
    

def main():
    CRYPTO='BTC'
    CURRENCY='USD'
    PERIOD='1DAY'
    DATE_TIME_FORMAT='%Y-%m-%dT%H:%M:%S'
    end_date = date.today()
    filename = f'{CRYPTO}_{CURRENCY}_price_{end_date.strftime("%Y-%m-%d")}.json'
    start_date = end_date -  timedelta(days=372)
    start_time = start_date.strftime(DATE_TIME_FORMAT)
    end_time = end_date.strftime(DATE_TIME_FORMAT)
    
    try:
        response = get_coin_api_history_request(CRYPTO, CURRENCY, PERIOD, start_time, end_time)
        json_response = response.json()
    except Exception as e:
        print(f"Error while getting the date: [{e}]") #TODO proper exception handling
        raise Exception(f"Error while getting the date: [{e}]")
    
    if not json_response:
        raise Exception(f"API got no results for this query: [{response.url}]")
    
    with open(filename, 'w') as output_file:
        output_file.write(json.dumps(json_response))
    
    
if __name__ == '__main__':
    main()
