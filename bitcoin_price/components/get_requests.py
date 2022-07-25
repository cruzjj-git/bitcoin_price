import requests


def get_url_request(url: str, headers: dict, params: dict, timeout=1.00) -> requests.models.Response:
    try:
        response = requests.get(url=url, headers=headers, params=params, timeout=timeout)
    except Exception as e: #TODO catch multiple granular exceptions instead of this so proper actions can be taken
        print(f"Error: {e}")
        
    return response
