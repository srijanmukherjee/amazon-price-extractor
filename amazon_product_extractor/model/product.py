from abc import ABC
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Product(ABC):
    name: str
    price: int
    currency: str
    discount: int
    rating: Optional[float]
    review_count: Optional[int]

@dataclass
class AmazonProduct(Product):
    about: List[str]