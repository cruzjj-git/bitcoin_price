from datetime import date, timedelta
from ecb_rates import get_ecb_exchange_rate_hist
    

def main():
    PERIOD='D'
    BASE_CURRENCY='USD'
    TO_CURRENCY='EUR'
    DATE_TIME_FORMAT='%Y-%m-%d'
    end_date = date.today()
    filename = f'{BASE_CURRENCY}_{TO_CURRENCY}_exr_{end_date.strftime("%Y-%m-%d")}.csv'
    start_date = end_date -  timedelta(days=365)
    start_date = start_date.strftime(DATE_TIME_FORMAT)
    end_date = end_date.strftime(DATE_TIME_FORMAT)
    
    try:
        response = get_ecb_exchange_rate_hist(PERIOD, BASE_CURRENCY, TO_CURRENCY, start_date, end_date)
    except Exception as e:
        print(f"Error while getting the date: [{e}]") #TODO proper exception handling
        raise Exception(f"Error while getting the date: [{e}]")

    with open(filename, 'w') as output_file:
        output_file.write(response.content.decode('utf-8'))
    

if __name__ == '__main__':
    main()
