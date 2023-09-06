import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
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
    if len(links) > 0:
        for link in links:
            carro=[]
            data = requests.get(link, headers=headers)
            soup = BeautifulSoup(data.content, 'html.parser')
            div = soup.find_all('div', class_=['sc-chPdSV dkrALZ'])
            for item in div:
                span = item.find_all('span', class_=['sc-bZQynM eVkVTv'])
                if(span[0].get_text()=='Modelo'):
                    a = item.find_all('a', class_=['sc-EHOje bKbCBo'])
                    carro.append(a[0].get_text())
                if(span[0].get_text()=='Marca'):
                    a = item.find_all('a', class_=['sc-EHOje bKbCBo'])
                    carro.append(a[0].get_text())
                if(span[0].get_text()=='Tipo de veículo'):
                    x = item.find_all('span', class_=['sc-bZQynM bBPxWM'])
                    carro.append(x[0].get_text())
                if(span[0].get_text()=='Ano'):
                    a = item.find_all('a', class_=['sc-EHOje bKbCBo'])
                    carro.append(a[0].get_text())
                if(span[0].get_text()=='Câmbio'):
                    x = item.find_all('span', class_=['sc-bZQynM bBPxWM'])
                    carro.append(x[0].get_text())
                if(span[0].get_text()=='Cor'):
                    x = item.find_all('span', class_=['sc-bZQynM bBPxWM'])
                    carro.append(x[0].get_text())
            valor = soup.find_all('h2', class_=['ad__sc-12l420o-1 dnbBJL sc-bZQynM jyLhNn'])    
            cidade = soup.find_all('span', class_= ['ad__sc-1f2ug0x-1 cpGpXB sc-bZQynM KhQwW'])   
            if valor != '':
                carro.append(valor[1].get_text())
            else:
                carro.append("0")
            carro.append(cidade[1].get_text())
            carros.append(carro)
    return carros

def _post(carros):
    driver = webdriver.Firefox()
    driver.get("http://weka.inf.ufes.br/IFESTP/login.php")
    time.sleep(2)
    #Realizar login
    login = driver.find_element(By.ID, "username")
    senha = driver.find_element(By.ID, "password")
    login.send_keys("Peaga")
    senha.send_keys("guilherme_play")
    btnLogin = driver.find_element(By.NAME, "submit")
    btnLogin.click()
    time.sleep(2)
    #Acessa página de cadastro
    btnNovo = driver.find_element(By.CLASS_NAME, "btn")
    btnNovo.click()
    time.sleep(2)
    #Adiciona veiculo
    txtMarca = driver.find_element(By.ID, "marca")

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36'
}
url = "https://www.olx.com.br/autos-e-pecas/carros-vans-e-utilitarios/estado-es?rs=55&re=69"
links = _scrapper_first_page(url, headers)
carros = _scrapper(links, headers)
_post(carros)