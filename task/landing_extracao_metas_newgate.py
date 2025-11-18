import requests
import re
import json
import pandas as pd
import time
from bs4 import BeautifulSoup
from datetime import datetime
from constantes.constantes import HEADERS_LOGIN,\
                                            URL,\
                                            URL_METAS,\
                                            HEADERS_METAS, \
                                            SEMANAS, \
                                            ANO, \
                                            PAYLOAD_LOGIN,\
                                            PAYLOAD_METAS,\
                                            CAMINHO_ARQUIVO,\
                                            LANDING


class ExtracaoApiNewGate():
    def executar(self) -> pd.DataFrame:
        for semana_do_ano in SEMANAS:
            print(f"Extraindo dados da semana {semana_do_ano} do ano {ANO}")
            self.extracao(semana_do_ano)

    def extracao(self, semana_do_ano: str) -> pd.DataFrame:
        # Caminho para o arquivo config.json
        config_file = "config.json"

        # Carregar o JSON do arquivo
        with open(config_file, 'r') as file:
            config = json.load(file)

        # Acessar os valores de username e password
        username = config['login_newgate']['username']
        password = config['login_newgate']['password']

        session = requests.Session()

        payload_login = PAYLOAD_LOGIN.copy()

        payload_login['username'] = username
        payload_login['password'] = password

        # Obtendo CSRFTOKEN
        response = session.get(URL, headers=HEADERS_LOGIN, params=payload_login)

        if response.status_code != 200:
            print(f"Erro ao obter a resposta da URL: {response.status_code}")
            exit()

        # Regex para capturar apenas o value do csrfmiddlewaretoken
        token_match = re.search(r'{"access_token":"([^"]+)","token_type":"([^"]+)"}', response.content.decode('utf-8'))

        if token_match:
                    access_token = token_match.group(1)
                    token_type = token_match.group(2)
                    print("Access Token:", access_token)
                    print("Token Type:", token_type)
        else:
            print("Tokens não encontrados.")

        print(f"semana={semana_do_ano} e ano={ANO}" )

        payload_metas = PAYLOAD_METAS.copy()
        payload_metas['semana'] = semana_do_ano
        payload_metas['ano'] = ANO
        time.sleep(10)  # Atraso de 10 segundos entre as requisições

        response = session.get(URL_METAS, headers=HEADERS_METAS, params=payload_metas)
        if response.status_code != 200:
            print(f"Erro ao obter a resposta da URL: {response.status_code}")
            exit()
        # print(f"response={response}")
        data = response.json()

        print(data)

        #Extraindo os dados necessários do JSON
        detalhes = data["detalhes"]
        dados = [{
            "Mentor": item["nome_mentor"],
            "Aluno": item["nome_estudante"],
            "Cumprimento": item["cumprimento"],
            "Total": item["numero_total_metas"],
            "Semana": item["semana"],

        } for item in detalhes]

        # Criando o DataFrame
        df = pd.DataFrame(dados)

        #Salvar em csv com nome dinâmico na pasta storage
        nome_arquivo = f"{CAMINHO_ARQUIVO}/{LANDING}/newgate/metas_newgate_{ANO}_semana_{int(semana_do_ano):02d}.csv"
        df.to_csv(nome_arquivo, index=False)
        print(f"Arquivo salvo como: {nome_arquivo}")

        return df
    
# if __name__ == "__main__":
#     extrator = ExtracaoApiNewGate()
#     extrator.executar()