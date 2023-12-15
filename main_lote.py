from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import csv
from datetime import datetime
import re
import pandas as pd


def processar_dominio(dominio, driver, writer, data_hora_atuais, url):
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

    # Restante do código original para processar um domínio
    driver.get(url)
    time.sleep(1)
    element = driver.find_element(By.XPATH, element_path)
    element.send_keys(element_text)
    time.sleep(1)
    button = driver.find_element(By.XPATH, element_button)
    button.click()
    time.sleep(1)

    dominio = driver.find_element(By.XPATH, element_dominio).text
    status = driver.find_element(By.XPATH, element_status).text

    # Escrever no arquivo CSV
    if status == "Domínio não disponível para registro.":
        dominios_disponiveis = driver.find_elements(By.XPATH, element_disponiveis)
        for dominio_disponivel in dominios_disponiveis:
            writer.writerow([url, data_hora_atuais, dominio, dominio_disponivel.text])
    elif status == "Domínio disponível para candidaturas no processo de liberação .":
        info_liberacao = driver.find_element(By.XPATH, element_liberacao).text
        data_liberacao = re.search(
            r"\d{2}/\d{2}/\d{4} \d{2}:\d{2}:\d{2}", info_liberacao
        ).group()
        writer.writerow(
            [url, data_hora_atuais, dominio, "Processo de Liberação", data_liberacao]
        )
    else:
        writer.writerow([url, data_hora_atuais, dominio, "Domínio Disponível", ""])


def main():
    # Carrega a lista de domínios
    df = pd.read_csv(
        "dominios_em_liberacao.csv", header=None, names=["dominio", "processado"]
    )
    df["processado"] = df["processado"].fillna("n")

    # Configurações para executar o Chrome em modo headless
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)

    with open(
        "dominios_disponiveis.csv", mode="a", newline="", encoding="utf-8"
    ) as file:
        writer = csv.writer(file)

        for index, row in df.iterrows():
            if row["processado"] == "n":
                processar_dominio(
                    row["dominio"],
                    driver,
                    writer,
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    url,
                )
                # Marca o domínio como processado
                df.at[index, "processado"] = "y"

    # Salva o progresso no arquivo CSV
    df.to_csv("dominios_em_liberacao.csv", index=False)

    # Encerrar o webdriver
    driver.quit()


if __name__ == "__main__":
    main()
