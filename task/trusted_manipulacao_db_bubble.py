from constantes.constantes import CAMINHO_ARQUIVO, TRUSTED, LANDING
import pandas as pd

class ManipulationTrustedDbBubble:

    def executar(self):
        '''Lê os CSVs mensais extraídos e consolida em um único CSV no trusted.'''

        df_concat = self.ler_csv()

        df_renamed = self.estruturar_dados(df_concat)

        df = self.salvar_dataframe(df_renamed)

        return df
    
    def ler_csv(self):
        dfs = []
        columns = None
        for mes in range(1, 10):
            caminho_arquivo = f"{CAMINHO_ARQUIVO}/{LANDING}/bubble/db_2025_{mes:02d}.csv"
            if mes == 1:
                df = pd.read_csv(caminho_arquivo, header=0)
                columns = df.columns
                # Remove a primeira linha se ela for um cabeçalho duplicado
                if (df.iloc[0] == columns).all():
                    df = df.iloc[1:].reset_index(drop=True)
            else:
                df = pd.read_csv(caminho_arquivo, header=None)
                df.columns = columns
            dfs.append(df)
        df_concat = pd.concat(dfs, ignore_index=True)
        print(df_concat.head())

        return df_concat

    def estruturar_dados(self, df: pd.DataFrame):
        # Normaliza a coluna nomeDeAluno
        df['nomeDeAluno'] = df['nomeDeAluno'].str.strip().str.lower().str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')
        # modificar nomes das colunas
        df_renamed = df.rename(columns={
            'nomeDeAluno': 'nome_aluno_bubble',
            'Emocional_alunos': 'emocional_aluno',
            'conteúdoMinistrado': 'conteudo_ministrado',
            'dificuldadesApresentadas': 'dificuldades_encontradas',
            'sanardificuldades': 'resolucao_dificuldades',
            'Duracao_da_Aula': 'duracao_aula',
            'StatusAcompanhamento': 'feedback_aula'
        })
        # Criar coluna semana_ano com base na coluna data_aula
        df_renamed['data_aula'] = pd.to_datetime(df_renamed['data_aula'], errors='coerce')
        df_renamed['semana_ano'] = df_renamed['data_aula'].dt.isocalendar().week.astype(str)

        df_renamed = df_renamed.drop(columns=['aula_foi_reposicao','id_mentor'])

        # Retirar linhas com semana_ano nulo
        df_renamed = df_renamed[df_renamed['feedback_aula'] != 'StatusAcompanhamento']

        # converter semana_ano para inteiro
        df_renamed.loc[:, 'semana_ano'] = df_renamed['semana_ano'].astype(int)

        return df_renamed

    def salvar_dataframe(self, df_renamed: pd.DataFrame):
        caminho_trusted = f"{CAMINHO_ARQUIVO}/{TRUSTED}/bubble"
        nome_arquivo = f"{caminho_trusted}/trusted_db_bubble_2025.csv"

        df_renamed.to_csv(nome_arquivo, index=False, encoding="utf-8")

        print(f"Salvo: {nome_arquivo} ({len(df_renamed)} linhas)")

        return df_renamed

# if __name__ == "__main__":
#     manipulador = ManipulationTrustedDbBubble()
#     manipulador.executar()