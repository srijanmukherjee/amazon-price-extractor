import logging
import pytest
from amazon_product_extractor.model.selector_schema import SelectorSchema
from amazon_product_extractor.product_selector import AmazonProductSelector
from amazon_product_extractor.scrapper import AmazonScrapper
from amazon_product_extractor.validator import (
    AmazonUrlValidator,
    InvalidUrlException,
    UrlValidator,
)


@pytest.fixture
def amazon_product_selector_schema():
    yield SelectorSchema(
        about="#feature-bullets > ul > li",
        currency="#corePriceDisplay_desktop_feature_div > div.a-section.a-spacing-none.aok-align-center.aok-relative > span.a-price.aok-align-center.reinventPricePriceToPayMargin.priceToPay > span:nth-child(2) > span.a-price-symbol",
        discount="#corePriceDisplay_desktop_feature_div > div.a-section.a-spacing-none.aok-align-center.aok-relative > span.a-size-large.a-color-price.savingPriceOverride.aok-align-center.reinventPriceSavingsPercentageMargin.savingsPercentage",
        name="#productTitle",
        price="#corePriceDisplay_desktop_feature_div > div.a-section.a-spacing-none.aok-align-center.aok-relative > span.a-price.aok-align-center.reinventPricePriceToPayMargin.priceToPay > span:nth-child(2) > span.a-price-whole",
        rating="#acrPopover > span.a-declarative > a > span",
        review_count="#acrCustomerReviewText",
    )


@pytest.fixture
def amazon_product_selector(amazon_product_selector_schema: SelectorSchema):
    yield AmazonProductSelector(amazon_product_selector_schema)


@pytest.fixture
def amazon_url_validator():
    yield AmazonUrlValidator()


@pytest.fixture
def amazon_scrapper(
    amazon_url_validator: UrlValidator, amazon_product_selector: AmazonProductSelector
):
    yield AmazonScrapper(amazon_url_validator, amazon_product_selector)


def test_get_product_fail_with_invalid_url(amazon_scrapper: AmazonScrapper):
    invalid_urls = [
        "https://www.amazon.Western-Digital-Elements-Compatible-WDBU6Y0015BBK-WESN/dp/B06XDKWLJH/ref=sr_1_3?crid=2MS71M9L1IT8O&keywords=1.5tb%2Bexternal%2Bhdd&qid=1704533577"
    ]
    for url in invalid_urls:
        with pytest.raises(InvalidUrlException):
            amazon_scrapper.scrape_product(url)


def test_get_product(amazon_scrapper: AmazonScrapper):
    product = amazon_scrapper.scrape_product(
        "https://www.amazon.in/Western-Digital-Elements-Compatible-WDBU6Y0015BBK-WESN/dp/B06XDKWLJH"
    )

    logging.info(product)

    assert product is not None
