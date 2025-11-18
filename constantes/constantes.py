# Comentar constantes abaixo -  adicionar ao git.ignore
#========================================================
APP_URL = 'URL DA API DO BUBBLE' 
DATA_TYPE = 'TIPO DE DADO' 
API_TOKEN = 'TOKEN DA API'
DATA_TYPE_DB = 'BANCO DE DADOS'

URL = 'LINK NEWGATE'
URL_METAS = 'URL DE METAS'


#========================================================
# Constantes gerais do projeto
#========================================================
SEMANAS = [
    1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20,
    21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37,38,39,40,41
]
ANO = 2025

CAMINHO_ARQUIVO = "storage"
LANDING = 'landing/2025'
TRUSTED = 'trusted/2025'
BUSINESS = 'business/2025'


HEADERS_LOGIN = {
    "accept": "/",
    "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
    "connection": "keep-alive",
    "content-length": "131",
    "content-type": "application/x-www-form-urlencoded",
    "host": "new.kaizen.newgate.pro",
    "origin": "URL_SISTEMA_NEWGATE",
    "referer": "URL_SISTEMA_NEWGATE/login",
    "schema": "SCHEMA",
    "sec-ch-ua": '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "macOS",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"
}
HEADERS_METAS = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,/;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "en-US,en;q=0.9,pt;q=0.8",
    "cache-control": "max-age=0",
    "connection": "keep-alive",
    # "content-type": "application/x-www-form-urlencoded",
    "host": "URL_SISTEMA_NEWGATE",
    "referer": "URL_SISTEMA_NEWGATE/metas",
    # "cookie": "",
    "sec-ch-ua": "'Google Chrome';v='131', 'Chromium';v='131', 'Not_A Brand';v='24'",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "'macOS'",
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "same-origin",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
}

COLUNAS_DESEJADAS_ALUNO = [
    "Created Date",
    "Nome_usuário",
    "_id",
]

COLUNAS_DESEJADAS_DB = [
    "Created Date",
    "data_aula",
    "Created By",
    "nome_mentor",
    "Emocional_alunos",
    "nomeDeAluno",
    "conteúdoMinistrado",
    "materias_alunos",
    "StatusAcompanhamento",
    "dificuldadesApresentadas",
    "Duracao_da_Aula",
    "sanardificuldades",
    "aula_foi_reposicao",
    "_id",
    
]
PAYLOAD_LOGIN = {
    "grant_type": "password",
    "scope": "",
    "client_id": " string",
    "client_secret": "string"
}

PAYLOAD_METAS = {
    "semana": "",
    "ano": ""
}

ALUNO_CRIANCA = ['Nome da criança 1', 'Nome da criança 2', 'Nome da criança 3']
