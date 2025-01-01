import pandas as pd

def numeros_provaveis_de_sair_proximo_jogo(ultimo_jogo: list[int], maior_numero_apostavel: int) -> list[int]:
    
    caminho_arquivo_ref = "C:/Users/italo/Documents/codpy/analise_loteria/megasena/src/arquivos_referencias/contagem_dado_um_numero_qual_numero_mais_sai_prox_jogo.csv"
    df = pd.read_csv(caminho_arquivo_ref)

    dicinario = {
        f"{i + 1}": 0 for i in range(maior_numero_apostavel)
    }

    for numero in ultimo_jogo:
        coluna_df = df[f"dado{numero}"]
        for i in range(maior_numero_apostavel):
            linha = coluna_df.iloc[i]
            dicinario[f"{i + 1}"] += linha


    dicinario = dict(sorted(dicinario.items(), key=lambda item: item[1], reverse=True))
    numeros = list(dicinario.keys())
    numeros = [int(numero) for numero in numeros]

    return numeros

def numeros_provaveis_de_sair_em_conjunto(analise_prox_jogo: list[int], maior_numero_apostavel: int) -> list[list[int]]:
    
    caminho_arquivo_ref = "C:/Users/italo/Documents/codpy/analise_loteria/megasena/src/arquivos_referencias/contagem_saida_dado_numero_no_mesmo_jogo.csv"
    df = pd.read_csv(caminho_arquivo_ref)

    dicinario = {
        f"{i + 1}": 0 for i in range(maior_numero_apostavel)
    }

    lista_numeros = []
    for numero in analise_prox_jogo:
        dicinario = {
        f"{i + 1}": 0 for i in range(maior_numero_apostavel)
    }
        coluna_df = df[f"dado{numero}"]
        for i in range(maior_numero_apostavel):
            linha = coluna_df.iloc[i]
            dicinario[f"{i + 1}"] += linha
        dicinario = dict(sorted(dicinario.items(), key=lambda item: item[1], reverse=True))
        numeros = list(dicinario.keys())
        numeros = [int(numero) for numero in numeros]
        lista_numeros.append(numeros)

    return lista_numeros

def analisar_ciclo_dezenas(maior_numero_apostavel, arquivo_xlsx: str, quantidade_numeros_sorteados: int, corretor_media_ciclos: int) -> list[int]:
    
    caminho_arquivo_ref = "C:/Users/italo/Documents/codpy/analise_loteria/megasena/src/arquivos_referencias/media_ciclos_das_dezenas.csv"
    df = pd.read_csv(caminho_arquivo_ref)
    media_ciclos = round(df["media_ciclos"].values[0]) - corretor_media_ciclos

    df = pd.read_excel(arquivo_xlsx)
    colunas = [f'Bola{i}' for i in range(1, quantidade_numeros_sorteados + 1)]
    df = df[colunas]
    df = df.tail(media_ciclos)
    numeros = list()
    for index in df.index.tolist():
        lista = df.loc[index].tolist()
        for numero in lista:
            if numero not in numeros:
                numeros.append(numero)
    
    numeros_que_faltam = list()
    for i in range(1, maior_numero_apostavel + 1):
        if i not in numeros:
            numeros_que_faltam.append(i)

    return numeros_que_faltam

def montar_chave(lista_numeros: list[int], separador: str) -> str:
    return f"{separador}".join([str(numero) for numero in lista_numeros])

def montar_jogo_com_base_nos_numeros_impares_pares(lista_numeros: list[int], quantidade_numeros_apostada: int) -> list[list[int]]:

    df_pares_impar = pd.read_csv("C:/Users/italo/Documents/codpy/analise_loteria/megasena/src/arquivos_referencias/contagem_pares_impares_mesmo_jogo.csv")
    df_pares_impar = df_pares_impar.sort_values(by="RECORRENCIA", ascending=False)
    media_recorrencia = round(df_pares_impar["RECORRENCIA"].mean())

    numeros_pares = [numero for numero in lista_numeros if numero % 2 == 0]
    numeros_impares = [numero for numero in lista_numeros if numero % 2 != 0]
    chaves_jogos = []
    for i in range(len(df_pares_impar)):
        linha = df_pares_impar.iloc[i]
        qtd_pares = linha["PARES"]
        qtd_impares = linha["IMPARES"]

        if qtd_pares + qtd_impares < quantidade_numeros_apostada:
            restante = quantidade_numeros_apostada - (qtd_pares + qtd_impares)
            if qtd_pares < qtd_impares:
                qtd_pares += restante
            else:
                qtd_impares += restante

        if linha["RECORRENCIA"] < media_recorrencia:
            break
        
        n_pares_jogo = numeros_pares[:qtd_pares]
        n_impares_jogo = numeros_impares[:qtd_impares]
        jogo = n_pares_jogo + n_impares_jogo
        chave_jogo = montar_chave(sorted(jogo), ",")
        chaves_jogos.append(chave_jogo)
    
    return chaves_jogos

