from constantes.constantes import CAMINHO_ARQUIVO, TRUSTED, BUSINESS, ALUNO_CRIANCA
import pandas as pd
import ast
import json
import numpy as np

class BusinessApplyRuleRT:
    '''Classe para aplicar regras de negócio nos arquivos da trusted'''

    def executar(self):
        # Lógica para aplicar regras de negócio em tempo real
        df_user, df_bubble, df_metas = self.ler_csv_trusted()

        df_merged_all = self.aplicar_regras(df_user, df_bubble, df_metas)

        self.construir_json(df_merged_all)

        self.salvar_resultados(df_merged_all)

    def ler_csv_trusted(self):
        '''Função para ler os arquivos CSV da trusted'''
        # Lógica para ler os arquivos CSV de user
        caminho_pasta = f"{CAMINHO_ARQUIVO}/{TRUSTED}/user"
        nome_arquivo = f"{caminho_pasta}/alunos_ativos.csv"
        df_user = pd.read_csv(nome_arquivo)

        # Lógica para ler os arquivos CSV de bubble
        caminho_pasta_bubble = f"{CAMINHO_ARQUIVO}/{TRUSTED}/bubble"
        nome_arquivo_bubble = f"{caminho_pasta_bubble}/trusted_db_bubble_2025.csv"
        df_bubble = pd.read_csv(nome_arquivo_bubble)

        # Lógica para ler os arquivos CSV de metas
        caminho_pasta_metas = f"{CAMINHO_ARQUIVO}/{TRUSTED}/newgate"
        nome_arquivo_metas = f"{caminho_pasta_metas}/trusted_metas_newgate_2025.csv"
        df_metas = pd.read_csv(nome_arquivo_metas)

        return df_user, df_bubble, df_metas

    def aplicar_regras(self, df_user: pd.DataFrame, df_bubble: pd.DataFrame, df_metas: pd.DataFrame):
        '''Função responsável por aplicar as regras de negócio nos DataFrames lidos
            df_user: DataFrame contendo os dados dos usuários
            df_bubble: DataFrame contendo os dados extraídos do Bubble
            df_metas: DataFrame contendo os dados de metas do NewGate
            retorna: 
                DataFrame mesclado com as regras aplicadas
        '''

        # 1. mesclar tabela user com bubble e metas para adicionar id único a cada um dos dataframes
        df_merge_bubble = pd.merge(
            df_bubble,
            df_user,
            how='left',
            left_on='nome_aluno_bubble',
            right_on='nome_aluno'
        )

        # 2. mesclar tabela user com newgate e metas para adicionar id único a cada um dos dataframes
        df_merge_metas = pd.merge(
            df_metas,
            df_user,
            how='left',
            left_on='nome_aluno_newgate',
            right_on='nome_aluno'
        )

        # 3. Tratamento para df_merge_bubble: deixar apenas registros onde nome_aluno não é nulo
        df_merge_bubble = df_merge_bubble[df_merge_bubble['nome_aluno'].notna()]

        # 4. Tratamento para df_merge_metas: deixar apenas registros onde nome_aluno não é nulo
        df_merge_metas = df_merge_metas[df_merge_metas['nome_aluno'].notna()]

        # 5. Criar id_unico em df_merge_bubble id_aluno +  semana_ano
        df_merge_bubble['id_unico_bubble'] = df_merge_bubble['id_aluno'].astype(str) + '_' + df_merge_bubble['semana_ano'].astype(str)

        # 6. Criar id_unico em df_merge_metas id_aluno +  semana_ano
        df_merge_metas['id_unico_metas'] = df_merge_metas['id_aluno'].astype(str) + '_' + df_merge_metas['semana_ano'].astype(str)

        # Retirar duplicadas de id_unico_metas
        df_merge_metas = df_merge_metas.drop_duplicates(subset=['id_unico_metas'])

        # 7. Fazer merge entre df_merge_bubble e df_merge_metas com base em id_unico_bubble e id_unico_metas
        df_merge_all = pd.merge(
            df_merge_bubble,
            df_merge_metas,
            left_on='id_unico_bubble',
            right_on='id_unico_metas',
            how='left'
        )

        # Filtrar apenas colunas necessárias
        colunas_desnecessarias = ["semana_ano_x",
                                  "nome_aluno_x",
                                  "data_criacao_x",
                                  "id_aluno_x",
                                  "semana_ano_y",
                                  "data_criacao_y",
                                  "nome_aluno_y",
                                  "id_aluno_y"
                                ]

        df_merge_all_filtrado = df_merge_all.drop(columns=colunas_desnecessarias)

        # Convert data_aula to datetime and format as dd/mm/yyyy
        df_merge_all_filtrado['data_aula'] = df_merge_all_filtrado['data_aula'].str[:10]  # Pegar apenas os primeiros 10 dígitos
        df_merge_all_filtrado['data_aula'] = pd.to_datetime(df_merge_all_filtrado['data_aula']).dt.strftime('%d/%m/%Y')

        # Create month name column
        df_merge_all_filtrado['mes'] = pd.to_datetime(df_merge_all_filtrado['data_aula'], format='%d/%m/%Y').dt.strftime('%B')
        meses_pt = {
            'January': 'Janeiro', 'February': 'Fevereiro', 'March': 'Março',
            'April': 'Abril', 'May': 'Maio', 'June': 'Junho',
            'July': 'Julho', 'August': 'Agosto', 'September': 'Setembro',
            'October': 'Outubro', 'November': 'Novembro', 'December': 'Dezembro'
        }
        df_merge_all_filtrado['mes'] = df_merge_all_filtrado['mes'].map(meses_pt)

        # Create year column 
        df_merge_all_filtrado['ano'] = pd.to_datetime(df_merge_all_filtrado['data_aula'], format='%d/%m/%Y').dt.year

        # Criar coluna metas_propostas
        # Create metas_realizadas column using %_cumpridas and total_estipulado
        df_merge_all_filtrado['%_cumprida'] = pd.to_numeric(df_merge_all_filtrado['%_cumprida'])
        df_merge_all_filtrado['total_estipulado'] = pd.to_numeric(df_merge_all_filtrado['total_estipulado'])
        df_merge_all_filtrado['metas_realizadas'] = ((df_merge_all_filtrado['%_cumprida'] * df_merge_all_filtrado['total_estipulado']).round().astype(float))/100

        # Caso em emocional_aluno tenha Ausente a linha deve ser excluida
        df_merge_all_filtrado = df_merge_all_filtrado[~df_merge_all_filtrado['emocional_aluno'].str.contains('Ausente', na=False)]

        #Criar lista com elementos de emocoes
        emocoes_dict = {
            'Cansado(a)': -1,
            'Ansioso(a)': -2, 
            'Ativo(a)': 2,
            'Sonolento(a)': -1,
            'Resistente(a)': -2,
            'Falante(a)': 2,
            'Autônomo(a)': 3,
            'Concentrado': 3,
            'Confuso(a)': -1,
            'Estimulado(a)': 2,
            'Desestimulado(a)': -2,
            'Distraído(a)': -2,
            'Passivo(a)': -1,
            'Calado(a)': -1
        }
        # Com base no dicionario acima,criar uma nova coluna qtd_emocoes_positivas e qtd_emocoes_negativas com a soma das emoções, oq ue for positivo para qtd_emocoes_positivas e o que for negativo para qtd_emocoes_negativas
        def calcular_emocoes(emocoes_str):
            if pd.isna(emocoes_str):
                return 0, 0
            emocoes = ast.literal_eval(emocoes_str)
            positivas = sum(emocoes_dict[emo] for emo in emocoes if emo in emocoes_dict and emocoes_dict[emo] > 0)
            negativas = sum(emocoes_dict[emo] for emo in emocoes if emo in emocoes_dict and emocoes_dict[emo] < 0)
            return positivas, abs(negativas)
        df_merge_all_filtrado[['qtd_emocoes_positivas', 'qtd_emocoes_negativas']] = df_merge_all_filtrado['emocional_aluno'].apply(
            lambda x: pd.Series(calcular_emocoes(x))
        )
        # Adicionar coluna com a soma total das emoções
        df_merge_all_filtrado['resultado_subtracao_emocoes'] = df_merge_all_filtrado['qtd_emocoes_positivas'] - df_merge_all_filtrado['qtd_emocoes_negativas']

        # Adicionar coluna total de emoções
        df_merge_all_filtrado['total_emocoes_modulo'] = df_merge_all_filtrado['qtd_emocoes_positivas'] + df_merge_all_filtrado['qtd_emocoes_negativas']

        # Adicionar coluna com a listagem dos valores do dicionário emocoes_dict para cada registro
        def listar_valores_emocoes(emocoes_str):
            if pd.isna(emocoes_str):
                return []
            try:
                emocoes = ast.literal_eval(emocoes_str)
                if not isinstance(emocoes, (list, tuple)):
                    return []
            except Exception:
                return []
            return [emocoes_dict[e] for e in emocoes if e in emocoes_dict]

        df_merge_all_filtrado['listagem_valores_emocoes'] = df_merge_all_filtrado['emocional_aluno'].apply(listar_valores_emocoes)

        #======================= TESTES =================================
        # filtrar todos os registros onde id_unico_metas é nulo
        # df_merge_all_nulo = df_merge_all[df_merge_all['id_unico_metas'].isna()]

        # df_merge_all_nulo.to_csv('business_nulo.csv')

        # df_merge_metas.to_csv('metas.csv')
        #======================= TESTES =================================
        return df_merge_all_filtrado

    def salvar_resultados(self, df: pd.DataFrame):
        '''Função para salvar os resultados em arquivos CSV na pasta business'''
        caminho_pasta_business = f"{CAMINHO_ARQUIVO}/{BUSINESS}/relatorio_rt.csv"
        nome_arquivo_business = f"{caminho_pasta_business}"
        df.to_csv(nome_arquivo_business, index=False)

    def construir_json(self, df: pd.DataFrame):
        '''Função para transformar o DataFrame em JSON'''
        
        # Lista fixa de meses por extenso
        meses = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
                 "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]

        data = {}

        def safe(value):
            # pd.isna may return a scalar boolean or an array/Series of booleans;
            # handle both cases to avoid ambiguous truth-value errors.
            try:
                is_na = pd.isna(value)
            except Exception:
                is_na = False

            # If is_na is an array-like (numpy array or pandas Series), treat as missing only if all elements are missing or it's empty.
            if isinstance(is_na, (np.ndarray, pd.Series)):
                if getattr(is_na, "size", 0) == 0 or is_na.all():
                    return ""
                # If it's a numpy array, convert to a native list for JSON serialization
                if isinstance(value, np.ndarray):
                    return value.tolist()
                return value

            # Scalar case: return empty string for NA, otherwise convert numpy scalars to Python scalars
            if is_na:
                return ""
            if isinstance(value, np.generic):
                return value.item()
            return value
            

        # Agrupar por aluno
        for aluno, df_aluno in df.groupby("nome_aluno_bubble"):
            # Inicializar estrutura do aluno com todos os meses vazios
            data[aluno] = {mes: {} for mes in meses}
            
            # Iterar pelas linhas desse aluno
            for _, row in df_aluno.iterrows():
                mes = safe(row["mes"])  # Ex: "Janeiro"
                id_db = str(safe(row["id_diario_bordo"]))
                
                # Converter string de lista em lista real
                try:
                    emocional_aluno = ast.literal_eval(row["emocional_aluno"]) if pd.notna(row["emocional_aluno"]) else []
                except:
                    emocional_aluno = []
                
                try:
                    materias_alunos = ast.literal_eval(row["materias_alunos"]) if pd.notna(row["materias_alunos"]) else []
                except:
                    materias_alunos = []

                # Criar dicionário com os dados da aula
                data[aluno][mes][id_db] = {
                    "data_aula": safe(row["data_aula"]),
                    "conteudo_ministrado": safe(row["conteudo_ministrado"]),
                    "materias_alunos": materias_alunos,
                    "feedback_aula": safe(row["feedback_aula"]),
                    "dificuldades_encontradas": safe(row["dificuldades_encontradas"]),
                    "duracao_aula": safe(row["duracao_aula"]),
                    "resolucao_dificuldades": safe(row["resolucao_dificuldades"]),
                    "id_unico_bubble": safe(row["id_unico_bubble"]),
                    "nome_aluno_newgate": safe(row["nome_aluno_newgate"]),
                    "nome_mentor": safe(row["nome_mentor"]),
                    "emocional_aluno": emocional_aluno,
                    "qtd_emocoes_positivas": safe(row["qtd_emocoes_positivas"]),
                    "qtd_emocoes_negativas": safe(row["qtd_emocoes_negativas"]),
                    "resultado_subtracao_emocoes": safe(row["resultado_subtracao_emocoes"]),
                    "total_emocoes_modulo": safe(row["total_emocoes_modulo"]),
                    "listagem_valores_emocoes": safe(row["listagem_valores_emocoes"]),
                    "%_cumprida": safe(row["%_cumprida"]),
                    "total_estipulado": safe(row["total_estipulado"]),
                    "metas_realizadas": safe(row["metas_realizadas"]),
                    "id_unico_metas": safe(row["id_unico_metas"]),
                }

        # salvar json em arquivo (apenas UMA vez, com todos os alunos)
        caminho_pasta_business = f"{CAMINHO_ARQUIVO}/{BUSINESS}/business_json.json"
        with open(caminho_pasta_business, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

        return data

# if __name__ == "__main__":
#     main = BusinessApplyRuleRT()
#     main.executar()
        