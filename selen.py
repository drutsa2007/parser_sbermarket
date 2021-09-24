from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
from bs4 import BeautifulSoup as BS

magazin = ['metro']
# driver = webdriver.Chrome()
driver = webdriver.Chrome(ChromeDriverManager().install())
for mag in range(len(magazin)):
    driver.get("https://sbermarket.ru/" + magazin[mag])
    js = 'window.scrollTo(0, document.body.scrollHeight);'
    for i in range(20):
        driver.execute_script(js)
        time.sleep(3)

    main_page = driver.page_source
    soup = BS(main_page, 'html.parser')

    url1 = 'https://sbermarket.ru'
    links = [url1+item['href'] for item in soup.select('h3._1H_dX a')]
    texts = [item.text for item in soup.select('h3._1H_dX div._2VRk1 span')]
    #print(links)
    #print(texts)
    dict_kategory = {}
    for i in range(1, len(texts)):
        dict_kategory[texts[i]] = links[i]
        with open('kategory_'+magazin[mag]+'.sql', 'a', encoding='utf-8') as f:
            sql = "INSERT INTO `kategory` ('mag_id', 'name') VALUES ("+str(mag)+", '"+texts[i]+"');"
            f.write(sql + "\n")
        with open('kategory_'+magazin[mag]+'_links.txt', 'a', encoding='utf-8') as f:
            f.write(links[i] + "\n")
driver.close()
# for i in dict_kategory.items():

# js = 'window.scrollTo(0, document.body.scrollHeight);'
# for i in range(20):
#     driver.execute_script(js)
#     time.sleep(3)
# results = driver.find_elements_by_xpath('//div[@class="_2VRk1"]')
# links = {}
# for i in results:
#     with open('kategory.txt', 'w+') as f:
#         f.write(i.text)
#         links[i.text] =