def montar_jogos_com_base_primeiros_numeros_provaveis_de_sair_em_conjunto(analise_prox_jogo: list[int], maior_numero_apostavel: int, quantidade_numeros_apostada: int) -> list[str]:

    chaves_jogos = []
    for numero in analise_prox_jogo:
        jogo = [numero]
        numero_analise = numero
        while True:
            
            lista_numeros = numeros_provaveis_de_sair_em_conjunto([numero_analise], maior_numero_apostavel)[0]
            
            for i, n in enumerate(lista_numeros):
                if n not in jogo:
                    jogo.append(n)
                    break
                else:
                    continue

            if len(jogo) == quantidade_numeros_apostada:
                break

            numero_analise = lista_numeros[i]

        chave = montar_chave(sorted(jogo), ",")
        if chave not in chaves_jogos:
            chaves_jogos.append(chave)

    return chaves_jogos

def montar_list_dict_para_dataframe(lista_jogos: list[list[int]], numeros_que_faltam: list[int]) -> list[dict]:
    lista_dict = []
    for jogo in lista_jogos:
        dicionario = {
            f"bola_{i+1}": jogo[i] for i in range(len(jogo))
        }
        dicionario["qtd_n_faltas_jogo"] = len([numero for numero in jogo if numero in numeros_que_faltam])
        lista_dict.append(dicionario)
    
    return lista_dict

def montar_dataframe(lista_dict: list[dict], quantidade_jogos_desejados: int) -> pd.DataFrame:

    lista_dict = lista_dict[:quantidade_jogos_desejados]
    df_final = pd.DataFrame(lista_dict)

    return df_final
    
def execute_sugestao_jogos(
        ultimo_jogo: list[int], 
        maior_numero_apostavel: int, 
        quantidade_numeros_apostada: int,
        quantidade_numeros_sorteados: int,
        arquivo_xlsx: str, 
        quantidade_jogos_desejados: int, 
        corretor_media_ciclos: int
        ) -> list[list[int]]:

    print("Iniciando analise dos dados...")
    numeros_prox_jogo = numeros_provaveis_de_sair_proximo_jogo(ultimo_jogo, maior_numero_apostavel)
    numeros_conjunto = numeros_provaveis_de_sair_em_conjunto(numeros_prox_jogo, maior_numero_apostavel)
    numeros_que_faltam = analisar_ciclo_dezenas(maior_numero_apostavel, arquivo_xlsx, quantidade_numeros_sorteados, corretor_media_ciclos)
    
    print("Montando os jogos...")
    chaves_gerais = list()
    chaves_gerais += montar_jogo_com_base_nos_numeros_impares_pares(numeros_prox_jogo, quantidade_numeros_apostada)
    chaves_gerais += montar_jogos_com_base_primeiros_numeros_provaveis_de_sair_em_conjunto(numeros_prox_jogo, maior_numero_apostavel, quantidade_numeros_apostada)
    for numeros in numeros_conjunto:
        chaves = montar_jogo_com_base_nos_numeros_impares_pares(numeros, quantidade_numeros_apostada)
        chaves_gerais += chaves
    
    chaves_unicas = list(set(chaves_gerais))
    jogos = list()
    for chave in chaves_unicas:
        jogo_str = str(chave).split(",")
        jogo = sorted([int(numero) for numero in jogo_str])
        jogos.append(jogo)

    print("Montando arquivo...")
    lista_dict = montar_list_dict_para_dataframe(jogos, numeros_que_faltam)
    df_final = montar_dataframe(lista_dict, quantidade_jogos_desejados)
    print(len(chaves_unicas), "jogos gerados")
    df_final_spec = df_final.sort_values(by="qtd_n_faltas_jogo", ascending=False)
    df_final_spec.to_csv("C:/Users/italo/Documents/codpy/analise_loteria/megasena/src/sugestao_jogos_spec.csv", index=False)

    df_final = df_final.drop(columns=["qtd_n_faltas_jogo"])
    df_final.to_csv("C:/Users/italo/Documents/codpy/analise_loteria/megasena/src/sugestao_jogos.csv", index=False)

    return chaves_unicas

ultimo_jogo = [1,2,3,4,5,6]
maior_numero_apostavel = 60
quantidade_numeros_apostada = 6
quantidade_numeros_sorteados = 6
arquivo_xlsx = "C:/Users/italo/Downloads/Mega-Sena (1).xlsx"
quantidade_jogos_desejados = 1000
corretor_media_ciclos = 10
chaves = execute_sugestao_jogos(
    ultimo_jogo, 
    maior_numero_apostavel, 
    quantidade_numeros_apostada,
    quantidade_numeros_sorteados,
    arquivo_xlsx, 
    quantidade_jogos_desejados,
    corretor_media_ciclos
)


resu = [1,17,19,29,50,57]
for jogo in chaves:
    jogo = jogo.split(",")
    jogo = [int(numero) for numero in jogo]
    acertos = 0
    for numero in resu:
        if numero not in jogo:
            continue
        else:
            acertos += 1

    if acertos == 6:
        print(jogo, "sena")
    elif acertos == 5:
        print(jogo, "quina")
    elif acertos == 4:
        print(jogo, "quadra")

