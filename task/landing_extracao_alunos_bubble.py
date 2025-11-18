import requests
import json
import pandas as pd

from constantes.constantes import COLUNAS_DESEJADAS_ALUNO, \
                    CAMINHO_ARQUIVO, \
                    APP_URL, \
                    DATA_TYPE,\
                    LANDING

class ExtracaoDadosBubbleAliunoMentor():
    """
    Classe para extração e processamento de dados de alunos ativos via API Bubble.

    Esta classe realiza a busca dos alunos ativos, normaliza os dados recebidos,
    seleciona apenas as colunas relevantes e salva o resultado em um arquivo CSV.

    Métodos:
        - executar(): Inicia o processo de extração e retorna o DataFrame resultante.
        - tab_usuarios(): Realiza a requisição, tratamento e salvamento dos dados.
    """
    def executar(self):
        '''Executa a rotina de extração de dados'''
        df_alunos = self.tab_usuarios()
        return df_alunos

    def tab_usuarios(self) -> pd.DataFrame:
        '''Busca, processa e salva os dados dos alunos ativos da API Bubble'''
        lista_papel = ["Aluno"]

        for papel in lista_papel:
            cursor = 0
            has_more = True
            todos_os_registros = []

            while has_more:
                constraints = [
                    {"key": "papel", "constraint_type": "equals", "value": f"{papel}"},
                    {"key": "status", "constraint_type": "equals", "value": "Ativo"}
                ]
                response = requests.get(
                    f'{APP_URL}/{DATA_TYPE}',
                    params={
                        'cursor': cursor,
                        'constraints': json.dumps(constraints)
                    }
                )
                if response.status_code == 200:
                    data = response.json()
                    registros = data.get('response', {}).get('results', [])
                    todos_os_registros.extend(registros)
                    has_more = data.get('response', {}).get('remaining', 0) > 0
                    cursor += 100
                else:
                    print(f'Erro: {response.status_code}, Detalhes: {response.text}')
                    has_more = False

            df = pd.DataFrame(todos_os_registros)
            authentication_df = pd.json_normalize(df["authentication"])
            df = pd.concat([df, authentication_df], axis=1).drop(columns=["authentication"])

            if papel == "Aluno":
                df = df[COLUNAS_DESEJADAS_ALUNO]
                df.rename(columns={'_id': 'id_aluno'}, inplace=True)
                df_alunos = df

        nome_arquivo = f"{CAMINHO_ARQUIVO}/{LANDING}/user/alunos_ativos.csv"
        df.to_csv(nome_arquivo, index=False)
        print(f"Arquivo salvo como: {nome_arquivo}")

        return df_alunos

# if __name__ == "__main__":
#     extrator = ExtracaoDadosBubbleAliunoMentor()
#     extrator.executar()