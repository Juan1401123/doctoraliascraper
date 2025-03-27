import re
import time
from colorama import Fore
import openpyxl
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options
import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import StaleElementReferenceException
import random
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import NoSuchElementException
import math

enlinea='NO'#NO O SI
Zona='Ciudad de México'# Verificar bien la escritura
Especialidad='Pediatra'
top=25
start_page=3

listaespecialidades=pd.read_csv('listaespecialidades.csv')
listaespecialidades1=pd.read_csv('especialidades1.csv')
listaciudades=pd.read_csv('listaciudades.csv')

options = Options()

options.add_argument('--disable-application-cache')
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_argument("--disable-cookies")
options.add_argument("--disable-extensions")
options.add_argument('--no-sandbox')
options.add_argument("--disable-extensions")
options.add_argument("start-maximized")
options.add_argument('--disable-gpu')
# options.add_argument("--headless")  
# options.add_argument("--disable-gpu")
options.add_argument("--disable-dev-shm-usage")
options.add_argument('--ignore-urlfetcher-cert-requests')
options.add_argument('--no-first-run')
options.add_argument("--disable-popup-blocking") 
driver = webdriver.Chrome(options=options)

driver.get('https://www.doctoralia.com.mx/')

if len(driver.find_elements(By.CSS_SELECTOR,'#footer > div.row.m-0.w-100.floating-cookie-info > div > div > div > div > div.floating-cookie-info-btn > button'))>=1:
    try:
      closewindow=driver.find_element(By.CSS_SELECTOR,'#footer > div.row.m-0.w-100.floating-cookie-info > div > div > div > div > div.floating-cookie-info-btn > button')
      closewindow.click()
    except NoSuchElementException:
       pass


urls_toscrap=[]


time.sleep(2)
if enlinea=='NO':
  inputciudad=driver.find_element(By.CSS_SELECTOR,'#search > div > div > div.city-col.mb-1.mb-md-0.col-12.col-md-5 > div > div.dropdown-toggle > div > i > svg')
  inputciudad.click()
  time.sleep(.5)
  vermas=driver.find_element(By.CSS_SELECTOR,'#search > div > div > div.city-col.mb-1.mb-md-0.col-12.col-md-5 > div > div.dropdown-menu.show > ul > div > div')
  vermas.click()
  inputsciudad=driver.find_elements(By.XPATH,'/html/body/section[1]/div[2]/div/div/div[1]/div[2]/div[1]/div/div/div/div[2]/div/div[2]/ul/div/li')
  lugaresdeciudad=int(listaciudades[listaciudades['ciudades']==Zona]['indice'].values)
  inputsciudad[lugaresdeciudad].click()
  time.sleep(1)
  todasesp=driver.find_element(By.CSS_SELECTOR,'#search > div > div > div.specialists-col.mb-1.mb-md-0.col-12.col-md-5 > div > div.dropdown-menu.show > ul > div > div.dropdown-item.d-flex.justify-content-center')
  todasesp.click()
  time.sleep(.5)
  especialidadnum=int(listaespecialidades1[listaespecialidades1['Especialidad']==Especialidad]['indice'].values)
  inputs1=driver.find_elements(By.XPATH,'/html/body/section[1]/div[2]/div/div/div[1]/div[2]/div[1]/div/div/div/div[1]/div/div[2]/ul/div/div[1]/a')
  inputs1[especialidadnum].click()
  time.sleep(1)
  search1=driver.find_element(By.CSS_SELECTOR,'#search > div > div > div.button-col.col-12.col-md-2 > button')
  search1.click()
elif enlinea=='SI':
  clickenlinea=driver.find_element(By.CSS_SELECTOR,'#homepage-search > div.d-flex.align-items-center.pt-1.mb-1.navigation.nav.text-left > a.btn.btn-lg.ml-0-5')
  clickenlinea.click()
  time.sleep(.5)
  input2=driver.find_element(By.CSS_SELECTOR,'#homepage-search > div.tab-content > div.tab-pane.active > div > div.col-md-10.col-12.dropdown-col > div > div > div.multiselect__caret-wrapper')
  input2.click()
  time.sleep(.5)
  inputs2=driver.find_elements(By.CLASS_NAME,'multiselect__element')
  lugarespecialidad2=int(listaespecialidades[listaespecialidades['Especialidad']==Especialidad]['indice'].values)
  inputs2[lugarespecialidad2].click()
  time.sleep(.5)
  search=driver.find_element(By.CSS_SELECTOR,'#homepage-search > div.tab-content > div.tab-pane.active > div > div.col-md-2.col-12.button-col > button')
  search.click()
