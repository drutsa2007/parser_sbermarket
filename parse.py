import time
from bs4 import BeautifulSoup as BS

kats = {}
kat_id = 1
tovar_id = 4
number_file = 1


def create_magazine(driver, mag_id, name):
    sql = "INSERT INTO `magazines` (`id`, `name`) VALUES (" + str(mag_id) + ", '" + name + "');"
    with open('magazines.sql', 'a', encoding='utf-8') as f:
        f.write(sql + "\n")
    print('Магазин:', name, 'добавлен.')
    parse_kategory(driver, mag_id, 'https://sbermarket.ru/' + name)


def parse_kategory(driver, mag_id, url):
    driver.get(url)
    kategories = ['Овощи, фрукты, орехи', 'Молочные продукты, яйца',
                  'Мясо, птица', 'Рыба, морепродукты',
                  'Замороженные продукты', 'Бакалея',
                  'Вода, соки, напитки', 'Колбасы, сосиски, деликатесы']
    # Прокручиваем вниз до конца
    js = 'window.scrollTo(0, document.body.scrollHeight);'
    for i in range(15):
        driver.execute_script(js)
        time.sleep(3)

    main_page = driver.page_source
    soup = BS(main_page, 'html.parser')

    url1 = 'https://sbermarket.ru'
    links = [url1 + item['href'] for item in soup.select('h3._1H_dX a')]
    texts = [item.text for item in soup.select('h3._1H_dX div._2VRk1 span')]
    for i in range(1, len(texts)):
        if texts[i] == 'Сыры':
            return
        if texts[i] in kategories:
            print('Категория', texts[i], 'в процессе.')
            create_sub_kategory(driver, links[i], mag_id)
            print('Категория', texts[i], 'обработана.')

    driver.close()


def create_sub_kategory(driver, url, mag_id):
    global kat_id, kats
    driver.get(url)
    print('Переход в подкатегорию...')

    js = 'window.scrollTo(0, document.body.scrollHeight);'
    for i in range(15):
        driver.execute_script(js)
        time.sleep(3)

    main_page = driver.page_source
    soup = BS(main_page, 'html.parser')

    url1 = 'https://sbermarket.ru'
    links = [url1 + item['href'] for item in soup.select('h3._1H_dX a')]
    texts = [item.text for item in soup.select('h3._1H_dX div._2VRk1 span')]
    for i in range(0, len(texts)):
        print('Подкатегория: ' + texts[i] + ' в процессе.')
        if texts[i] not in kats:
            kats[kat_id] = texts[i]
            with open('kategory.sql', 'a', encoding='utf-8') as f:
                sql = "INSERT INTO `kategory` " \
                      "(`id`, `name`) VALUES " \
                      "(" + str(kat_id) + ", '" + texts[i] + "');"
                f.write(sql + "\n")
            parse_tovar(driver, links[i], mag_id, kat_id)
            kat_id += 1
        else:
            for key, value in kats.items():
                if value == texts[i]:
                    kat_id = key
            parse_tovar(driver, links[i], mag_id, kat_id)
        print('Работа с подкатегорией: ' + texts[i] + ' окончена.')


def parse_tovar(driver, url, mag_id, kat_id):
    global tovar_id, number_file
    driver.get(url)

    js = 'window.scrollTo(0, document.body.scrollHeight);'
    for i in range(15):
        driver.execute_script(js)
        time.sleep(3)

    main_page = driver.page_source
    soup = BS(main_page, 'html.parser')

    tovars = [item.text for item in soup.select('a._1PU84  h3._3pFCt')]
    weights = [item.text for item in soup.select('a._1PU84  div._1FpZ7 div._2zcEX span')]
    prices = [item.text for item in soup.select('a._1PU84  div._1FpZ7 div._2zcEX')]

    for i in range(len(prices)):
        d = prices[i].split("\\ ")
        a = d[0].replace(weights[i], '')
        b = "".join(filter(lambda d: str.isdigit(d) or d == ',', a))
        b = b.replace(',', '.')
        tovar = tovars[i].replace("'", "’")

        with open('tovars' + str(number_file) + '.sql', 'a', encoding='utf-8') as f:
            sql = "INSERT INTO `tovars` " \
                  "(`mag_id`, `kat_id`, `name`, `weight`, `price`) VALUES " \
                  "(" + str(mag_id) + ", " + str(kat_id) + \
                  ", '" + tovar + "', '" + weights[i] + "', " + str(float(b)) + ");"
            f.write(sql + "\n")
        tovar_id += 1
        if tovar_id % 1000 == 0:
            number_file += 1
    print('Товары добавлены.')
