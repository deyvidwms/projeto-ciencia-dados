from constantes.constantes import CAMINHO_ARQUIVO, TRUSTED, LANDING
import pandas as pd
import os


class ManipulationTrustedUserBubble:
    def executar(self):
        '''Lê os CSVs mensais extraídos e consolida em um único CSV no trusted.'''

        df_concat = self.ler_csv()

        df_renamed = self.estruturar_dados(df_concat)

        df = self.salvar_dataframe(df_renamed)

        return df
    
    def ler_csv(self):
        caminho_pasta = f"{CAMINHO_ARQUIVO}/{LANDING}/user"
        nome_arquivo = f"{caminho_pasta}/alunos_ativos.csv"
        df = pd.read_csv(nome_arquivo)
        return df
    
    def estruturar_dados(self, df):
        df['Nome_usuário'] = df['Nome_usuário'].str.strip().str.lower().str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')
    
        df_renamed = df.rename(columns={
            'Nome_usuário': 'nome_aluno',
            'Created Date': 'data_criacao',
        })

        return df_renamed
    
    def salvar_dataframe(self, df):
        caminho_pasta = f"{CAMINHO_ARQUIVO}/{TRUSTED}/user"
        if not os.path.exists(caminho_pasta):
            os.makedirs(caminho_pasta)
        nome_arquivo = f"{caminho_pasta}/alunos_ativos.csv"

        df.to_csv(nome_arquivo, index=False)
        print(f"Arquivo salvo em: {nome_arquivo}")
        return df
    
# if __name__ == "__main__":
#     manipulador = ManipulationTrustedUserBubble()
#     manipulador.executar()