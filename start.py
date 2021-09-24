from parse import *
from selenium import webdriver

if __name__ == "__main__":
    driver = webdriver.Chrome(r'C:\Users\infa.LYCEUM61\.wdm\drivers\chromedriver\win32\93.0.4577.63\chromedriver.exe')

    # magazines = {0: 'metro', 1: 'lenta', 2: 'auchan', 3: 'okey', 4: 'magnit_express'}
    magazines = {2: 'auchan', 3: 'okey', 4: 'magnit_express'}
    for mag_id, mag in magazines.items():
        create_magazine(driver, mag_id, mag)
