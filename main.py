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
            cidade = soup.find_all('span', class_= ['ad__sc-1f2ug0x-1 cpGpXB sc-jTzLTM ieZUgc'])   
            if valor != '':
                carro.append(valor[1].get_text())
            else:
                carro.append("0")
            carro.append(cidade[1].get_text())
            carros.append(carro)
    print(carros)
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
        txtMarca.send_keys(carro[0])
        txtModelo.send_keys(carro[1])
        txtAno.send_keys(carro[2])
        if carro[3] == "Automático":
            isAutomatico.click()
        if carro[4]=="Hatch":
            isHatch.click()
        elif carro[4] == "Sedã":
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

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36'
}
url = "https://www.olx.com.br/autos-e-pecas/carros-vans-e-utilitarios/estado-es?rs=55&re=69"
links = _scrapper_first_page(url, headers)
carros = _scrapper(links, headers)

#link = https://www.olx.com.br/autos-e-pecas/carros-vans-e-utilitarios/estado-es?rs=55&re=69
#hora da busca: 9:15
# carros = [['FIAT STRADA TREKKING 1.6 16V FLEX CE', 'FIAT', 'Pick-up', '2013', 'Manual', 'Vermelho', '44.990', 'Vila Velha'], 
#           ['RENAULT LOGAN EXPRES. EASYR HI-FLEX 1.6 8V', 'RENAULT', 'Sedã', '2016', 'Manual', 'Branco', '37.500', 'Vitória'], 
#           ['MERCEDES-BENZ C-180 CGI EXC. 1.6/1.6 FLEX TB 16V  AUT.', 'MERCEDES-BENZ', 'Sedã', '2016', 'Automático', 'Preto', '118.000', 'Vitória'], 
#           ['CHEVROLET S10 PICK-UP LS 2.8 TDI 4X2 CD DIES. MEC.', 'CHEVROLET', 'Pick-up', '2013', 'Manual', 'Preto', '92.000', 'Piúma'], 
#           ['CHEVROLET CLASSIC LIFE/LS 1.0 VHC FLEXP. 4P', 'CHEVROLET', 'Sedã', '2015', 'Manual', 'Preto', '32.900', 'Vila Velha'],
#           ['CHEVROLET CLASSIC LIFE/LS 1.0 VHC FLEXP. 4P', 'CHEVROLET', 'Sedã', '2014', 'Manual', 'Azul', '28.500', 'Vila Velha'], 
#           ['MITSUBISHI PAJERO SPORT 2.8 4X4 DIESEL AUT.', 'MITSUBISHI', 'SUV', '2006', 'Automático', 'Prata', '47.900', 'Serra']]

# carros =  [['VOLKSWAGEN', 'VOLKSWAGEN VOYAGE 1.6 MSI FLEX 16V 4P AUT', '2019', 'Manual', 'Sedã','Prata', '49999', 'Vila Velha'], 
# ['FORD', 'FORD KA+ SEDAN 1.0 TIVCT FLEX 4P', '2019', 'Manual', 'Sedã','Prata', '55000', 'Vila Velha'], 
# ['VOLKSWAGEN', 'VOLKSWAGEN VOYAGE TRENDLINE 1.6 T.FLEX 8V 4P', '2018','Manual', 'Sedã', 'Branco', '53900', 'Vitória'], 
# ['CHEVROLET', 'CHEVROLET PRISMA SED. LT 1.4 8V FLEXPOWER 4P AUT.', '2019', 'Automático', 'Sedã', 'Preto', '49990', 'Serra'], 
# ['FORD', 'FORD KA 1.5 SEDAN SE 12V FLEX 4P MEC.', '2020', 'Manual', 'Sedã', 'Cinza', '56900', 'Vila Velha'], 
# ['HYUNDAI', 'HYUNDAI HB20 COMFORT PLUS 1.0 TB FLEX 12V MEC.', '2017', 'Manual', 'Sedã', 'Branco', '55000', 'Colatina'], 
# ['RENAULT','RENAULT LOGAN ZEN FLEX 1.0 12V 4P MEC.', '2020', 'Manual', 'Sedã', 'Branco', '51990', 'Vitória'],
# ['VOLKSWAGEN', 'VOLKSWAGEN VOYAGE 1.6 MSI FLEX 8V 4P', '2020', 'Manual', 'Sedã', 'Branco', '59500', 'Vila Velha'], 
# ['FIAT', 'FIAT CRONOS DRIVE 1.8 16V FLEX AUT', '2020', 'Automático', 'Sedã', 'Cinza', '60000','Serra'], 
# ['CHEVROLET', 'CHEVROLET ONIX SED. PLUS PREM. 1.0 12V TB FLEX AUT', '2020', 'Automático','Sedã', '4 portas', '600', 'Cariacica'],
#  ['FORD', 'FORD KA+ SEDAN 1.0 SEL TICVT FLEX 4P', '2018', 'Manual', 'Sedã', 'Preto', '50000', 'Jaguaré']]

_post(carros)