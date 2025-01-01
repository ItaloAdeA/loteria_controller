# Preparar Arquivos para Análise de Loteria

Este script prepara os dados necessários para a análise e criação de sugestões de jogos de loteria com base nos resultados anteriores.

## Descrição

O script `preparar_arquivos.py` lê os dados de um arquivo Excel contendo os resultados anteriores da loteria e realiza diversas análises para gerar arquivos de referência que serão utilizados na criação de sugestões de jogos.

## Funcionalidades

- Verificar quais números mais saem em conjunto dado um número específico.
- Analisar a ocorrência de pares e ímpares no mesmo jogo.
- Verificar números repetidos no próximo jogo.
- Verificar quais números mais saem no próximo jogo dado um número específico.
- Verificar ciclos das dezenas.

## Estrutura do Código

O script contém a classe `AnaliseLoteria` com os seguintes métodos:

- `__init__(self, arquivo_xlsx: str, quantidade_numeros_sorteio: int, maior_numero_apostavel: int)`: Inicializa a classe com os dados do arquivo Excel.
- `verificar_qual_numero_mais_sai_em_conjunto_dado_um_numero(self)`: Gera um arquivo CSV com a contagem de números que mais saem em conjunto dado um número específico.
- `analisar_ocorrencias_de_pares_impares_no_mesmo_jogo(self)`: Gera um arquivo CSV com a contagem de pares e ímpares no mesmo jogo.
- `verificar_numero_repitidos_proximo_jogo(self)`: Gera um arquivo CSV com a contagem de números repetidos no próximo jogo.
- `verificar_quais_numeros_que_mais_saim_no_proximo_jogo_dado_um_numero(self)`: Gera um arquivo CSV com a contagem de números que mais saem no próximo jogo dado um número específico.
- `verificar_ciclos_das_dezenas(self)`: Gera um arquivo CSV com a média dos ciclos das dezenas.
- `executar_todas_analises(self)`: Executa todas as análises acima e gera os arquivos CSV correspondentes.

## Como Usar

1. Certifique-se de ter o Python instalado em sua máquina.
2. Instale as dependências necessárias:
    ```sh
    pip install pandas
    ```
3. Altere o caminho do arquivo Excel no exemplo de uso para o caminho do seu arquivo de resultados da loteria:
    ```python
    arquivo_xlsx = "C:/Users/italo/Downloads/Lotofácil (7).xlsx"
    ```
4. Execute o script:
    ```sh
    python preparar_arquivos.py
    ```

## Exemplo de Uso

```python
arquivo_xlsx = "C:/Users/italo/Downloads/Lotofácil (7).xlsx"
quantidade_numeros_sorteio = 15
maior_numero_apostavel = 25

analise = AnaliseLoteria(arquivo_xlsx, quantidade_numeros_sorteio, maior_numero_apostavel)
analise.executar_todas_analises()
```
# Gerar Sugestões de Jogos de Loteria

Este script gera sugestões de jogos de loteria com base nos resultados anteriores e nas análises realizadas pelo script `preparar_arquivos.py`.

## Descrição

O script `sugestao_jogos.py` utiliza os arquivos de referência gerados pelo script `preparar_arquivos.py` para criar sugestões de jogos de loteria. Ele analisa os números prováveis de sair no próximo jogo, os números que mais saem em conjunto, e os ciclos das dezenas para montar as sugestões de jogos.

## Funcionalidades

- Analisar os números prováveis de sair no próximo jogo.
- Analisar os números que mais saem em conjunto.
- Analisar os ciclos das dezenas.
- Montar jogos com base na análise de pares e ímpares.
- Montar jogos com base nos primeiros números prováveis de sair em conjunto.
- Gerar arquivos CSV com as sugestões de jogos.

## Estrutura do Código

O script contém as seguintes funções:

- `numeros_provaveis_de_sair_proximo_jogo(ultimo_jogo: list[int], maior_numero_apostavel: int) -> list[int]`: Analisa os números prováveis de sair no próximo jogo.
- `numeros_provaveis_de_sair_em_conjunto(analise_prox_jogo: list[int], maior_numero_apostavel: int) -> list[list[int]]`: Analisa os números que mais saem em conjunto.
- `analisar_ciclo_dezenas(maior_numero_apostavel, arquivo_xlsx: str, quantidade_numeros_sorteados: int, corretor_media_ciclos: int) -> list[int]`: Analisa os ciclos das dezenas.
- `montar_chave(lista_numeros: list[int], separador: str) -> str`: Monta uma chave de jogo a partir de uma lista de números.
- `montar_jogo_com_base_nos_numeros_impares_pares(lista_numeros: list[int], quantidade_numeros_apostada: int) -> list[list[int]]`: Monta jogos com base na análise de pares e ímpares.
- `montar_jogos_com_base_primeiros_numeros_provaveis_de_sair_em_conjunto(analise_prox_jogo: list[int], maior_numero_apostavel: int, quantidade_numeros_apostada: int) -> list[str]`: Monta jogos com base nos primeiros números prováveis de sair em conjunto.
- `montar_list_dict_para_dataframe(lista_jogos: list[list[int]], numeros_que_faltam: list[int]) -> list[dict]`: Monta uma lista de dicionários para criar um DataFrame.
- `montar_dataframe(lista_dict: list[dict], quantidade_jogos_desejados: int) -> pd.DataFrame`: Monta um DataFrame a partir de uma lista de dicionários.
- `execute_sugestao_jogos(ultimo_jogo: list[int], maior_numero_apostavel: int, quantidade_numeros_apostada: int, quantidade_numeros_sorteados: int, arquivo_xlsx: str, quantidade_jogos_desejados: int, corretor_media_ciclos: int) -> list[list[int]]`: Executa a geração de sugestões de jogos.

## Como Usar

1. Certifique-se de ter o Python instalado em sua máquina.
2. Instale as dependências necessárias:
    ```sh
    pip install pandas
    ```
3. Altere o caminho dos arquivos de referência e do arquivo Excel no exemplo de uso para os caminhos corretos:
    ```python
    ultimo_jogo = [2, 4, 5, 8, 10, 11, 12, 14, 15, 17, 18, 20, 22, 24, 25]
    maior_numero_apostavel = 25
    quantidade_numeros_apostada = 17
    quantidade_numeros_sorteados = 15
    arquivo_xlsx = "C:/Users/italo/Downloads/Lotofácil (7).xlsx"
    quantidade_jogos_desejados = 200
    corretor_media_ciclos = 2
    chaves = execute_sugestao_jogos(
        ultimo_jogo, 
        maior_numero_apostavel, 
        quantidade_numeros_apostada,
        quantidade_numeros_sorteados,
        arquivo_xlsx, 
        quantidade_jogos_desejados,
        corretor_media_ciclos
    )
    ```
4. Execute o script:
    ```sh
    python sugestao_jogos.py
    ```

## Saída

O script gerará os seguintes arquivos CSV na pasta `src`:

- `sugestao_jogos_spec.csv`: Contém as sugestões de jogos com a quantidade de números que faltam em cada jogo.
- `sugestao_jogos.csv`: Contém as sugestões de jogos sem a quantidade de números que faltam.

---

Espero que isso ajude! Se precisar de mais alguma coisa, estou à disposição.