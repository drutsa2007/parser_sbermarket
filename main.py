import requests
from bs4 import BeautifulSoup

headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36(KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36'}
url = 'https://sbermarket.ru/metro'
r = requests.get(url, headers=headers)
soup = BeautifulSoup(r.text, 'html.parser')

# print(soup)
# a = soup.find_all('a', class_='_1PU84 ')  # , class_='sale-card'
url1 = 'https://sbermarket.ru'
links = [url1+item['href'] for item in soup.select('h3._1H_dX a')]
texts = [item.text for item in soup.select('h3._1H_dX div._2VRk1 span')]
print(links)
print(texts)

# url = 'https://5ka.ru/'
# r = requests.get(url)
# soup = BeautifulSoup(r.text)
# a = soup.find_all('a').text
# print(a)
