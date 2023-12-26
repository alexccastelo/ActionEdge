import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import csv
from datetime import datetime
import re

# Defina o URL do site que você deseja raspá-lo
url = "https://www.oficinadanet.com.br/smartphones/google-pixel-5"

# Defina os caminhos dos elementos HTML que você deseja raspá-los
element_path_name = '//h1[@class="title"]'
element_path_releasedate = '//*[@id="especificacoes"]/div[2]/div[5]'
element_path_weight = '//*[@id="especificacoes"]/div[3]/div[5]'
element_path_cpu = '//*[@id="especificacoes"]/div[4]/div[5]/a'
element_path_ram = '//*[@id="especificacoes"]/div[5]/div[3]/a'
element_path_storage = '//*[@id="especificacoes"]/div[5]/div[5]'
element_path_screensize = '//*[@id="especificacoes"]/div[6]/div[5]'
element_path_screenresolution = '//*[@id="especificacoes"]/div[6]/div[7]'
element_path_battery = '//*[@id="especificacoes"]/div[9]/div[3]/a'
element_path_4G = '//*[@id="especificacoes"]/div[10]/div[5]'
element_path_5G = '//*[@id="especificacoes"]/div[10]/div[7]'
element_path_bluetooth = '//*[@id="especificacoes"]/div[10]/div[11]'
element_path_usb = '//*[@id="especificacoes"]/div[12]/div[5]'
element_path_sensors = '//*[@id="especificacoes"]/div[12]/div[7]' 

# Configurações para executar o Chrome em modo headless
chrome_options = Options()
chrome_options.add_argument("--headless")

# Inicialize o webdriver com as opções configuradas
driver = webdriver.Chrome(options=chrome_options)
driver.get(url)
time.sleep(1)

name = driver.find_element(By.XPATH, element_path_name).text
releasedate = driver.find_element(By.XPATH, element_path_releasedate).text
weight = driver.find_element(By.XPATH, element_path_weight).text
cpu = driver.find_element(By.XPATH, element_path_cpu).text
ram = driver.find_element(By.XPATH, element_path_ram).text
storage = driver.find_element(By.XPATH, element_path_storage).text
screensize = driver.find_element(By.XPATH, element_path_screensize).text
screenresolution = driver.find_element(By.XPATH, element_path_screenresolution).text
battery = driver.find_element(By.XPATH, element_path_battery).text
quatroG = driver.find_element(By.XPATH, element_path_4G).text
cincoG = driver.find_element(By.XPATH, element_path_5G).text
bluetooth = driver.find_element(By.XPATH, element_path_bluetooth).text
usb = driver.find_element(By.XPATH, element_path_usb).text
sensors = driver.find_element(By.XPATH, element_path_sensors).text

print("Final dos XPATHs")
time.sleep(2)
print(name)
print(releasedate)
print(weight)
print(cpu)
print(ram)
print(storage)
print(screensize)
print(screenresolution)
print(battery)
print(quatroG)
print(cincoG)
print(bluetooth)
print(usb)
print(sensors)
print("--------- Script encerrado ---------")
time.sleep(2)
# Feche o webdriver
driver.quit()
