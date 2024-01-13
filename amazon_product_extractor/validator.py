from abc import ABC, abstractmethod
import logging
from urllib.parse import urlparse


class UrlValidator(ABC):
    @abstractmethod
    def validate(self, url: str) -> bool:
        pass


class AmazonUrlValidator(UrlValidator):
    schemes = ["https", "http"]
    tld = ["com", "in"]
    domain = ["amazon"]

    def __init__(self):
        self.netlocs = []
        for root in ["", "www."]:
            for end in self.tld:
                for name in self.domain:
                    self.netlocs.append(f"{root}{name}.{end}")

    def validate(self, url: str) -> bool:
        result = urlparse(url)
        logging.debug(result)

        if result.scheme not in self.schemes:
            return False

        if result.netloc not in self.netlocs:
            return False

        parts = result.path.split("/")
        if len(parts) < 4:
            return False

        if parts[2] != "dp":
            return False

        return True
