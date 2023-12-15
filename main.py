# XPATH campo texto (element_path): //*[@id="is-avail-field"]
# XPATH botão(element_button): //*[@id="conteudo"]/div/section[1]/div[1]/form/div/button
# texto a preencher no campo texto (element_text): "actionedge.com.br"
# XPATH resultado pesquisa nome domínio (element_dominio): //*[@id="conteudo"]/div/section/div[2]/div/strong
# XPATH resultado pesquisa status domínio (element_status): //*[@id="conteudo"]/div/section/div[2]/div/p
# XPATH domínios disponíveis(element_disponiveis): //*[@id="conteudo"]/div/section/div[2]/div/div[2]/ul/li[2]/p
# XPATH processo de liberação (element_liberacao): //*[@id="conteudo"]/div/section/div[2]/div/div/p[1]
# Sequence:
# 1. mapear XPATH campo texto
# 2. escrever texto
# 3. mapear XPATH botão
# 4. clicar no botão
# 5. aguardar 3 segundos
# 6. mapear o XPATH 'element_dominio"
# 7. capturar o conteúdo 'element_dominio'
# 8. mapear o XPATH 'element_status'
# 9. capturar o conteúdo 'element_status'
# 10. incluir no arquivo CSV dominios.csv:
# 10.1. 'url', 'data_hora_atuais', element_dominio', 'element_status'
# 11. caso o 'element_status' seja igual a "Domínio não disponível para registro.", o site irá relacionar abaixo dos domínios dispoíveis, um abaixo do outro e sendo assim:
# 11.1. mapear, um a um, no XPATH domínios disponíveis(element_disponiveis): //*[@id="conteudo"]/div/section/div[2]/div/div[2]/ul/li[2]/p
# 11.2. caputurar os domínios disponíveis
# 11.3. inclui no arquivo dominios_disponiveis.csv no formato:
# 11.4. 'url', 'data_hora_atuais', element_dominio', 'dominio_disponivel'
# 12. aguardar 3 segundos
# 13. fechar o navegador

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import csv
from datetime import datetime
import re

# Defina o URL do site que você deseja raspá-lo
url = "https://registro.br/"

# Defina os caminhos dos elementos HTML que você deseja raspá-los
element_path = '//input[@id="is-avail-field"]'
element_button = '//*[@id="conteudo"]/div/section[1]/div[1]/form/div/button'
element_text = "042vip.com.br"
element_dominio = '//*[@id="conteudo"]/div/section/div[2]/div/strong'
element_status = '//*[@id="conteudo"]/div/section/div[2]/div/p'
element_disponiveis = '//*[@id="conteudo"]/div/section/div[2]/div/div[2]/ul/li/p'
element_liberacao = '//*[@id="conteudo"]/div/section/div[2]/div/div/p[1]'

# Configurações para executar o Chrome em modo headless
chrome_options = Options()
chrome_options.add_argument("--headless")

# Inicialize o webdriver com as opções configuradas
driver = webdriver.Chrome(options=chrome_options)
driver.get(url)

# Aguarde alguns segundos para o JavaScript carregar
time.sleep(1)

# Localize o elemento HTML e escreva um texto
element = driver.find_element(By.XPATH, element_path)
element.send_keys(element_text)
time.sleep(1)

# Clique no botão
button = driver.find_element(By.XPATH, element_button)
button.click()
time.sleep(1)

dominio = driver.find_element(By.XPATH, element_dominio).text
status = driver.find_element(By.XPATH, element_status).text

# Captura da data e hora atuais
data_hora_atuais = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Abre o arquivo CSV para escrita
with open("dominios_disponiveis.csv", mode="a", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    # Escreve o cabeçalho do arquivo CSV
    # writer.writerow(["URL", "Data_Hora", "Dominio", "Dominio_Disponivel"])

    # Verifica o status do domínio
    if status == "Domínio não disponível para registro.":
        # Captura os domínios disponíveis
        dominios_disponiveis = driver.find_elements(By.XPATH, element_disponiveis)

        for dominio_disponivel in dominios_disponiveis:
            writer.writerow([url, data_hora_atuais, dominio, dominio_disponivel.text])
    elif status == "Domínio disponível para candidaturas no processo de liberação .":
        # Captura a informação de liberação
        info_liberacao = driver.find_element(By.XPATH, element_liberacao).text
        data_liberacao = re.search(
            r"\d{2}/\d{2}/\d{4} \d{2}:\d{2}:\d{2}", info_liberacao
        ).group()

        # Escreve as informações no arquivo CSV
        writer.writerow(
            [url, data_hora_atuais, dominio, "Processo de Liberação", data_liberacao]
        )
    else:
        # Caso o domínio esteja disponível, registra essa informação
        writer.writerow([url, data_hora_atuais, dominio, "Domínio Disponível", ""])

# Aguardar 3 segundos
time.sleep(3)

# Encerrar o webdriver
driver.quit()
