from selenium import webdriver
import time
from bs4 import BeautifulSoup as BS

driver = webdriver.Chrome(r'C:\Users\infa.LYCEUM61\.wdm\drivers\chromedriver\win32\93.0.4577.63\chromedriver.exe')
driver.get('https://sbermarket.ru/metro/c/ovoshchi-frukty-oriekhi/frukty')

js = 'window.scrollTo(0, document.body.scrollHeight);'
for i in range(4):
    driver.execute_script(js)
    time.sleep(2)

main_page = driver.page_source
soup = BS(main_page, 'html.parser')

tovars = [item.text for item in soup.select('a._1PU84  h3._3pFCt')]
weights = [item.text for item in soup.select('a._1PU84  div._1FpZ7 div._2zcEX span')]
prices = [item.text for item in soup.find('a._1PU84  div._1FpZ7 div._2zcEX').next_sibling.strip()]
print(prices)
for i in range(len(prices)):
    d = prices[i].split("\\ ")
    a = d[0].replace(weights[i], '')
    b = "".join(filter(lambda d: str.isdigit(d) or d == ',', a))
    b = b.replace(',', '.')
    print(tovars[i] + " ("+weights[i]+") ", b)
