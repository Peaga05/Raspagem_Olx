import selenium
import requests
from bs4 import BeautifulSoup


def _scrapper_first_page(url, headers):
    links = []
    data = requests.get(url, headers=headers)
    soup = BeautifulSoup(data.content, 'html.parser')
    a = soup.find_all('a', class_=['sc-dJjYzT dOvWTZ'])
    for href in a:
        links.append(href.get('href'))
    return links
        
def _scrapper(links, headers):
    carros = []
    if links.len > 0:
        for link in links:
            carro=[]
            data = requests.get(link, headers=headers)

def _post():
    print("Olá")

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36'
}
url = "https://www.olx.com.br/autos-e-pecas/carros-vans-e-utilitarios/seda/estado-es/norte-do-espirito-santo?me=40000&pe=60000&rs=65"
links = _scrapper_first_page(url, headers)
_scrapper(links, headers)