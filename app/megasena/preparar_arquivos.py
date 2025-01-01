import pandas as pd

class AnaliseLoteria:
    def __init__(self, arquivo_xlsx: str, quantidade_numeros_sorteio: int, maior_numero_apostavel: int):
        self.data = pd.read_excel(arquivo_xlsx)
        self.quantidade_numeros_sorteio = quantidade_numeros_sorteio
        self.maior_numero_apostavel = maior_numero_apostavel
        self.colunas = [f'Bola{i}' for i in range(1, quantidade_numeros_sorteio + 1)]
        self.df = self.data[self.colunas]
        self.total_linhas = len(self.df.index)

    def verificar_qual_numero_mais_sai_em_conjunto_dado_um_numero(self):
        dic = {}
        for i in range(self.maior_numero_apostavel):
            numero_analise = i + 1
            lista_numeros = [0] * self.maior_numero_apostavel

            for n_linha in range(self.total_linhas):
                linha = self.df.loc[n_linha].tolist()
                if numero_analise in linha:
                    for numero in linha:
                        if numero != numero_analise:
                            lista_numeros[numero - 1] += 1

            dic[f'dado{i + 1}'] = lista_numeros

        df_final = pd.DataFrame(dic)
        df_final.to_csv('arquivos_referencias/contagem_saida_dado_numero_no_mesmo_jogo.csv', index=False)

    def analisar_ocorrencias_de_pares_impares_no_mesmo_jogo(self):
        results = dict()
        for n_linha in range(self.total_linhas):
            linha = self.df.loc[n_linha].tolist()
            qtd_impar = sum(1 for numero in linha if numero % 2 != 0)
            qtd_par = len(linha) - qtd_impar
            chave = f'PARES={qtd_par}/IMPARES={qtd_impar}'
            dict_rela= {
                'PARES': qtd_par,
                'IMPARES': qtd_impar,
                'RECORRENCIA': 1
            }
            if chave not in results:
                results[chave] = dict_rela
            else:
                results[chave]['RECORRENCIA'] += 1

        lista_df = []
        for chave, dic in results.items():
            lista_df.append(dic)

        df_final = pd.DataFrame(lista_df)
        df_final.to_csv('arquivos_referencias/contagem_pares_impares_mesmo_jogo.csv', index=False)

    def verificar_numero_repitidos_proximo_jogo(self):
        dic = {}
        for i in range(self.maior_numero_apostavel):
            numero_analise = i + 1
            pontos = 0

            for n_linha in range(self.total_linhas):
                linha = self.df.loc[n_linha].tolist()
                if numero_analise in linha and n_linha + 1 < self.total_linhas:
                    prox_linha = self.df.loc[n_linha + 1].tolist()
                    if numero_analise in prox_linha:
                        pontos += 1

            dic[f'numero_{i + 1}'] = pontos

        df_final = pd.DataFrame(dic, index=[0])
        df_final.to_csv('arquivos_referencias/cotagem_de_numeros_repitidos_prox_jogo.csv', index=False)

    def verificar_quais_numeros_que_mais_saim_no_proximo_jogo_dado_um_numero(self):
        dic = {}
        for i in range(self.maior_numero_apostavel):
            numero_analise = i + 1
            lista_numeros = [0] * self.maior_numero_apostavel

            for n_linha in range(self.total_linhas):
                linha = self.df.loc[n_linha].tolist()
                if numero_analise in linha and n_linha + 1 < self.total_linhas:
                    prox_linha = self.df.loc[n_linha + 1].tolist()
                    for numero in prox_linha:
                        lista_numeros[numero - 1] += 1

            dic[f'dado{i + 1}'] = lista_numeros

        df_final = pd.DataFrame(dic)
        df_final.to_csv('arquivos_referencias/contagem_dado_um_numero_qual_numero_mais_sai_prox_jogo.csv', index=False)

    def verificar_ciclos_das_dezenas(self):
        ciclos = []
        contagem_jogos = 0
        lista_numeros = [0] * self.maior_numero_apostavel

        for n_linha in range(self.total_linhas):
            linha = self.df.loc[n_linha].tolist()
            for numero in linha:
                if lista_numeros[numero - 1] == 0:
                    lista_numeros[numero - 1] += 1

            contagem_jogos += 1
            if 0 not in lista_numeros:
                lista_numeros = [0] * self.maior_numero_apostavel
                ciclos.append(contagem_jogos)
                contagem_jogos = 0

        media = sum(ciclos) / len(ciclos) if ciclos else 0
        dic = {"media_ciclos": media}
        df_final = pd.DataFrame(dic, index=[0])
        df_final.to_csv('arquivos_referencias/media_ciclos_das_dezenas.csv', index=False)

    def executar_todas_analises(self):
        self.verificar_qual_numero_mais_sai_em_conjunto_dado_um_numero()
        self.analisar_ocorrencias_de_pares_impares_no_mesmo_jogo()
        self.verificar_numero_repitidos_proximo_jogo()
        self.verificar_quais_numeros_que_mais_saim_no_proximo_jogo_dado_um_numero()
        self.verificar_ciclos_das_dezenas()

# Exemplo de uso
arquivo_xlsx = "C:/Users/italo/Downloads/Mega-Sena (2).xlsx"
quantidade_numeros_sorteio = 6
maior_numero_apostavel = 60

analise = AnaliseLoteria(arquivo_xlsx, quantidade_numeros_sorteio, maior_numero_apostavel)
analise.executar_todas_analises()