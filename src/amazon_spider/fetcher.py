import random
from typing import Optional, Dict

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from .const import USER_AGENTS


def create_session(max_retries: int = 3, backoff_factor: float = 0.5) -> requests.Session:
    session = requests.Session()
    retry = Retry(
        total=max_retries,
        read=max_retries,
        connect=max_retries,
        backoff_factor=backoff_factor,
        status_forcelist=(429, 500, 502, 503, 504),
        allowed_methods=("GET", "HEAD"),
        raise_on_status=False,
    )
    adapter = HTTPAdapter(max_retries=retry, pool_connections=100, pool_maxsize=100)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session


def fetch_html(
    url: str,
    session: requests.Session,
    proxies: Optional[Dict[str, str]] = None,
    timeout: float = 30.0,
) -> str:
    headers = {
        "User-Agent": random.choice(USER_AGENTS),
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Referer": "https://www.google.com/",
        "Connection": "keep-alive",
    }
    response = session.get(url, headers=headers, proxies=proxies, timeout=timeout)
    response.raise_for_status()
    return response.text