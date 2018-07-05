from time import sleep
from random import randint
from multiprocessing import Process
from typing import Set

from selenium import webdriver
from selenium.webdriver.common.proxy import Proxy, ProxyType
from user_agent import generate_user_agent

from config import RPM, ERROR_COEFFICIENT, URL, KEY_WORDS, \
    PROXY_HOST, PROXY_PORT, PROXY_USER, PROXY_PASSWORD


class Crawler:
    def __call__(self):

        proxy = Proxy({
            'proxyType': ProxyType.MANUAL,
            'httpProxy': f"http://{PROXY_USER}:{PROXY_PASSWORD}@{PROXY_HOST}:{PROXY_PORT}"
        })

        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        options.add_argument("--headless")
        options.add_argument(f"user-agent={generate_user_agent()}")
        capabilities = webdriver.DesiredCapabilities.CHROME
        proxy.add_to_capabilities(capabilities)

        driver = webdriver.Chrome("./chromedriver", chrome_options=options,
                                  desired_capabilities=capabilities)
        driver.get(URL)

        elements = driver.find_elements_by_tag_name("a")
        for element in elements:
            if has_concurrences(KEY_WORDS, element.text):
                element.click()

        driver.close()


def form_word_set(word_string: str) -> Set[str]:
    return {word.strip(',;').lower() for word in word_string.split(" ")}


def has_concurrences(words1: str, words2: str) -> bool:
    word_set1 = form_word_set(words1)
    word_set2 = form_word_set(words2)
    if word_set1.intersection(word_set2):
        return True

    return False


def get_delay() -> float:
    return 60 / randint(round(RPM / (1 + ERROR_COEFFICIENT)),
                        round(RPM * (1 + ERROR_COEFFICIENT)))


if __name__ == "__main__":
    while True:
        crawler = Crawler()
        c = Process(target=crawler)
        c.start()

        delay = get_delay()
        sleep(delay)
