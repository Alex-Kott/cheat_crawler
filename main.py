from selenium import webdriver
from time import sleep
from user_agent import generate_user_agent, generate_navigator
from random import random
from multiprocessing import Process

from config import RPM, ERROR_COEFFICIENT, URL


class Crawler:
    def __call__(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        # options.add_argument("--headless")
        driver = webdriver.Chrome("./chromedriver", chrome_options=options)

        driver.get(URL)
        sleep(3)
        driver.close()


def get_delay():
    return 60 / randint(RPM/ERROR_COEFFICIENT, RPM*ERROR_COEFFICIENT)


if __name__ == "__main__":


    while True:
    # for i in range(5):
        crawler = Crawler()
        c = Process(target=crawler)
        # c.start()

        delay = get_delay()
        print(delay)
        sleep(1)

