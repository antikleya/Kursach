import requests
from bs4 import BeautifulSoup
from time import sleep
from random_user_agent.user_agent import UserAgent

user_agent_rotator = UserAgent()

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    'User-Agent': user_agent_rotator.get_random_user_agent()
}


def parse_router_page(url, f):
    resp = requests.get(url, params=headers)
    if resp.status_code == 200:
        soup = BeautifulSoup(resp.text, features="html.parser")
        params = {'Частоты Wi-Fi:': 'frequencies', 'Стандарты Wi-Fi 802.11:': 'wifi_standard', 'Порты:': 'ports'}
        res = {}
        specifications = soup.find_all('div', class_='Specifications__row')

        for spec in specifications:
            tmp = spec.contents[0].text.strip()
            if tmp in params:
                res[params[tmp]] = spec.contents[1].text.strip()

        res['price'] = int(soup.find('span', class_='ProductHeader__price-default_current-price')
                           .text.strip().replace(' ', ''))
        name = soup.find('h1', class_='ProductHeader__title').text.strip().split(',')[0]
        res['model'] = ' '.join(name.split()[2:])
        if len(res.keys()) == 5:
            f.write(f"{res['price']};{res['model']};{res['frequencies']};{res['wifi_standard']};{res['ports']}\n")
    else:
        print('Error', url, resp.status_code)
        f.close()
        exit()
    sleep(1)


def parse_router_list(url, f):
    resp = requests.get(url, params=headers)
    if resp.status_code == 200:
        soup = BeautifulSoup(resp.text, features="html.parser")
        links = soup.find_all('a', class_="ProductCardVertical__name")
        for link in links:
            parse_router_page('https://www.citilink.ru' + link['href'], f)
    else:
        print('Error', url, resp.status_code)
        f.close()
        exit()


def parse_routers():
    urls = ['https://www.citilink.ru/catalog/wi-fi-routery-marshrutizatory/']

    for url in urls:
        f = open('scraped/routers.txt', 'w')
        parse_router_list(url, f)
        f.close()

    return 1


def parse_cpu():
    url = 'https://www.citilink.ru/catalog/processory/'
    f = open('scraped/cpu.txt', 'w')

    resp = requests.get(url, params=headers)
    if resp.status_code == 200:
        soup = BeautifulSoup(resp.text, features="html.parser")
        names = soup.find_all('a', class_="ProductCardHorizontal__title")
        prices = soup.find_all('span', class_="ProductCardHorizontal__price_current-price")
        for i in range(len(names)):
            f.write(f"{' '.join(names[i].text.split(',')[0].split()[2:])};{''.join(prices[i].text.strip().split())}\n")
    else:
        print('Error', url, resp.status_code)
        return 0

    f.close()
    return 1


def parse_ram():
    url = 'https://www.citilink.ru/catalog/moduli-pamyati/'
    f = open('scraped/ram.txt', 'w')

    resp = requests.get(url, params=headers)
    if resp.status_code == 200:
        soup = BeautifulSoup(resp.text, features="html.parser")
        names = soup.find_all('a', class_="ProductCardVertical__name")
        prices = soup.find_all('span', class_="ProductCardVerticalPrice__price-current_current-price")
        for i in range(len(names)):
            f.write(f"{' '.join(names[i].text.split(',')[0].split()[2:])};{''.join(prices[i].text.strip().split())}\n")
    else:
        print('Error', url, resp.status_code)
        return 0

    f.close()
    return 1


def finalize(filename):
    inp = open(f'scraped/{filename}.txt', 'r')
    out = open(f'scraped/{filename}', 'w')
    lines = inp.readlines()[:-1]
    for line in lines:
        out.write(line)
    inp.close()
    out.close()


if __name__ == '__main__':
    cpu_code = parse_cpu()
    if cpu_code:
        finalize('cpu')

    ram_code = parse_ram()
    if ram_code:
        finalize('ram')

    # router_code = parse_routers()
    # if not router_code:
    #     finalize('router')