else:
  print('elige si es en linea escribe SI o NO en mayusculas')


pagecounter=1
while pagecounter<start_page:
 driver.execute_script(f"window.scrollBy(0, {15500});")
 if driver.find_elements(By.CLASS_NAME,'page-item')[len(driver.find_elements(By.CLASS_NAME,'page-item'))-1].text=='Siguiente':
  nextpage=driver.find_elements(By.CLASS_NAME,'page-item')[len(driver.find_elements(By.CLASS_NAME,'page-item'))-1]
  nextpage.click()
 pagecounter+=1   
desicion=1
while desicion==1:
 time.sleep(2)
 page=BeautifulSoup(driver.page_source,'html.parser')
 doctorecard=page.find_all('li',class_='has-cal-active')
 driver.execute_script(f"window.scrollBy(0, {15500});")
 for a in doctorecard:
    try:
      doctorecard=page.find_all('li',class_='has-cal-active')
      for a in doctorecard:
        urlpre=a.find('h3')
        urls_toscrap.append(urlpre.find('a')['href'])
    except AttributeError:
      print('no se encuentran doctores con esa especialidad.')
 
 if driver.find_elements(By.CLASS_NAME,'page-item')[len(driver.find_elements(By.CLASS_NAME,'page-item'))-1].text=='Siguiente':
  nextpage=driver.find_elements(By.CLASS_NAME,'page-item')[len(driver.find_elements(By.CLASS_NAME,'page-item'))-1]
  nextpage.click()
  if pd.DataFrame(urls_toscrap)[0].nunique()>=top:
    desicion=0 
  print(pd.DataFrame(urls_toscrap)[0].nunique())
 else:
   desicion=0



driver.quit()


listaurls=list(pd.DataFrame(urls_toscrap)[0].unique())

name=[]
especialidad=[]
rating=[]
direccion=[]
numerotel=[]
urls=[]
clinica=[]
residencia=[]
formacion=[]
linkedinurl=[]
facebookurl=[]
precio=[]


driver = webdriver.Chrome(options=options)


wait = WebDriverWait(driver, 10)


