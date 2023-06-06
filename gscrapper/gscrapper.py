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
from selenium.webdriver.chrome.options import Options

import json
import re

def get_categorias_txt(file) -> list[str]:
    with open(file, "r") as f:
        return [link.strip().strip("\n") for link in f.readlines()]

def filter_categorias(categorias) -> list[str]:
    """ Filter category links. """
    
    # Add Filter: */ , /conteudo , *p-* , *growth-supplements* , full-link
    fcategorias = []
    for categoria in categorias:
        if re.search('/$', categoria) and \
        not re.search('conteudo', categoria) and \
        categoria != "https://www.gsuplementos.com.br/":
            fcategorias.append(categoria)

    return fcategorias


def get_categorias(driver, wait) -> list[str]:
    """ Returns a list of links to all categories. """

    driver.get("https://www.gsuplementos.com.br")
    link_categorias = wait.until(lambda d: d.find_element(By.ID, 'menu-Categorias'))
    lista_categorias = link_categorias.find_element(By.XPATH, 'following-sibling::ul')
    categorias = lista_categorias.find_elements(By.TAG_NAME, 'a')
    categorias = [categoria.get_attribute('href') for categoria in categorias]
    return filter_categorias(categorias)

def get_link_produtos(wait) -> list[str]:
    produtos = []
    produtos_div = wait.until(lambda d: d.find_elements(By.CLASS_NAME, 'categoriaProdItem'))
    for produto in produtos_div:
        produto_link = produto.find_element(By.TAG_NAME, 'a').get_attribute('href')
        produtos.append(produto_link)

    return produtos


def get_produtos(categoria, driver, wait) -> list[str]:
    """ Returns a list of links to all products of a given category. """

    print(f"Getting {categoria} products...")
    driver.get(categoria)
    produtos = get_link_produtos(wait)
    try:
        proxima_button = wait.until(lambda d: d.find_element(By.CLASS_NAME, 'proxima'))
        driver.execute_script("arguments[0].scrollIntoView();", proxima_button)
        while "disabled" not in proxima_button.get_attribute('class'):
            next_link = proxima_button.get_attribute('onclick').split('=')[1][1:-1]
            driver.get(next_link)
            produtos += get_link_produtos(wait)
            proxima_button = wait.until(lambda d: d.find_element(By.CLASS_NAME, 'proxima'))
    except TimeoutException:
        pass

    return produtos

def get_product_details(product, driver, wait) -> dict:
    """ Given a product, returns it's characteristics. """

    print(f"\tGetting {product}")
    driver.get(product)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    nome = soup.find('h1')
    nome = str(nome.string) if nome else None
    if not nome:
        print(f"\t\t[ERRO] Nao possui nome")
        return
    nome = nome.strip().strip('\n')
    preco = str(soup.find('gs-custom', attrs={"data-desconto-boleto-valor":""}).string)
    hash = soup.find(id='finalizarCompra')
    hash = "00" if not hash else hash['data-hash']
    opcoes = {}
    options = soup.find('select')
    options = options.find_all('option') if options else None
    if options:
        for op in options:
            opcoes[str(op.string)] = op['value']

    return {
        "nome": nome,
        "preco": preco,
        "hash": hash,
        "opcoes": opcoes
    }

def link_to_category(link) -> str:
    """ Transforms a category link into a readable format. """

    return link.split('/')[-2]

def link_to_product(link) -> str:
    """ Transforms a product link into a readable format. """

    return link.split('/')[-1]


options = Options()
options.page_load_strategy = 'eager'
options.add_argument('--headless=new')
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)
wait = WebDriverWait(driver, timeout=10)



# categorias = get_categorias(driver, wait)
categorias = get_categorias_txt("categorias")
db = {}
for categoria in categorias:
    produtos = get_produtos(categoria, driver, wait)
    category_name = link_to_category(categoria)
    db[category_name] = {}
    for produto in produtos:
        details = get_product_details(produto, driver, wait)
        product_name = link_to_product(produto)
        db[category_name][product_name] = details

# Save to file
with open("db.json", "w") as f:
    f.write(json.dumps(db))

