import requests
from xml.etree import ElementTree
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.common.exceptions import (ElementClickInterceptedException,
                                        TimeoutException)
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.relative_locator import locate_with
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

from pprint import pprint

# # Get sitemap 
# response = requests.get("https://www.gsuplementos.com.br/xml/sitemap-categorias.xml")
# XML_Tree = ElementTree.fromstring(response.content)
# urls = [child[0].text for child in XML_Tree]
# urls = urls[1:]
# print(urls)


service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)
wait = WebDriverWait(driver, timeout=10)

driver.get("https://www.gsuplementos.com.br")
link_categorias = wait.until(lambda d: d.find_element(By.ID, 'menu-Categorias'))
lista_categorias = link_categorias.find_element(By.XPATH, 'following-sibling::ul')
categorias = lista_categorias.find_elements(By.TAG_NAME, 'a')
categorias = [categoria.get_attribute('href') for categoria in categorias]
# Add Filter: */ , /conteudo , *p-* , *growth-supplements*
# TODO reimplementar usando regex
fcategorias = []
for categoria in categorias:
    if categoria[-1] == '/' and categoria != 'https://www.gsuplementos.com.br/':
        fcategorias.append(categoria)
with open('categorias.txt', 'w') as f:
    for categoria in fcategorias:
        f.write(f"{categoria}\n")

db = {}
categorias = categorias[:5]
for categoria in categorias:
    driver.get(categoria)
    try:
        produtos = wait.until(lambda d: d.find_elements(By.CLASS_NAME, 'categoriaProdItem'))
        db[categoria] = {}
        for produto in produtos:
            try:
                link_produto = produto.find_element(By.TAG_NAME, 'a').get_attribute('href')
                db[categoria][link_produto] = {}
            except TimeoutException:
                pass
    except TimeoutException:
        pass

pprint(db)