for i, e in enumerate(listaurls[:top]):
    numerostel = []
    try:
        old_url = driver.current_url
        driver.get(e)
        time.sleep(1)

        # Esperar a que la página realmente cargue
        attempts = 0
        max_attempts = 5
        while attempts < max_attempts:
            if driver.current_url != old_url:
                break  # Página cargada con éxito

            print(f"Intento {attempts+1} de cargar: {e}")
            driver.get(e)
            time.sleep(2)
            attempts += 1

        # Si no cambia de página, reiniciar WebDriver
        if driver.current_url == old_url:
            print(f"⚠️ ¡No cambia de página! Reiniciando el navegador...")
            driver.quit()
            driver = webdriver.Chrome(options=options)

        urls.append(e)

        # Esperar a que el cuerpo de la página cargue
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )

        page = BeautifulSoup(driver.page_source, 'html.parser')

        # Extraer nombre
        try:
            nombre = page.find('span', {'itemprop': 'name'})
            name.append(nombre.text.strip() if nombre else None)
        except:
            name.append(None)

        # Extraer precios
        try:
            todosprecios = page.find('div', attrs={"data-id": "services-list-container"})
            antesprecio = todosprecios.find('div', class_='mr-1').text
            if antesprecio:
                precio.append(antesprecio.replace('\t', '').replace('\n', '').replace('Desde', '').strip())
            else:
                precio.append(None)
        except:
            precio.append(None)

        # Extraer especialidad
        try:
            especiality = page.find('h2').find('span').find('a').text
            especialidad.append(especiality.strip() if especiality else None)
        except:
            especialidad.append(None)

        # Extraer rating
        try:
            calificacion_elem = page.find('u', class_='rating rating-md unified-doctor-header-info__rating-text')
            if calificacion_elem:
                calificacion = calificacion_elem.get('data-score', None)
                numopiniones = calificacion_elem.text.replace('\n', '')
                rating.append(f"{calificacion} {numopiniones}" if calificacion else None)
            else:
                rating.append(None)
        except:
            rating.append(None)

        # Extraer dirección
        try:
            direccion_elem = page.find("span", {"itemprop": "streetAddress"})
            direccion.append(direccion_elem.text.replace('\n', '').replace('\t', '') + ' ' + Zona if direccion_elem else None)
        except:
            direccion.append(None)

        # Extraer clínica
        try:
            clinica_elem = page.find('span', class_='font-weight-bold')
            clinica.append(clinica_elem.text if clinica_elem else None)
        except:
            clinica.append(None)

        # Reducir zoom para mejorar detección de botones
        driver.execute_script("document.body.style.zoom='25%'")
        time.sleep(1)

        # Extraer información adicional
        try:
            btres = driver.find_element(By.CSS_SELECTOR, 'button[class="btn btn-light btn-lg btn-block mt-1"]')
            btres.click()
            time.sleep(.5)
            preresidencia, preformacion, prelinkedin, prefecebook = None, None, None, None
            for c in driver.find_elements(By.CSS_SELECTOR, '#about-section > div.modal.fade.modal-scrollable.show > div > div > div.modal-body > div'):
                if 'Residencia' in c.text:
                    preresidencia = c.text
                elif 'Formación' in c.text:
                    preformacion = c.text
                elif 'Redes sociales' in c.text:
                    preredes = c.find_elements(By.TAG_NAME, "a")
                    for d in preredes:
                        if 'Linkedin' in d.text:
                            prelinkedin = d.get_attribute("href")
                        elif 'Facebook' in d.text:
                            prefecebook = d.get_attribute("href")
            residencia.append(preresidencia if preresidencia else None)
            formacion.append(preformacion if preformacion else None)
            linkedinurl.append(prelinkedin if prelinkedin else None)
            facebookurl.append(prefecebook if prefecebook else None)
        except:
            residencia.append(None)
            formacion.append(None)
            linkedinurl.append(None)
            facebookurl.append(None)

        # Hacer clic en la página para evitar bloqueos
        driver.execute_script("document.elementFromPoint(200, 300).click();")
        time.sleep(1)

        # Extraer teléfonos
        try:
            botones_tel = driver.find_elements(By.CSS_SELECTOR, 'a[role="button"].text-muted[data-doctor-stats="contact"]')
            for boton in botones_tel:
                if boton.text == 'Mostrar número':
                    boton.click()
                    WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, 'a.text-muted.pl-2[data-patient-app-selector="patient-app-event"]'))
                    )
                    time.sleep(.5)
                    prenumbers = driver.find_elements(By.CSS_SELECTOR, 'a.text-muted.pl-2[data-patient-app-selector="patient-app-event"]')
                    for num in prenumbers:
                        if len(num.text) > 5:
                            numerostel.append(num.text)
                            break  # Tomar el primer número válido
                    time.sleep(0.5)
                    driver.execute_script("document.elementFromPoint(200, 300).click();")
            numerotel.append(numerostel if numerostel else None)
        except:
            numerotel.append(None)

        # Reiniciar WebDriver cada 20 iteraciones
        if i % 20 == 0 and i > 0:
            driver.quit()
            driver = webdriver.Chrome(options=options)

    except Exception as ex:
        print(f"⚠️ Error en {e}: {ex}")
        urls.append(e)
        name.append(None)
        especialidad.append(None)
        rating.append(None)
        direccion.append(None)
        numerotel.append(None)
        clinica.append(None)
        formacion.append(None)
        residencia.append(None)
        linkedinurl.append(None)
        facebookurl.append(None)
        precio.append(None)



sample=({
    'nombre':name,
    'especialidad':especialidad,
    'numero de telefono':numerotel,
    'rating':rating,
    'direccion':direccion,
    'url':urls,
    'clinica':clinica,
    'residencia':residencia,
    'formacion':formacion,
    'linkedinurl':linkedinurl,
    'facebookurl':facebookurl,
    'precio':precio
})


for a in sample:
    print(a,len(sample[a]))



sample=pd.DataFrame(sample)


sample['numero de telefono']=sample['numero de telefono'].apply(lambda x: str(x).replace('[', '').replace(']', '') if x is not None else None)

print('creando documento')
sample.to_csv(Especialidad+Zona+enlinea+'.csv',index=False)
