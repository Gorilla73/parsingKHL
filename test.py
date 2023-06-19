from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from webdriver_manager.chrome import ChromeDriverManager

url_KHL = "https://www.flashscore.com.ua/match/j3AFnAXq/#/odds-comparison/1x2-odds/full-time"
driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get(url=url_KHL)
time.sleep(5)
odds_selector = []
# odd_selector = driver.find_element(By.XPATH, '//*[@id="detail"]/div[8]/div[3]/div/div[2]/div/a[1]')
# odds_selector.append(odd_selector)
# odds_selector.append(driver.find_element(By.XPATH, '//*[@id="detail"]/div[8]/div[3]/div/div[2]/div/a[2]'))
# odds_selector.append(odd_selector)
# odds_selector.append(driver.find_element(By.XPATH, '//*[@id="detail"]/div[8]/div[3]/div/div[2]/div/a[3]'))
# odds_selector.append(odd_selector)
odds_selector = driver.find_elements(By.CSS_SELECTOR, ".oddsCell__odd.oddsCell__highlight ")
#                                                       ".oddsCell__odd.oddsCell__highlight "
collect_odds = odds_selector[0].text + " " + odds_selector[1].text + " " + odds_selector[2].text

print(collect_odds)
