import pytest
from amazon_product_extractor.scrapper import AmazonScrapper
from amazon_product_extractor.validator import AmazonUrlValidator, UrlValidator


@pytest.fixture
def amazon_url_validator():
    yield AmazonUrlValidator()


@pytest.fixture
def amazon_scrapper(amazon_url_validator: UrlValidator):
    yield AmazonScrapper * (amazon_url_validator)


def test_get_product_successfully(amazon_scrapper: AmazonScrapper):
    assert True
