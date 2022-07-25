from components.get_requests import get_url_request, requests


def get_coin_api_history_request(crypto: str, currency:str, period: str, start_time: str, end_time: str, limit: int=100000) -> requests.models.Response:
    if start_time > end_time:
        raise ValueError(f'start time [{start_time}] cannot be older than end time: [{end_time}]')
    url = f'http://rest.coinapi.io/v1/exchangerate/{crypto}/{currency}/history' #TODO ENTRYPOINT could be a secret stored in secret manager
    headers = {
        'X-CoinAPI-Key' : '' #TODO api key should be a secret stored in secret manager
    }
    params = {
        'period_id': period,
        'time_start': start_time,
        'time_end': end_time,
        'limit': limit
    }
    
    response = get_url_request(url, headers=headers, params=params, timeout=1.00)
    if response.status_code != 200:
        raise Exception("Error while getting the data from coin api")
    
    return response
