#!/usr/bin/env python
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import socket
from urllib2 import urlopen
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import unicodedata
from flask import *
from json import *
from flask_cors import CORS, cross_origin


#Start flask app, and set the CORS configuration to allow the access to any device or modern framework
app = Flask(__name__)
CORS(app)




@app.route('/api/v1/ufro/horario', methods=['POST'])
def horarioApi():

    chrome_options = webdriver.ChromeOptions()
    #chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.set_window_size(1024, 768) # optional


    print "Formateando valores de entrada"
    content = request.json
    user = content['username']
    password = content['password']

    print "Contenido"
    print user
    print password

    print "Cargando pagina"
    driver.get("https://intranet.ufro.cl/")  

    print "Rellenando informacion de credenciales"
    username_field = driver.find_element_by_name('Formulario[POPUSERNAME]')
    username_field.send_keys( user )

    password_field = driver.find_element_by_name('Formulario[XYZ]')
    password_field.send_keys( password )

    entrarBtn = driver.find_elements(By.XPATH, "//a[@href='Javascript:Enviar()']")
    for option in entrarBtn: #iterate over the options, place attribute value in list
        option.click()


    print "Abriendo menu para acceder a horarios"
    WebDriverWait(driver, 6).until( EC.presence_of_element_located((By.XPATH, "//a[@class='linksubmenu']")) )    
    subMenuOptions = driver.find_elements(By.XPATH, "//a[@class='linksubmenu']")

    for option in subMenuOptions: #iterate over the options, place attribute value in list
        elementList = option.find_elements_by_tag_name("font")
        if( elementList[0].text == "Alumno" ):
            option.click()
            break

    print "Accediendo a horarios"
    WebDriverWait(driver, 6).until( EC.presence_of_element_located((By.XPATH, "//a[@class='linkopcmenu']")) )  
    horariosMenu = driver.find_elements(By.XPATH, "//a[@class='linkopcmenu']")

    for option in horariosMenu: #iterate over the options, place attribute value in list
        elementList = option.find_elements_by_tag_name("font")
        if( elementList[0].text == "Horarios" ):
            option.click()
            break


    WebDriverWait(driver, 6).until( EC.presence_of_element_located((By.XPATH, "//table[@style='border: 2px solid #8caedc;']")) )  
    menuTabla = driver.find_elements(By.XPATH, "//table[@style='border: 2px solid #8caedc;']")

    for option in menuTabla: #iterate over the options, place attribute value in list
        elementClass = option.get_attribute("class")
        if( elementClass == "Normal" ):
            print "Horario encontrado"
            horario = option
            break



    print "Creando objeto de respuesta"
    respo = {}
    respo['horario'] = []

    for row in horario.find_elements_by_xpath(".//tr"):
        rowArray = [td.text for td in row.find_elements_by_xpath(".//td")]
        try:
            respo['horario'].append({ "periodo" : rowArray[0], "Lunes" : rowArray[1], "Martes" : rowArray[2], "Miercoles" : rowArray[3], "Jueves" : rowArray[4], "Viernes" : rowArray[5], "Sabado": rowArray[6] })
        except IndexError:
            print "omitiendo.."

    print "Enviando respuesta"
    driver.close()
    return json.dumps( respo, indent= 4 )





@app.route('/api/v1/ufro/notas', methods=['POST'])
def notasApi():

    chrome_options = webdriver.ChromeOptions()
    #chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.set_window_size(1024, 768) # optional
    respo = {}
    respo['notas'] = []


    print "Formateando valores de entrada"
    content = request.json
    user = content['username']
    password = content['password']

    try:
        semester = content['semester']
        year = content['year']
        period = year+semester
    except KeyError:
        respo['notas'].append({ "error" : "Para realizar esta consulta es necesario especificar semestre y anio" })
        driver.close()
        return json.dumps( respo, indent= 4 )
          
        


    print "Contenido"
    print user
    print password

    print "Cargando pagina"
    driver.get("https://intranet.ufro.cl/")  

    print "Rellenando informacion de credenciales"
    username_field = driver.find_element_by_name('Formulario[POPUSERNAME]')
    username_field.send_keys( user )

    password_field = driver.find_element_by_name('Formulario[XYZ]')
    password_field.send_keys( password )

    entrarBtn = driver.find_elements(By.XPATH, "//a[@href='Javascript:Enviar()']")
    for option in entrarBtn: #iterate over the options, place attribute value in list
        option.click()


    print "Abriendo menu para acceder a notas"
    WebDriverWait(driver, 6).until( EC.presence_of_element_located((By.XPATH, "//a[@class='linksubmenu']")) )    
    subMenuOptions = driver.find_elements(By.XPATH, "//a[@class='linksubmenu']")

    for option in subMenuOptions: #iterate over the options, place attribute value in list
        elementList = option.find_elements_by_tag_name("font")
        if( elementList[0].text == "Alumno" ):
            option.click()
            break

    print "Accediendo a notas"
    WebDriverWait(driver, 6).until( EC.presence_of_element_located((By.XPATH, "//a[@class='linkopcmenu']")) )  
    horariosMenu = driver.find_elements(By.XPATH, "//a[@class='linkopcmenu']")

    for option in horariosMenu: #iterate over the options, place attribute value in list
        elementList = option.find_elements_by_tag_name("font")
        if( elementList[0].text == "Consultas" ):
            option.click()
            break

    WebDriverWait(driver, 6).until( EC.presence_of_element_located((By.XPATH, "//a[@class='linkopcmenu']")) )  
    horariosMenu = driver.find_elements(By.XPATH, "//a[@class='linkopcmenu']")

    for option in horariosMenu: #iterate over the options, place attribute value in list
        elementList = option.find_elements_by_tag_name("font")
        if( elementList[0].text == "Notas Parciales" ):
            option.click()
            break

    print "Seleccionando semestre en cuestion" 
    periodSelect = driver.find_element_by_name('Formulario[periodo]')
    options = periodSelect.find_elements_by_tag_name("option")
    select = Select(periodSelect)

    for option in options:
        if( period == unicodedata.normalize('NFKD', option.text.lower() ).encode('ascii','ignore') ):
            select.select_by_value( option.get_attribute("value") )


if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True, port=5000) #Aqui se cambia el puerto y se declara publico para el mundo 0.0.0.0
