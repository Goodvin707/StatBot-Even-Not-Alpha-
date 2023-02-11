from bs4 import BeautifulSoup
from selenium import webdriver


def prepare_data(url):
    driver = webdriver.Edge()
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    driver.quit()

    # page = requests.get(url)
    # soup = BeautifulSoup(page.text, "lxml")
    return soup


# def try_in_remote_web_driver(url):
#     firefox_options = webdriver.FirefoxOptions()
#     driver = webdriver.Remote(
#         command_executor="http://127.0.0.1:4444", options=firefox_options
#     )
#     driver.get(url)
#     soup = BeautifulSoup(driver.page_source, "html.parser")
#     driver.quit()

#     print(soup)


# try_in_remote_web_driver("https://clashspot.net/en/clan/V8GJ9C0U/view/home-village")
