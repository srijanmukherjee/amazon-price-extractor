from abc import ABC, abstractmethod
from typing import List
from bs4 import BeautifulSoup

from amazon_product_extractor.model.selector_schema import SelectorSchema


class SchemaNotProvidedException(Exception):
    pass


class InvalidSelectionException(Exception):
    def __init__(self, selector: str) -> None:
        super().__init__(f"{selector} did not select any element")


class ProductSelector(ABC):
    @abstractmethod
    def select_name(self, soup: BeautifulSoup) -> str:
        pass

    @abstractmethod
    def select_review_count(self, soup: BeautifulSoup) -> int:
        pass

    @abstractmethod
    def select_rating(self, soup: BeautifulSoup) -> float:
        pass

    @abstractmethod
    def select_price(self, soup: BeautifulSoup) -> float:
        pass

    @abstractmethod
    def select_discount(self, soup: BeautifulSoup) -> float:
        pass

    @abstractmethod
    def select_currency(self, soup: BeautifulSoup) -> str:
        pass

    @abstractmethod
    def select_about(self, soup: BeautifulSoup) -> str:
        pass


class SchemaProductSelector(ProductSelector):
    def __init__(self, schema: SelectorSchema):
        self.schema = schema

    def select_name(self, soup: BeautifulSoup) -> str:
        return self.__select__(soup, self.schema.name)

    def select_review_count(self, soup: BeautifulSoup) -> int:
        return int(self.__select__(soup, self.schema.review_count))

    def select_rating(self, soup: BeautifulSoup) -> float:
        return float(self.__select__(soup, self.schema.rating))

    def select_price(self, soup: BeautifulSoup) -> float:
        return float(self.__select__(soup, self.schema.price))

    def select_discount(self, soup: BeautifulSoup) -> float:
        return float(self.__select__(soup, self.schema.discount))

    def select_currency(self, soup: BeautifulSoup) -> str:
        return self.__select__(soup, self.schema.currency)

    def select_about(self, soup: BeautifulSoup) -> str:
        return self.__select__(soup, self.schema.about)

    def __select__(self, soup: BeautifulSoup, selector: str) -> str:
        element = soup.select_one(selector)
        if element is None:
            raise InvalidSelectionException(selector)

        return element.get_text()


class AmazonProductSelector(SchemaProductSelector):
    def select_name(self, soup: BeautifulSoup) -> str:
        return super().select_name(soup).strip()

    def select_about(self, soup: BeautifulSoup) -> List[str]:
        elements = soup.select(self.schema.about)
        return [el.get_text() for el in elements]

    def select_discount(self, soup: BeautifulSoup) -> str:
        return super().__select__(soup, self.schema.discount)

    def select_price(self, soup: BeautifulSoup) -> float:
        price = super().__select__(soup, self.schema.price)
        price = price.replace(",", "")
        return float(price)

    def select_review_count(self, soup: BeautifulSoup) -> str:
        return super().__select__(soup, self.schema.review_count)
