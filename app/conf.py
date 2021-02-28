import os


def get_with_warning(key, default=None):
    value = os.environ.get(key, default)
    if not value:
        raise ValueError(
            f"missing {key}, you can supply one in docker-compose.yml"
            f",or docker run -e {key}=secret or in the shell export {key}=value")
    return value


MARKETSTACK_API_KEY = get_with_warning('MARKETSTACK_API_KEY')
MARKETSTACK_API_URL = get_with_warning('MARKET_API_URL', 'http://api.marketstack.com/v1/eod')
