import concurrent.futures
from typing import Dict, List, Optional

import requests

from .fetcher import create_session, fetch_html
from .parser import parse_seller_page
from .proxy import build_proxies
from .types import SellerInfo


def process_url(
    url: str,
    session: requests.Session,
    proxies: Optional[Dict[str, str]],
    timeout: float,
) -> SellerInfo:
    try:
        html = fetch_html(url, session=session, proxies=proxies, timeout=timeout)
        return parse_seller_page(html, url=url)
    except Exception:
        return SellerInfo(seller=url)


def run(
    urls: List[str],
    max_workers: int = 20,
    timeout: float = 30.0,
    max_retries: int = 3,
    backoff_factor: float = 0.5,
    http_proxy: Optional[str] = None,
    https_proxy: Optional[str] = None,
    socks_proxy: Optional[str] = None,
) -> List[SellerInfo]:
    session = create_session(max_retries=max_retries, backoff_factor=backoff_factor)
    proxies = build_proxies(http_proxy=http_proxy, https_proxy=https_proxy, socks_proxy=socks_proxy)

    results_by_url: Dict[str, SellerInfo] = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_url = {
            executor.submit(process_url, url, session, proxies, timeout): url for url in urls
        }
        for future in concurrent.futures.as_completed(future_to_url):
            url = future_to_url[future]
            try:
                results_by_url[url] = future.result()
            except Exception:
                results_by_url[url] = SellerInfo(seller=url)

    ordered_results = [results_by_url.get(u, SellerInfo(seller=u)) for u in urls]
    return ordered_results