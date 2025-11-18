from constantes.constantes import CAMINHO_ARQUIVO, TRUSTED, LANDING
import pandas as pd
import os
from datetime import datetime

class ManipulationTrustedMetasNewgate:

    def executar(self):
        '''Lê os CSVs mensais extraídos e consolida em um único CSV no trusted.'''

        df_concat = self.ler_csv()

        df_renamed = self.estruturar_dados(df_concat)

        df = self.salvar_dataframe(df_renamed)

        return df
    
    def ler_csv(self):
        dfs = []
        columns = None

        caminho_pasta = f"{CAMINHO_ARQUIVO}/{LANDING}/newgate"
        semana_atual = datetime.now().isocalendar()[1]

        for semana in range(1, semana_atual + 1):
            nome_arquivo = f"{caminho_pasta}/metas_newgate_2025_semana_{semana:02d}.csv"
            if not os.path.exists(nome_arquivo):
                print(f"Arquivo não encontrado: {nome_arquivo}")
                continue
            # Verifica se o arquivo está vazio
            if os.path.getsize(nome_arquivo) == 0:
                print(f"Arquivo vazio: {nome_arquivo}")
                continue
            if columns is None:
                try:
                    df = pd.read_csv(nome_arquivo, header=0)
                except pd.errors.EmptyDataError:
                    print(f"Arquivo sem dados ou corrompido: {nome_arquivo}")
                    continue
                columns = df.columns
                if (df.iloc[0] == columns).all():
                    df = df.iloc[1:].reset_index(drop=True)
            else:
                # Verifica se o arquivo está vazio antes de ler sem header
                if os.path.getsize(nome_arquivo) == 0:
                    print(f"Arquivo vazio: {nome_arquivo}")
                    continue
                try:
                    df = pd.read_csv(nome_arquivo, header=None)
                except pd.errors.EmptyDataError:
                    print(f"Arquivo sem dados ou corrompido: {nome_arquivo}")
                    continue
                if df.empty:
                    print(f"Arquivo sem dados: {nome_arquivo}")
                    continue
                df.columns = columns
            dfs.append(df)
        if dfs:
            df_concat = pd.concat(dfs, ignore_index=True)
            print(df_concat.head())
            return df_concat
        else:
            print("Nenhum arquivo encontrado.")
            return pd.DataFrame()

    def estruturar_dados(self, df: pd.DataFrame):
        # Normaliza a coluna Aluno
        df['Aluno'] = df['Aluno'].str.strip().str.lower().str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')
        df['Mentor'] = df['Mentor'].str.strip().str.lower().str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')

        # modificar nomes das colunas
        df_renamed = df.rename(columns={
            'Aluno': 'nome_aluno_newgate',
            'Meta': 'meta_semanal',
            'Cumprimento': '%_cumprida',
            'Total': 'total_estipulado',
            'Semana': 'semana_ano'
        })

        return df_renamed

    def salvar_dataframe(self, df_renamed: pd.DataFrame):
        caminho_trusted = f"{CAMINHO_ARQUIVO}/{TRUSTED}/newgate"
        nome_arquivo = f"{caminho_trusted}/trusted_metas_newgate_2025.csv"
        df_renamed.to_csv(nome_arquivo, index=False)
        print(f"Arquivo salvo em: {nome_arquivo}")

        return df_renamed

# if __name__ == "__main__":
#     manipulador = ManipulationTrustedMetasNewgate()
#     manipulador.executar()