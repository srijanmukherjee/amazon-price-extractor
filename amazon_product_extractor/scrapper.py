from abc import ABC, abstractmethod
import logging
from bs4 import BeautifulSoup

import requests
from requests.exceptions import HTTPError
from fake_useragent import UserAgent
from amazon_product_extractor.model.product import AmazonProduct, Product
from amazon_product_extractor.product_selector import AmazonProductSelector
from amazon_product_extractor.validator import InvalidUrlException, UrlValidator


class Scrapper(ABC):
    @abstractmethod
    def scrape_product(self, url: str) -> Product:
        pass


class AmazonScrapper(Scrapper):
    def __init__(
        self, url_validator: UrlValidator, product_selector: AmazonProductSelector
    ):
        self.url_validator = url_validator
        self.product_selector = product_selector

        ua = UserAgent(browsers=["firefox", "chrome"])
        self.headers = {"User-Agent": ua.random}

    def scrape_product(self, url: str) -> AmazonProduct:
        if not self.url_validator.validate(url):
            raise InvalidUrlException(url)

        response = requests.get(url, headers=self.headers)

        if response.status_code != 200:
            logging.debug(f"Server responded with status code {response.status_code}")
            raise HTTPError(response=response)

        soup = BeautifulSoup(response.text, "lxml")

        logging.info(f"title = {self.product_selector.select_name(soup)}")

        return AmazonProduct(
            name=self.product_selector.select_name(soup),
            about=self.product_selector.select_about(soup),
            price=self.product_selector.select_price(soup),
            currency=self.product_selector.select_currency(soup),
            rating=self.product_selector.select_rating(soup),
            review_count=self.product_selector.select_review_count(soup),
            discount=self.product_selector.select_discount(soup),
        )
