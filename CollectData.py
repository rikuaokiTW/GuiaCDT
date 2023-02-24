from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

driver = webdriver.Firefox()
driver.get('https://myanimelist.net/anime/season/2023/spring')

"""
animes = driver.find_elements(By.CSS_SELECTOR, '.js-seasonal-anime-list-key-1 .h2_anime_title')

animes[0].click()
information = driver.find_elements(By.CSS_SELECTOR, ".spaceit_pad")
information = [info.text for info in information]

animes = [item.text for item in animes]
"""
