from time import sleep
from random import randint
from multiprocessing import Process

from selenium import webdriver
from selenium.webdriver.common.proxy import Proxy, ProxyType
from user_agent import generate_user_agent

from config import RPM, ERROR_COEFFICIENT, URL, REDIRECT_URL, \
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
            link = element.get_attribute('href')
            if link.find(REDIRECT_URL) != -1:
                element.click()

        driver.close()


def get_delay():
    return 60 / randint(round(RPM / (1 + ERROR_COEFFICIENT)),
                        round(RPM * (1 + ERROR_COEFFICIENT)))


if __name__ == "__main__":
    while True:
        crawler = Crawler()
        c = Process(target=crawler)
        c.start()

        delay = get_delay()
        sleep(1)
