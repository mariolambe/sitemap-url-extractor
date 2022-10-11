keyword= 'black friday'#@param {type:"string"} 
# change the keyword to whatever you want, for example keyword = 'best backlinks'


# Optional parameters
language = 'en' #@param {type:"string"} # english => you can use it in another languages, for example with language = 'es'
country = 'us' # United States => use for example country = 'uk' for United Kingdom
scrapeLevels = 2  # Si quieres más resultados usa 2. A partir de 3 necesitarás proxies...
loopPAA = False # False makes the loop thru related searches // True makes the loop thru PAA



urlInicial = f"https://www.google.com/search?hl={language}&gl={country}&q={keyword}&oq={keyword}"

scrapeado = []
contadorPreguntas = []
contadorBusquedas = []
contadorSuggest = []

googleHasHuntedUs = False

# we install dependencies
!pip install treelib
!pip install pyOpenSSL==22.0.0
!pip install selenium-wire
from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
!apt update
!apt install chromium-chromedriver

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument("user-agent=Mozilla/5.0")
options.add_argument("--window-size=1366,768")#360,851

from treelib import Node, Tree
from bs4 import BeautifulSoup
import requests
import random

# we start selenium
wd = webdriver.Chrome(options=options)

# General function => be careful with infinite loops it calls to itself
def busquedaGlobal(busquedasX, level):
  if googleHasHuntedUs: return
  print("--------------------------")
  print(f"         Level {level}")
  print("--------------------------")

  subBusquedasRelacionadas = []
  
  for busqueda in busquedasX:
    subBusquedas = busquedaIndividual(busqueda, level+1)
    subBusquedasRelacionadas.extend(subBusquedas)
  
  if level < scrapeLevels:
    busquedaGlobal(subBusquedasRelacionadas, level +1) # be carefull with infinite loops

# Individual function to scrap each SERP
def busquedaIndividual(busqueda0X, level):
  busqueda0 = busqueda0X[0]
  url0 = busqueda0X[1] # option url0 = f"https://www.google.com/search?hl={language}&gl={country}&q={busqueda0}&oq={busqueda0}"
  
  global  googleHasHuntedUs
  if busqueda0.lower() in scrapeado or googleHasHuntedUs == True: return []
  
  preguntas = []
  busquedas = []
  
  tree = Tree() # Tree graph to represent the querie and its related searches, People also ask and google suggest
  tree.create_node(busqueda0, busqueda0.lower())  # root node        
    
  wd.get(url0) # navigate to the url
  
  if ("URL: https://www.google.com/search?" in wd.page_source): # Checking if google has huaunted us
    googleHasHuntedUs = True

    if level == 1:
      print("---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------")
      print("Sorry Google has hunted the IP, to continue scraping delete the runtime environment (In the menu, Runtime environment/disconnect and delete...) or make a copy of this colab (file/save a copy on drive) and hit play again")
      print("---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------")
    else:
      print("Google ens Roba, digo... Sorry Google has haunted us, end of scrapping for this keyword")
    
    return []

  if level == 1:
    acepto = wd.find_elements(by=By.CSS_SELECTOR, value="input[value='I agree']")
    if len(acepto) > 0:
      acepto[0].click() 

  comienza = random.randint(100, 500)/1000 # let's put a little random wait
  time.sleep(comienza)
  
  # retrieve People also asks (PAA)
  PAA = wd.find_elements(by=By.CSS_SELECTOR, value="[class='xpc']") 
  if len(PAA) > 0 : tree.create_node("Related Questions", "Related Questions" , parent= busqueda0.lower())
  for boton in PAA:
    enlaces = boton.find_elements(by=By.TAG_NAME, value="a")
    for enlace in enlaces:
      href = enlace.get_attribute('href')
      if "/search" in href:
        contadorPreguntas.append(boton.text.strip().lower())
        if boton.text.strip() in tree: continue
        try:
          tree.create_node(boton.text.strip(), boton.text.strip().lower(), parent= "Related Questions")
        except:
          continue # in some exceptional cases the text is to long to add it to the tree 
        preguntas.append([boton.text.strip(), href])

  # we retrive related searches
  busquedasRelacionadas = wd.find_elements(by=By.CSS_SELECTOR, value=".Q71vJc") 
  if len(busquedasRelacionadas) > 0: tree.create_node("Related Searches", "Related Searches" , parent= busqueda0.lower())

  for busqueda in busquedasRelacionadas:
    contadorBusquedas.append(busqueda.text.strip().lower())
    if busqueda.text.strip() in tree: continue
    try:
      tree.create_node(busqueda.text.strip().lower(), busqueda.text.strip().lower(), parent="Related Searches")
    except:
      continue
    busquedas.append([busqueda.text.strip(), busqueda.get_attribute('href')] )

  # Get google suggest
  sugeridos = suggest(busqueda0)
  sugeridos = [x for x in sugeridos if x !=busqueda0 and x.lower() not in tree]
  if len(sugeridos) > 0 : tree.create_node("Google Suggest", "Google Suggest" , parent= busqueda0.lower())

  for sugerido in sugeridos:
    contadorSuggest.append(sugerido.lower())
    try:
      tree.create_node(sugerido, sugerido.lower(), parent="Google Suggest")
    except:
      continue
    
  if len(tree) > 1: tree.show(key=False)

  scrapeado.append(busqueda0.lower()) # control to avoid repeating queries

  if loopPAA: return preguntas # option to return People Also Ask
  return busquedas # The default option is to return related searches for the loop
 
# function to retrieve data from google suggest
def suggest(key):
  r = requests.get(f'http://suggestqueries.google.com/complete/search?output=toolbar&hl={language}&gl={country}&q={key}')
  soup = BeautifulSoup(r.content, 'html.parser')
  sugg = [sugg['data'] for sugg in soup.find_all('suggestion')]
  return sugg
    
      
# Here we start all => Vaaamooooooosss
busquedaGlobal([[keyword, urlInicial]], 0)

# result tables
from collections import Counter # contador para mostrar en tabla
contadorPreguntas1 = [list(x) for x in Counter(contadorPreguntas).most_common()]
contadorBusquedas1 = [list(x) for x in Counter(contadorBusquedas +contadorSuggest ).most_common()]


import pandas as pd
from google.colab import data_table
# I use a function to display tables
def pasarATabla(lista,columnas):
  lista = pd.DataFrame (lista, columns = columnas )
  lista = data_table.DataTable(lista, include_index=True, num_rows_per_page=20)
  display(lista)

if len(contadorBusquedas1) > 0:
  print("-----------------------------------------")
  print("May the Force be with you young Skywalker")
  print("----------------------------------------------------------------")
  print(f"If you want to get more results try with scrapeLevels = {scrapeLevels+1}")
  print("----------------------------------------------------------------")
  pasarATabla(contadorBusquedas1, ["Related Searches", "Relevance"])

if len(contadorPreguntas1) > 0:
  pasarATabla(contadorPreguntas1, ["Related Questions", "Relevance"])
