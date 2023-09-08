import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import requests
from bs4 import BeautifulSoup

#Quando a cor do carro for azul foi definido o valor padrão de "Outro"
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
                        carro.append(a[0].get_text())
                    if(span.get_text()=='Marca'):
                        a = item.find_all('a', class_=['sc-bZQynM fqHmWf'])
                        carro.append(a[3].get_text())
                    if(span.get_text()=='Tipo de veículo'):
                        x = item.find_all('span', class_=['sc-jTzLTM cseqXy'])
                        carro.append(x[0].get_text())
                    if(span.get_text()=='Ano'):
                        a = item.find_all('a', class_=['sc-bZQynM fqHmWf'])
                        carro.append(a[4].get_text())
                    if(span.get_text()=='Câmbio'):
                        x = item.find_all('span', class_=['sc-jTzLTM cseqXy'])
                        carro.append(x[4].get_text())
                    if(span.get_text()=='Cor'):
                        x = item.find_all('span', class_=['sc-jTzLTM cseqXy'])
                        carro.append(x[5].get_text())
            valor = soup.find_all('h2', class_=['ad__sc-12l420o-1 dnbBJL sc-jTzLTM iyLIyP'])   
            valor = valor[1].get_text() 
            valor = valor.replace(".", "")
            cidade = soup.find_all('span', class_= ['ad__sc-1f2ug0x-1 cpGpXB sc-jTzLTM ieZUgc'])   
            if valor != '':
                carro.append(valor)
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
   
    #Cadastrar carros
    for carro in carros:
         #Acessa página de cadastro
        time.sleep(2)
        btnNovo = driver.find_element(By.CLASS_NAME, "btn")
        btnNovo.click()

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

        #Cadastrar carros
        txtMarca.send_keys(carro[1])
        txtModelo.send_keys(carro[0])
        txtAno.send_keys(carro[3])
        if carro[4] == "Automático":
            isAutomatico.click()
        if carro[2]=="Hatch":
            isHatch.click()
        elif carro[2] == "Sedã":
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
            select.select_by_value("outro")
        elif carro[5] == "Rosa":
            select.select_by_value("rosa")
        else:    
            select.select_by_value("outro")
        txtValor.send_keys(carro[6])
        txtMunicipio.send_keys(carro[7])
        btnCadastrar.click()

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36'
}

url = "https://www.olx.com.br/autos-e-pecas/carros-vans-e-utilitarios/estado-es?ctp=9&ctp=8&pe=300000&ps=100000&re=74&rs=66"
# url = "https://www.olx.com.br/autos-e-pecas/carros-vans-e-utilitarios/estado-es?ctp=9&ctp=8&pe=100000&ps=70000&re=74&rs=66"
links = _scrapper_first_page(url, headers)
carros = _scrapper(links, headers)

#link = https://www.olx.com.br/autos-e-pecas/carros-vans-e-utilitarios/estado-es?ctp=9&ctp=8&pe=100000&ps=70000&re=74&rs=66
#hora da busca: 9:45
# carros = [['CHEVROLET CRUZE SPORT LTZ 1.4 16V TB FLEX 5P AUT.', 'CHEVROLET', 'Hatch', '2019', 'Automático', 'Branco', '98.000', 'Linhares'], 
#           ['CHEVROLET HATCH PREM. 1.0 12V TB FLEX 5P AUT', 'CHEVROLET', 'Hatch', '2021', 'Automático', 'Branco', '79.000', 'Vila Velha'], 
#           ['HYUNDAI HB20 PLATINUM 1.0 TB FLEX 12V AUT', 'HYUNDAI', 'Hatch', '2023', 'Automático', 'Azul', '94.000', 'Vitória'], 
#           ['FIAT ARGO TREKKING 1.3 8V FLEX', 'FIAT', 'Hatch', '2022', 'Manual', 'Preto', '78.000', 'Vila Velha'], 
#           ['VOLKSWAGEN VOYAGE 1.0 FLEX 12V 4P', 'VOLKSWAGEN', 'Sedã', '2023', 'Manual', 'Prata', '77.990', 'Vila Velha'], 
#           ['HYUNDAI HB20S EVOLUTION 1.0 FLEX 12V MEC', 'HYUNDAI', 'Sedã', '2021', 'Manual', 'Preto', '74.990', 'Guarapari'], 
#           ['HYUNDAI ELANTRA 2.0 16V FLEX AUT.', 'HYUNDAI', 'Sedã', '2017', 'Automático', 'Branco', '79.900', 'Vila Velha']]

# link = https://www.olx.com.br/autos-e-pecas/carros-vans-e-utilitarios/estado-es?ctp=9&ctp=8&pe=300000&ps=100000&re=74&rs=66
#hora da busca: 9:48
# carros =  [['MERCEDES-BENZ C-180 CGI EXC. 1.6/1.6 FLEX TB 16V  AUT.', 'MERCEDES-BENZ', 'Sedã', '2016', 'Automático', 'Preto', '118.000', 'Vitória'], 
#            ['TOYOTA 2.0 XEI 16V FLEX 4P AUTOMATICO', 'TOYOTA', 'Sedã', '2019', 'Automático', 'Cinza', '105.990', 'Vila Velha'], 
#            ['AUDI A3 SEDAN PRESTIGE PLUS 1.4 TFSI S-TRONIC', 'AUDI', 'Sedã', '2019', 'Automático', 'Branco', '100.000', 'Vila Velha'], 
#            ['BMW 120IA SPORT 2.0 ACTIVEFLEX 16V AUT.', 'BMW', 'Hatch', '2016', 'Automático', 'Cinza', '108.500', 'Vila Velha'], 
#            ['TOYOTA COROLLA ALTIS HYBRID 1.8 16V FLEX AUT.', 'TOYOTA', 'Sedã', '2022', 'Automático', 'Cinza', '157.990', 'Serra'], 
#            ['HONDA CIVIC SEDAN EX 2.0 FLEX 16V AUT.4P', 'HONDA', 'Sedã', '2017', 'Automático', 'Branco', '104.990', 'Vila Velha'], 
#            ['TOYOTA COROLLA XEI 2.0 FLEX 16V AUT.', 'TOYOTA', 'Sedã', '2019', 'Automático', 'Branco', '110.000', 'Guarapari']]

_post(carros)