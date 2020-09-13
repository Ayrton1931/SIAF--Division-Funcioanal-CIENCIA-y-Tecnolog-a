# -*- coding: utf-8 -*-
"""
Created on Thu Sep 10 20:51:41 2020

@author: Shadow
"""

import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
import pandas as pd
import requests
import urllib.parse as urlparse
import re
def newMatrix(f,c,n):
    matriz=[]
    for i in range(f):
        a=[n]*c
        matriz.append(a)
    return matriz

###############################################################################
############################################################################### 
############################################################################### 

#### Definition of folder paths:
input_folder_path = r'D:\mini-trabajos\SIAF Innovacion\Input'    ### Carpeta donde estan los insumos, en este caso no hay
output_folder_path = r'D:\mini-trabajos\SIAF Innovacion\Output' ## Carpeta donde se guardan los resultados
driver_path = r'D:\mini-trabajos\SIAF Innovacion\Code\Chromedriver\chromedriver.exe' ## Carpeta donde se guarda en el chromedriver

years = [ "2015", "2018", "2019", "2020"]
##############################################################################
############################################################################## SECTION 1: donwload information.
##############################################################################

############################################## PARTE 1
############################################## Loop inicial, debajo de este estan todos los pasos


for i in years: 
    new_dir = os.path.join( output_folder_path, i )
    #if not os.path.exists(new_dir):
    #    os.makedirs(new_dir)
        
    option = webdriver.ChromeOptions() 
    chrome_prefs = {}
    option.experimental_options["prefs"] = chrome_prefs
    chrome_prefs["profile.default_content_settings"] = {"images": 2}
    chrome_prefs["profile.managed_default_content_settings"] = {"images": 2}
    #option.add_argument("--headless") 
    option.add_experimental_option("prefs",  {'download.default_directory' : new_dir,
                                              "safebrowsing.enabled": "false"} )
    driver = webdriver.Chrome(options=option, executable_path=driver_path)
    driver.get(r"http://apps5.mineco.gob.pe/transparencia/Mensual/Default.aspx")
    

    ###############
    #~ Part 1: Choose year  
    ###############
      
    iframe = driver.find_elements_by_tag_name('frame')[0] ### Cambio de FRAME (particularidad de la pagina)
    driver.switch_to_frame(iframe)                        ### Accediendo la nuevo frame
    
    # Choose YEAR
    click_enable = driver.find_element_by_xpath("//option[@value='%s']" %i )
    next_enable = click_enable.is_enabled() 
    click_enable.click()
    
    # Change Frame
    iframe = driver.find_elements_by_tag_name('frame')[0] ### Cambio de FRAME (particularidad de la pagina)
    driver.switch_to_frame(iframe)                        ### Accediendo la nuevo frame

    ###############
    #~ Part 2: Interaction with page  
    ###############
    
    ### Click on 'Funcion' button
    next_enable=None### Define a logic variabl
    while not next_enable:             ### Define a indefinited loop, this just will be interruped if the button is found.
        try:
            click_enable = driver.find_element_by_xpath("//input[@type='submit'][@value='Función'][@onclick='OnClickButton();']")  ### Definition of element that will be sought
            next_enable = click_enable.is_enabled()   ### Redefine the logical variable. 
        except NoSuchElementException:
            time.sleep(0.1)
    click_enable.click()       ### Click the button.
    
    # Gather all Funcion in a list
    sub_funcion=None
    while not sub_funcion:
        content=driver.page_source             #### Se descarga el codigo HTML
        soup = BeautifulSoup(content)          #### Se conviente dicho code en beautifulSoup element
        try:
            sub_funcion = soup.find_all('table', class_='Data')   ### Se busca la parte de code que contiene los input para escoger los pliegos.
        except NoSuchElementException:
            time.sleep(0.1)        
    sub_funcion1 = sub_funcion[0].find_all('input')        ### Se busca los input para seleccionar 
    list_sub_funcion1=[]                                  ### Se crea una lista vacia para almacenar los inputs                                       
    for ii in sub_funcion1:                                ### Se obtiene los inputs mediante este bucle                   
        a= ii.get('onclick')
        list_sub_funcion1.append(a)
    # Get inside of each sector.
    for jj in list_sub_funcion1:
        next_enable=None                     ### Define a logic variable
        while not next_enable:             ### Define a indefinited loop, this just will be interruped if the button is found. 
          try:
            click_enable = driver.find_element_by_xpath("//input[@type='radio'][@onclick = '%s' ]" %jj )  ### Definition of element that will be sought
            next_enable = click_enable.is_enabled()   ### Redefine the logical variable. 
          except NoSuchElementException:
            time.sleep(0.1)
        click_enable.click()       ### Click the button. 
        ### Click on 'Division Funcional' button
        driver.find_element_by_xpath("//input[@type='submit'][@value='División Funcional'][@onclick='OnClickButton();']").click()
        # Gather all "Division Funcional" in a list
        sub_div_funcion=None
        while not sub_div_funcion:
            content=driver.page_source             #### Se descarga el codigo HTML
            soup = BeautifulSoup(content)          #### Se conviente dicho code en beautifulSoup element
            try:
                sub_div_funcion = soup.find_all('table', class_='Data')   ### Se busca la parte de code que contiene los input para escoger los pliegos.
            except NoSuchElementException:
                time.sleep(0.1)        
        sub_div_funcion1 = sub_div_funcion[0].find_all('input')        ### Se busca los input para seleccionar 
        list_sub_div_funcion1=[]                                  ### Se crea una lista vacia para almacenar los inputs                                       
        for ii in sub_div_funcion1:                                ### Se obtiene los inputs mediante este bucle                   
            a= ii.get('onclick')
            list_sub_div_funcion1.append(a)
        
        name_a = [CyT for CyT in list_sub_div_funcion1 if re.search(r"009", CyT )]
        
        if len(name_a) == 0:
            driver.execute_script("window.history.go(-1)")                         
        else:  
            aa = name_a[0]
            next_enable=None                     ### Define a logic variable
            while not next_enable:             ### Define a indefinited loop, this just will be interruped if the button is found. 
              try:
                click_enable = driver.find_element_by_xpath("//input[@type='radio'][@onclick = '%s' ]" %aa )  ### Definition of element that will be sought
                next_enable = click_enable.is_enabled()   ### Redefine the logical variable. 
              except NoSuchElementException:
                time.sleep(0.1)
            click_enable.click()       ### Click the button.
            ### Click on 'Nivel de gobierno' button
            driver.find_element_by_xpath("//input[@type='submit'][@value='Nivel de Gobierno'][@onclick='OnClickButton();']").click()
            # Gather all "Division Funcional" in a list
            sub_nivel_gob=None
            while not sub_nivel_gob:
                content=driver.page_source             #### Se descarga el codigo HTML
                soup = BeautifulSoup(content)          #### Se conviente dicho code en beautifulSoup element
                try:
                    sub_nivel_gob = soup.find_all('table', class_='Data')   ### Se busca la parte de code que contiene los input para escoger los pliegos.
                except NoSuchElementException:
                    time.sleep(0.1)  
                    
            sub_nivel_gob1 = sub_nivel_gob[0].find_all('input')        ### Se busca los input para seleccionar 
            list_sub_nivel_gob1=[]                                  ### Se crea una lista vacia para almacenar los inputs                                       
            for ii in sub_nivel_gob1:                                ### Se obtiene los inputs mediante este bucle                   
                a= ii.get('onclick')
                list_sub_nivel_gob1.append(a)
            
            name_niv_gob = [CyT for CyT in list_sub_nivel_gob1 if re.search(r"E|R", CyT )]
            
            if len(name_niv_gob)==0:
                driver.execute_script("window.history.go(-1)")
            else:
                for kk in name_niv_gob:
                    next_enable=None                     ### Define a logic variable
                    while not next_enable:             ### Define a indefinited loop, this just will be interruped if the button is found. 
                      try:
                        click_enable = driver.find_element_by_xpath("//input[@type='radio'][@onclick = '%s' ]" %kk )  ### Definition of element that will be sought
                        next_enable = click_enable.is_enabled()   ### Redefine the logical variable. 
                      except NoSuchElementException:
                        time.sleep(0.1)
                    click_enable.click()       ### Click the button.                    
                    ### Click on 'Nivel de gobierno' button
                    driver.find_element_by_xpath("//input[@type='submit'][@value='Sector'][@onclick='OnClickButton();']").click()            
                    # Gather all "Division Funcional" in a list
                    sub_sector=None
                    while not sub_sector:
                        content=driver.page_source             #### Se descarga el codigo HTML
                        soup = BeautifulSoup(content)          #### Se conviente dicho code en beautifulSoup element
                        try:
                            sub_sector = soup.find_all('table', class_='Data')   ### Se busca la parte de code que contiene los input para escoger los pliegos.
                        except NoSuchElementException:
                            time.sleep(0.1)          
                    sub_sector1 = sub_sector[0].find_all('input')        ### Se busca los input para seleccionar 
                    list_sub_sector1=[]                                  ### Se crea una lista vacia para almacenar los inputs                                       
                    for ii in sub_sector1:                                ### Se obtiene los inputs mediante este bucle                   
                        a= ii.get('onclick')
                        list_sub_sector1.append(a)  
                    # Get inside of each sector.    
                    for ll in list_sub_sector1:
                        next_enable=None                     ### Define a logic variable
                        while not next_enable:             ### Define a indefinited loop, this just will be interruped if the button is found. 
                          try:
                            click_enable = driver.find_element_by_xpath("//input[@type='radio'][@onclick = '%s' ]" %ll )  ### Definition of element that will be sought
                            next_enable = click_enable.is_enabled()   ### Redefine the logical variable. 
                          except NoSuchElementException:
                            time.sleep(0.1)
                        click_enable.click()       ### Click the button.                     
                        ### Click on 'Pliego' button
                        driver.find_element_by_xpath("//input[@type='submit'][@value='Pliego'][@onclick='OnClickButton();']").click()  
                        # Gather all "Pliego" in a list
                        sub_pliego=None
                        while not sub_pliego:
                            content=driver.page_source             #### Se descarga el codigo HTML
                            soup = BeautifulSoup(content)          #### Se conviente dicho code en beautifulSoup element
                            try:
                                sub_pliego = soup.find_all('table', class_='Data')   ### Se busca la parte de code que contiene los input para escoger los pliegos.
                            except NoSuchElementException:
                                time.sleep(0.1)          
                        sub_pliego1 = sub_pliego[0].find_all('input')        ### Se busca los input para seleccionar 
                        list_sub_pliego1=[]                                  ### Se crea una lista vacia para almacenar los inputs                                       
                        for ii in sub_pliego1:                                ### Se obtiene los inputs mediante este bucle                   
                            a= ii.get('onclick')
                            list_sub_pliego1.append(a)                          
                        # Get inside of each Pliego.    
                        for mm in list_sub_pliego1:
                            next_enable=None                     ### Define a logic variable
                            while not next_enable:             ### Define a indefinited loop, this just will be interruped if the button is found. 
                              try:
                                click_enable = driver.find_element_by_xpath("//input[@type='radio'][@onclick = '%s' ]" %mm )  ### Definition of element that will be sought
                                next_enable = click_enable.is_enabled()   ### Redefine the logical variable. 
                              except NoSuchElementException:
                                time.sleep(0.1)
                            click_enable.click()       ### Click the button.                     
                            ### Click on 'Pliego' button
                            driver.find_element_by_xpath("//input[@type='submit'][@value='Ejecutora'][@onclick='OnClickButton();']").click() 
                            # Gather all "Ejecutora" in a list
                            sub_ejecutora = None
                            while not sub_ejecutora:
                                content=driver.page_source             #### Se descarga el codigo HTML
                                soup = BeautifulSoup(content)          #### Se conviente dicho code en beautifulSoup element
                                try:
                                    sub_ejecutora = soup.find_all('table', class_='Data')   ### Se busca la parte de code que contiene los input para escoger los pliegos.
                                except NoSuchElementException:
                                    time.sleep(0.1)          
                            sub_ejecutora1 = sub_ejecutora[0].find_all('input')        ### Se busca los input para seleccionar 
                            list_sub_ejecutora1=[]                                  ### Se crea una lista vacia para almacenar los inputs                                       
                            for ii in sub_ejecutora1:                                ### Se obtiene los inputs mediante este bucle                   
                                a= ii.get('onclick')
                                list_sub_ejecutora1.append(a)        
                            # Get inside of each Ejecutora.    
                            for nn in list_sub_ejecutora1:
                                next_enable=None                     ### Define a logic variable
                                while not next_enable:             ### Define a indefinited loop, this just will be interruped if the button is found. 
                                  try:
                                    click_enable = driver.find_element_by_xpath("//input[@type='radio'][@onclick = '%s' ]" %nn )  ### Definition of element that will be sought
                                    next_enable = click_enable.is_enabled()   ### Redefine the logical variable. 
                                  except NoSuchElementException:
                                    time.sleep(0.1)
                                click_enable.click()       ### Click the button.                     
                                ### Click on 'Pliego' button
                                driver.find_element_by_xpath("//input[@type='submit'][@value='Categoría Presupuestal'][@onclick='OnClickButton();']").click() 
                                # Gather all "Categoria" in a list
                                sub_categoria = None
                                while not sub_categoria:
                                    content=driver.page_source             #### Se descarga el codigo HTML
                                    soup = BeautifulSoup(content)          #### Se conviente dicho code en beautifulSoup element
                                    try:
                                        sub_categoria = soup.find_all('table', class_='Data')   ### Se busca la parte de code que contiene los input para escoger los pliegos.
                                    except NoSuchElementException:
                                        time.sleep(0.1)          
                                sub_categoria1 = sub_categoria[0].find_all('input')        ### Se busca los input para seleccionar 
                                list_sub_categoria1=[]                                  ### Se crea una lista vacia para almacenar los inputs                                       
                                for ii in sub_categoria1:                                ### Se obtiene los inputs mediante este bucle                   
                                    a= ii.get('onclick')
                                    list_sub_categoria1.append(a)
                                # Get inside of each Catagoria.    
                                for ss in list_sub_categoria1:
                                    next_enable=None                     ### Define a logic variable
                                    while not next_enable:             ### Define a indefinited loop, this just will be interruped if the button is found. 
                                      try:
                                        click_enable = driver.find_element_by_xpath("//input[@type='radio'][@onclick = '%s' ]" %ss )  ### Definition of element that will be sought
                                        next_enable = click_enable.is_enabled()   ### Redefine the logical variable. 
                                      except NoSuchElementException:
                                        time.sleep(0.1)
                                    click_enable.click()       ### Click the button.                     
                                    ### Click on 'Producto/Proyecto' button
                                    driver.find_element_by_xpath("//input[@type='submit'][@value='Producto/Proyecto'][@onclick='OnClickButton();']").click()    
                                    # Gather all "Categoria" in a list
                                    sub_producto = None
                                    while not sub_producto:
                                        content=driver.page_source             #### Se descarga el codigo HTML
                                        soup = BeautifulSoup(content)          #### Se conviente dicho code en beautifulSoup element
                                        try:
                                            sub_producto = soup.find_all('table', class_='Data')   ### Se busca la parte de code que contiene los input para escoger los pliegos.
                                        except NoSuchElementException:
                                            time.sleep(0.1)          
                                    sub_producto1 = sub_producto[0].find_all('input')        ### Se busca los input para seleccionar 
                                    list_sub_producto1=[]                                  ### Se crea una lista vacia para almacenar los inputs                                       
                                    for ii in sub_producto1:                                ### Se obtiene los inputs mediante este bucle                   
                                        a= ii.get('onclick')
                                        list_sub_producto1.append(a)
                                    for rr in list_sub_producto1:
                                        next_enable=None                     ### Define a logic variable
                                        while not next_enable:             ### Define a indefinited loop, this just will be interruped if the button is found. 
                                          try:
                                            click_enable = driver.find_element_by_xpath("//input[@type='radio'][@onclick = '%s' ]" %rr )  ### Definition of element that will be sought
                                            next_enable = click_enable.is_enabled()   ### Redefine the logical variable. 
                                          except NoSuchElementException:
                                            time.sleep(0.1)
                                        click_enable.click()       ### Click the button.                     
                                        ### Click on 'Departamento' button
                                        driver.find_element_by_xpath("//input[@type='submit'][@value='Departamento'][@onclick='OnClickButton();']").click()                                    
                                        ### Click Download button
                                        next_enable=None                     ### Define a logic variable
                                        while not next_enable:             ### Define a indefinited loop, this just will be interruped if the button is found. 
                                          try:
                                            click_enable = driver.find_element_by_xpath("//a[@id='ctl00_CPH1_lbtnExportar'][@class='ToolBarBtn']")  ### Definition of element that will be sought
                                            next_enable = click_enable.is_enabled()   ### Redefine the logical variable. 
                                          except NoSuchElementException:
                                            time.sleep(0.1)
                                        click_enable.click()       ### Click the button.
                                        driver.execute_script("window.history.go(-1)")
                                    driver.execute_script("window.history.go(-1)") ##Producto/Proyecto
                                driver.execute_script("window.history.go(-1)") ## Catagoria
                            driver.execute_script("window.history.go(-1)") ## Ejecutora
                        driver.execute_script("window.history.go(-1)") #Pliego
                    driver.execute_script("window.history.go(-1)") ## Sector
                driver.execute_script("window.history.go(-1)") ## Nivel de Gobierno
            driver.execute_script("window.history.go(-1)")
        
        
