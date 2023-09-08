import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
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
            div = soup.find_all('div', class_=['sc-brqgnP ad__sc-1g2w54p-1 buMtQZ'])
            for item in div:
                elemnt = item.find_all('span', class_=['sc-jTzLTM huxyns'])
                for span in elemnt:
                    if(span.get_text()=='Modelo'):
                        a = item.find_all('a', class_=['sc-bZQynM fqHmWf'])
                        print(a[0])
                        carro.append(a[0].get_text())
                    if(span.get_text()=='Marca'):
                        a = item.find_all('a', class_=['sc-bZQynM fqHmWf'])
                        print(a)
                        carro.append(a[0].get_text())
                    if(span.get_text()=='Tipo de veículo'):
                        x = item.find_all('span', class_=['sc-jTzLTM cseqXy'])
                        print(x)
                        carro.append(x[0].get_text())
                    if(span.get_text()=='Ano'):
                        a = item.find_all('a', class_=['sc-bZQynM fqHmWf'])
                        print(a)
                        carro.append(a[0].get_text())
                    if(span.get_text()=='Câmbio'):
                        x = item.find_all('span', class_=['sc-jTzLTM cseqXy'])
                        print(x)
                        carro.append(x[0].get_text())
                    if(span.get_text()=='Cor'):
                        x = item.find_all('span', class_=['sc-jTzLTM cseqXy'])
                        print(x)
                        carro.append(x[0].get_text())
            print(carro)
            valor = soup.find_all('h2', class_=['ad__sc-12l420o-1 dnbBJL sc-jTzLTM iyLIyP'])    
            cidade = soup.find_all('span', class_= ['ad__sc-1f2ug0x-1 cpGpXB sc-jTzLTM ieZUgc'])   
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
    #Capturar os campos de cadastro
    txtMarca = driver.find_element(By.ID, "marca")
    txtModelo = driver.find_element(By.ID, "modelo")
    txtAno = driver.find_element(By.ID, "ano")
    txtValor = driver.find_element(By.ID, "valor")
    txtMunicipio = driver.find_element(By.ID, "municipio")
    isAutomatico = driver.find_element(By.ID, "cambioAutomatico")
    isHatch = driver.find_element(By.ID, "c_hatch")
    isSedan = driver.find_element(By.ID, "c_sedan")
    selectBox = driver.find_element(By.ID, "cor")
    select = Select(selectBox)
    btnCadastrar = driver.find_element(By.NAME, "insert")
    for carro in carros:
        time.sleep(2)
        print(carro)
        txtMarca.send_keys(carro[0])
        txtModelo.send_keys(carro[1])
        txtAno.send_keys(carro[2])
        if carro[3] == "Automático":
            isAutomatico.click()
        if carro[4]=="Hatch":
            isHatch.click()
        elif carro[4] == "Sedan":
            isSedan.click()
        if carro[5] == "Branco":
            select.select_by_value("branco")
        elif carro[5] == "Preto":    
            select.select_by_value("preto")
        elif carro[5] == "Prata":    
            select.select_by_value("prata")
        elif carro[5] == "Vermelho":    
            select.select_by_value("vermelho")
        elif carro[5] == "Verde":    
            select.select_by_value("verde")
        elif carro[5] == "Azul":    
            select.select_by_value("azul")
        elif carro[5] == "Rosa":
            select.select_by_value("rosa")
        else:    
            select.select_by_value("outro")
        txtValor.send_keys(carro[6])
        txtMunicipio.send_keys(carro[7])
        btnCadastrar.click()
        btnNovo = driver.find_element(By.CLASS_NAME, "btn")
        btnNovo.click()
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36'
}
url = "https://www.olx.com.br/autos-e-pecas/carros-vans-e-utilitarios/estado-es?rs=55&re=69"
# links = _scrapper_first_page(url, headers)
# carros = _scrapper(links, headers)
carros = [['FORD', 'FORD KA 1.5 SE PLUS 12V FLEX 5P MEC.', '2020', 'Manual', 'Hatch', 'Branco','59900', 'Serra'], 
['HYUNDAI', 'HYUNDAI HB20 SENSE 1.0 FLEX 12V MEC', '2018', 'Manual', 'Hatch','Branco', '55850', 'Serra'], 
['VOLKSWAGEN', 'VOLKSWAGEN FOX CONNECT 1.6 FLEX 8V 5P', '2019', 'Manual','Hatch', 'Branco', '58000', 'Serra'], 
['CHEVROLET', 'CHEVROLET ONIX HATCH JOY 1.0 8V FLEX 5P MEC.',
'2020', 'Manual', 'Hatch', 'Branco', '56600', 'Vila Velha'], 
['VOLKSWAGEN', 'VOLKSWAGEN FOX CONNECT 1.6 FLEX 8V 5P', '2018', 'Manual', 'Hatch', 'Branco', '58000', 'Serra'], 
['HYUNDAI', 'HYUNDAI HB20 COMF./C.PLUS/C.STYLE 1.0 FLEX 12V', '2018', 'Manual', 'Hatch', 'Preto', '56900', 'Serra'], 
['CHEVROLET','CHEVROLET ONIX HATCH LT 1.0 8V FLEXPOWER 5P MEC.', '2019', 'Manual', 'Hatch', 'Prata', '57500','Cariacica'], 
['VOLKSWAGEN', 'VOLKSWAGEN FOX CONNECT I MOTION 1.6 FLEX 8V 5P', '2019', 'Automático', 'Hatch', 'Preto', '56900', 'Linhares'], 
['FIAT', 'FIAT ARGO DRIVE 1.0 6V FLEX', '2020', 'Manual','Hatch', 'Prata', '59900', 'Serra'], 
['FORD', 'FORD KA 1.5 SE PLUS 12V FLEX 5P MEC.', '2020', 'Manual','Hatch', 'Branco', '57900', 'Vila Velha'], 
['HYUNDAI', 'HYUNDAI HB20 UNIQUE 1.0 FLEX 12V MEC.', '2019','Branco', 'Hatch', '4 portas', '57000', 'Vila Velha']]
_post(carros)