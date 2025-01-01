from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

def listas_jogos_df(arquivo_csv: str) -> list[list[int]]:
    df = pd.read_csv(arquivo_csv, sep=',')
    lista_jogos = list()
    for i in range(len(df)):
        jogo = list(df.iloc[i])
        lista_jogos.append(jogo)

    return lista_jogos

navegador = webdriver.Chrome()
navegador.get('https://www.loteriasonline.caixa.gov.br')
input('Pressione ENTER para continuar...')

listas_xpath = [f'//*[@id="n{str(n).zfill(2)}"]' for n in range(1, 61)]
colocar_no_carrinho = """//*[@id="colocarnocarrinho"]"""
    
caminho_arquivo_jogos = 'C:/Users/italo/Documents/codpy/analise_loteria/megasena/src/sugestao_jogos.csv'
lista_jogos = listas_jogos_df(caminho_arquivo_jogos)

for jogo in lista_jogos:
    for numero in jogo:
        try:
            # Esperar até que o elemento esteja presente
            elemento = WebDriverWait(navegador, 10).until(
                EC.presence_of_element_located((By.XPATH, listas_xpath[numero - 1]))
            )
            # Rolar até o elemento
            navegador.execute_script("arguments[0].scrollIntoView();", elemento)
            # Clicar no elemento
            elemento.click()
        except Exception as e:
            print(f"Erro ao clicar no número {numero}: {e}")

    navegador.find_element(By.XPATH, colocar_no_carrinho).click()

    input('Pressione ENTER para continuar...')