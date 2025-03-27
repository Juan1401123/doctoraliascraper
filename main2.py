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
from datetime import datetime
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import NoSuchElementException
import math


start_page='https://www.doctoralia.com.mx/buscar?q=Ginec%C3%B3logo&loc=Ciudad%20de%20M%C3%A9xico&filters%5Bspecializations%5D%5B0%5D=30&page=3'
top=25



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


driver.get(start_page)


urls_toscrap=[]


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
      print('')
 
 if driver.find_elements(By.CLASS_NAME,'page-item')[len(driver.find_elements(By.CLASS_NAME,'page-item'))-1].text=='Siguiente':
  nextpage=driver.find_elements(By.CLASS_NAME,'page-item')[len(driver.find_elements(By.CLASS_NAME,'page-item'))-1]
  nextpage.click()
  if pd.DataFrame(urls_toscrap)[0].nunique()>=top:
    desicion=0 
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
redes=[]
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

            driver.get(e)
            time.sleep(2)
            attempts += 1

        # Si no cambia de página, reiniciar WebDriver
        if driver.current_url == old_url:
            
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
        arrayredes=[]
        # Extraer información adicional
        try:
            btres = driver.find_element(By.CSS_SELECTOR, 'button[class="btn btn-light btn-lg btn-block mt-1"]')
            btres.click()
            time.sleep(.5)
            preresidencia, preformacion, unicredes = None, None, None
            for c in driver.find_elements(By.CSS_SELECTOR, '#about-section > div.modal.fade.modal-scrollable.show > div > div > div.modal-body > div'):
                if 'Residencia' in c.text:
                    preresidencia = c.text
                elif 'Formación' in c.text:
                    preformacion = c.text
                elif 'Redes sociales' in c.text:
                    preredes = c.find_elements(By.TAG_NAME, "a")
                    for d in preredes:
                            unicredes= d.get_attribute("href")
                            arrayredes.append(unicredes)
            residencia.append(preresidencia if preresidencia else None)
            formacion.append(preformacion if preformacion else None)
            redes.append(arrayredes if arrayredes else None)
        except:
            residencia.append(None)
            formacion.append(None)
            redes.append(None)
            
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
        print(i,e)
        # Reiniciar WebDriver cada 20 iteraciones
        if i % 20 == 0 and i > 0:
            driver.quit()
            driver = webdriver.Chrome(options=options)
        
    except Exception as ex:
        urls.append(e)
        name.append(None)
        especialidad.append(None)
        rating.append(None)
        direccion.append(None)
        numerotel.append(None)
        clinica.append(None)
        formacion.append(None)
        residencia.append(None)
        redes.append(None)
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
    'redes sociales':redes,
    'precio':precio
})




sample=pd.DataFrame(sample)
sample['numero de telefono']=sample['numero de telefono'].apply(lambda x: str(x).replace('[', '').replace(']', '') if x is not None else None)
sample['redes sociales']=sample['redes sociales'].apply(lambda x: str(x).replace('[', '').replace(']', '') if x is not None else None)
sample['opiniones']=sample['rating'].apply(lambda x:' '.join(x.split(' ')[1:])if x is not None else None)
sample['residencia']=sample['residencia'].apply(lambda x:x.replace('Residencia\n','')if x is not None else None)
sample['rating']=sample['rating'].apply(lambda x:' '.join(x.split(' ')[0])if x is not None else None)
sample['formacion']=sample['formacion'].apply(lambda x:x.replace('Formación\n','')if x is not None else None)
sample['opiniones']=sample['opiniones'].apply(lambda x:x.replace(' opiniones','')if x is not None else None)
sample[['nombre', 'especialidad', 'numero de telefono', 'rating','opiniones', 'direccion',
       'url', 'clinica', 'residencia', 'formacion', 'redes sociales', 'precio']]
print('Creando documento...')

# Obtener la fecha y hora actual en formato seguro
fecha_hora_actual = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

# Generar el nombre del archivo
nombre_archivo = f"{fecha_hora_actual}_{len(sample)}.csv"

# Guardar el DataFrame como CSV
sample.to_csv(nombre_archivo, index=False)
