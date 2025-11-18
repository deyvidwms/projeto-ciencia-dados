import os
import json
from datetime import datetime, timezone

import requests
import pandas as pd
from constantes.constantes import APP_URL, DATA_TYPE_DB, API_TOKEN, COLUNAS_DESEJADAS_DB, CAMINHO_ARQUIVO, LANDING


class ExtracaoDadosBubbleDiarioBordo():
    """
    ExtracaoDadosBubbleDiarioBordo extrai registros de diários de bordo do Bubble para o ano de 2025, salvando um arquivo CSV por mês.

    Classes:
        ExtracaoDadosBubbleDiarioBordo:
            - __init__(): Inicializa a sessão HTTP, define diretório de saída e garante sua existência.
            - executar(): Percorre os meses de 2025, busca registros do Bubble para cada mês, ajusta e salva os dados em CSV.
            - _intervalo_mes_iso(ano, mes): Retorna tupla com datas ISO UTC de início e fim exclusivo do mês especificado.
            - _buscar_intervalo(inicio_iso, fim_iso): Busca registros do Bubble no intervalo informado, com paginação, e retorna DataFrame.

    O script garante que todos os meses de 2025 sejam processados, ajustando colunas conforme necessário e lidando com possíveis erros de requisição.
    """
    '''Extrai diários de bordo do Bubble e salva um CSV por mês de 2025.'''

    def __init__(self):
        super().__init__()
        self.session = requests.Session()
        self.base_dir = f"{CAMINHO_ARQUIVO}/{LANDING}/bubble"
        os.makedirs(self.base_dir, exist_ok=True)

    def executar(self):
        '''Executa a extração mês a mês (jan–dez 2025).'''
        for mes in range(1, 13):
            inicio_iso, fim_iso = self._intervalo_mes_iso(2025, mes)
            print(f"\nProcessando {inicio_iso[:7]} ...")
            df_mes = self._buscar_intervalo(inicio_iso, fim_iso)

            if df_mes is None or df_mes.empty:
                print(f"Nenhum registro para {inicio_iso[:7]}.")
                continue

            # Ajusta colunas faltantes para não dar KeyError
            existentes = set(df_mes.columns)
            faltantes = [c for c in COLUNAS_DESEJADAS_DB if c not in existentes]
            if faltantes:
                print(f"Criando colunas faltantes: {faltantes}")
                for c in faltantes:
                    df_mes[c] = pd.NA

            # Reordena as colunas
            df_mes = df_mes[COLUNAS_DESEJADAS_DB]

            # Renomeia colunas principais
            df_mes = df_mes.rename(columns={
                'Created By': 'id_mentor',
                '_id': 'id_diario_bordo'
            })

            # Salvar com mês no nome
            nome_arquivo = os.path.join(self.base_dir, f"db_2025_{mes:02d}.csv")
            df_mes.to_csv(nome_arquivo, index=False, encoding="utf-8")
            print(f"Salvo: {nome_arquivo} ({len(df_mes)} linhas)")

    def _intervalo_mes_iso(self, ano: int, mes: int) -> tuple[str, str]:
        '''Retorna (início, fim_exclusivo) ISO UTC para o mês.'''
        inicio = datetime(ano, mes, 1, 0, 0, 0, tzinfo=timezone.utc)
        fim = datetime(ano if mes < 12 else ano + 1,
                       mes + 1 if mes < 12 else 1,
                       1, 0, 0, 0, tzinfo=timezone.utc)
        return inicio.strftime("%Y-%m-%dT%H:%M:%SZ"), fim.strftime("%Y-%m-%dT%H:%M:%SZ")

    def _buscar_intervalo(self, inicio_iso: str, fim_iso: str):
        '''Busca registros no intervalo [inicio_iso, fim_iso) com paginação.'''
        cursor = 0
        has_more = True
        todos = []

        print(f"🔎 Janela: {inicio_iso} .. {fim_iso} (fim exclusivo)")

        while has_more:
            constraints = [
                {"key": "data_aula", "constraint_type": "greater than", "value": inicio_iso},
                {"key": "data_aula", "constraint_type": "less than",     "value": fim_iso},
            ]
            headers = {"Authorization": f"Bearer {API_TOKEN}", "Content-Type": "application/json"}
            params = {"cursor": cursor, "constraints": json.dumps(constraints)}

            resp = self.session.get(f"{APP_URL}/{DATA_TYPE_DB}", params=params, headers=headers)
            if resp.status_code == 200:
                data = resp.json()
                results = data.get("response", {}).get("results", [])
                todos.extend(results)
                print(f"Página {cursor//100 + 1}: {len(results)} registros")
                has_more = data.get("response", {}).get("remaining", 0) > 0
                cursor += 100
            else:
                print(f"Erro {resp.status_code}: {resp.text}")
                return None

        df = pd.DataFrame(todos)
        print(f"Total no intervalo: {len(df)}")
        if df.empty:
            return None

        # Debug: primeiras colunas recebidas
        print(f"Colunas recebidas ({len(df.columns)}): {sorted(df.columns.tolist())[:10]}{' ...' if len(df.columns)>10 else ''}")
        return df


# if __name__ == "__main__":
#     ExtracaoDadosBubbleDiarioBordo().executar()
