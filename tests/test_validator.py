import pytest
from amazon_product_extractor.validator import AmazonUrlValidator, UrlValidator


@pytest.fixture
def amazon_validator():
    yield AmazonUrlValidator()


def test_valid_amazon_url(amazon_validator: UrlValidator):
    valid_urls = [
        "https://www.amazon.in/Western-Digital-Elements-Compatible-WDBU6Y0015BBK-WESN/dp/B06XDKWLJH",
        "https://www.amazon.in/Sounce-Drive-Pouch-Seagate-Toshiba/dp/B088BGY43C/ref=pd_bxgy_img_d_sccl_1/260-8376877-9715966",
    ]

    amazon_validator.validate(valid_urls[0])

    for url in valid_urls:
        assert amazon_validator.validate(url)


def test_invalid_amazon_url(amazon_validator: UrlValidator):
    invalid_urls = [
        "https://www.amazon.Western-Digital-Elements-Compatible-WDBU6Y0015BBK-WESN/dp/B06XDKWLJH/ref=sr_1_3?crid=2MS71M9L1IT8O&keywords=1.5tb%2Bexternal%2Bhdd&qid=1704533577",
        "https://www.google.in/Sounce-Drive-Pouch-Seagate-Toshiba/dp/B088BGY43C/ref=pd_bxgy_img_d_sccl_1",
    ]

    for url in invalid_urls:
        assert amazon_validator.validate(url) is False
