import os
from typing import Dict, Optional


def build_proxies(
    http_proxy: Optional[str] = None,
    https_proxy: Optional[str] = None,
    socks_proxy: Optional[str] = None,
) -> Optional[Dict[str, str]]:
    http = http_proxy or os.getenv("HTTP_PROXY") or os.getenv("http_proxy")
    https = https_proxy or os.getenv("HTTPS_PROXY") or os.getenv("https_proxy")
    socks = socks_proxy or os.getenv("SOCKS_PROXY") or os.getenv("socks_proxy")

    proxies: Dict[str, str] = {}
    if socks:
        proxies["http"] = socks
        proxies["https"] = socks
    if http:
        proxies["http"] = http
    if https:
        proxies["https"] = https

    return proxies or None