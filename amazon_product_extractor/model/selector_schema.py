from pydantic import BaseModel


class SelectorSchema(BaseModel):
    name: str
    price: str
    currency: str
    discount: str
    rating: str
    review_count: str
    about: str
