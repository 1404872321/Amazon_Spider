from bs4 import BeautifulSoup
from typing import Optional

from .types import SellerInfo


def _text_or_dash(element: Optional[object]) -> str:
    if not element:
        return "-"
    text = element.get_text(strip=True)
    return text if text else "-"


def parse_seller_page(html: str, url: str) -> SellerInfo:
    soup = BeautifulSoup(html, "lxml")

    # Seller name
    seller_name = "-"
    for sid in ("seller-name", "sellerName", "sellerProfileTriggerId"):
        node = soup.find(id=sid)
        if node:
            seller_name = _text_or_dash(node)
            break

    # Ratings by time period
    rating_30days = _text_or_dash(soup.find(id="effective-timeperiod-rating-thirty-description"))
    rating_90days = _text_or_dash(soup.find(id="effective-timeperiod-rating-ninety-description"))
    rating_365days = _text_or_dash(soup.find(id="effective-timeperiod-rating-year-description"))
    rating_lifetime = _text_or_dash(soup.find(id="effective-timeperiod-rating-lifetime-description"))

    # Ratings histogram
    five_star = _text_or_dash(soup.find(id="percentFiveStar"))
    four_star = _text_or_dash(soup.find(id="percentFourStar"))
    three_star = _text_or_dash(soup.find(id="percentThreeStar"))
    two_star = _text_or_dash(soup.find(id="percentTwoStar"))
    one_star = _text_or_dash(soup.find(id="percentOneStar"))

    # Reviews list is not reliably selectable; leave empty for now
    reviews_list = []

    return SellerInfo(
        seller=url,
        seller_name=seller_name,
        rating_30days=rating_30days,
        rating_90days=rating_90days,
        rating_365days=rating_365days,
        rating_lifetime=rating_lifetime,
        reviews=reviews_list,
        percent_5star=five_star,
        percent_4star=four_star,
        percent_3star=three_star,
        percent_2star=two_star,
        percent_1star=one_star,
    )