from components.get_requests import get_url_request, requests


def get_ecb_exchange_rate_hist(period:str, base_currency:str, to_currency:str, start_date:str, end_date:str) -> requests.models.Response:
    url = f'https://sdw-wsrest.ecb.europa.eu/service/data/EXR/{period}.{base_currency}.{to_currency}.SP00.A'
    headers = {'Accept':'text/csv'}
    params = {
        'startPeriod': start_date,
        'endPeriod': end_date,
        'detail': 'dataonly'
    }
    response = get_url_request(url, headers=headers, params=params, timeout=1.00)
    if response.status_code != 200:
        raise Exception("Error while getting the data from ecb api")
    
    return response