#########################################################################################      
#########################################################################################     
######################################################################################### Organizacion de EXCELS
#########################################################################################     
#########################################################################################     

List_year_df=[]
for i in years:
    new_dir = os.path.join( output_folder_path, i )                             #### Ingresar a cada carpeta por año.
    list_of_names_files = os.listdir(new_dir)                       #### Obtener los nombres de los archivos de cada carpeta.
    for ss in list_of_names_files:                                  
        if re.search( 'desktop.ini', ss ):
            list_of_names_files.remove('desktop.ini')      
    
    List_semifinal = []                                      ### Lista vacia donde se guardaran los archivos descagados.             
    for ii in list_of_names_files:                                  ### Importar cada file y ponerlo en una lista.        
        file_path=os.path.join(new_dir, ii)                         ### Definir la direccion de cada file.
        content_file = pd.read_html(file_path)                      ### Read the file as html document         
        first_names = content_file[1][0] 
        MM = newMatrix(1,8,0)
        for jj in range(1,len(first_names) ):
            if re.search(r'Función', first_names[jj]):
                MM[0][jj-1]= re.sub('Función', '', first_names[jj])
            elif re.search(r'División Funcional', first_names[jj]):
                MM[0][jj-1]=re.sub('División Funcional', '', first_names[jj])
            elif re.search(r'Nivel de Gobierno', first_names[jj]):
                MM[0][jj-1]=re.sub('Nivel de Gobierno', '', first_names[jj])
            elif re.search(r'Sector', first_names[jj]):
                MM[0][jj-1]=re.sub('Sector', '', first_names[jj])
            elif re.search(r'Pliego', first_names[jj]):
                MM[0][jj-1]=re.sub('Pliego', '', first_names[jj])
            elif re.search(r'Unidad Ejecutora', first_names[jj]):
                MM[0][jj-1]=re.sub('Unidad Ejecutora', '', first_names[jj])
            elif re.search(r'Categoría Presupuestal', first_names[jj]):
                MM[0][jj-1]=re.sub('Categoría Presupuestal', '', first_names[jj]) 
            elif re.search(r'Producto/Proyecto', first_names[jj]):
                MM[0][jj-1]=re.sub('Producto/Proyecto', '', first_names[jj])
        
        Dataframe_uni = pd.DataFrame( MM )
        Dataframe_uni.columns = ['Función','División Funcional','Nivel de Gobierno',
                                 'Sector','Pliego','Unidad Ejecutora',
                                 'Categoría Presupuestal', 'Producto/Proyecto']
        first_values = content_file[3]    
        f_values= pd.concat( [first_values[0], first_values[1],
                     first_values[2], first_values[6]], axis=1 )    
        f_values.columns=['Departamento', 'PIA', 'PIM', 'Devengado']   
        shape_df = f_values.shape 
        if shape_df[0]==1:
            final_row= pd.concat( [Dataframe_uni, f_values], axis=1 )
        else:
            import numpy as np
            newdf = pd.DataFrame(np.repeat(Dataframe_uni.values,shape_df[0],axis=0))
            newdf.columns = Dataframe_uni.columns
            final_row= pd.concat( [newdf, f_values], axis=1 )    
        List_semifinal.append(final_row)
        
    for ll in range(0, len(List_semifinal)):
        if ll == 0:
            Data_Frame_final = pd.DataFrame( List_semifinal[ll] )
        else:
            Data_Frame_final = pd.concat( [Data_Frame_final, List_semifinal[ll] ] )
    Data_Frame_final['year'] = i
    List_year_df.append(Data_Frame_final)        

for mm in range(0, len(List_year_df) ):
    if mm==0:
        Data_Frame_Total= List_year_df[0]
    else:
        Data_Frame_Total= pd.concat( [Data_Frame_Total, List_year_df[mm]] ) 
        
# Exportar a DTA        
Data_Frame_Total = Data_Frame_Total.reset_index()           
Final_file_path = os.path.join(output_folder_path, 'Final.dta')             
Data_Frame_Total.to_stata(Final_file_path, version=117)          
            
            