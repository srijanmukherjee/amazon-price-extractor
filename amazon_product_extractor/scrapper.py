from abc import ABC, abstractmethod
from amazon_product_extractor.model.product import AmazonProduct, Product
from amazon_product_extractor.validator import UrlValidator


class Scrapper(ABC):
    @abstractmethod
    def scrape_product(self, url: str) -> Product:
        pass


class AmazonScrapper(Scrapper):
    def __init__(self, url_validator: UrlValidator):
        self.url_validator = url_validator

    def scrape_product(self, url: str) -> AmazonProduct:
        raise NotImplementedError()
