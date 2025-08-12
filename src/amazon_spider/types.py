from dataclasses import dataclass, asdict, field
from typing import List, Dict, Any


@dataclass
class SellerInfo:
    seller: str
    seller_name: str = "-"
    rating_30days: str = "-"
    rating_90days: str = "-"
    rating_365days: str = "-"
    rating_lifetime: str = "-"
    reviews: List[str] = field(default_factory=list)
    percent_5star: str = "-"
    percent_4star: str = "-"
    percent_3star: str = "-"
    percent_2star: str = "-"
    percent_1star: str = "-"

    def to_dict(self) -> Dict[str, Any]:
        data = {
            "seller": self.seller,
            "sellerName": self.seller_name,
            "30daysRating": self.rating_30days,
            "90daysRating": self.rating_90days,
            "365daysRating": self.rating_365days,
            "lifetimeRating": self.rating_lifetime,
            "reviews": list(self.reviews or []),
            "5starPercentage": self.percent_5star,
            "4starPercentage": self.percent_4star,
            "3starPercentage": self.percent_3star,
            "2starPercentage": self.percent_2star,
            "1starPercentage": self.percent_1star,
        }
        return data