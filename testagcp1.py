import pandas as pd
from google.cloud import bigquery

# Carregar o DataFrame a partir do arquivo pickle
df = pd.read_pickle('dfbbc.pkl')

# Especifique o caminho para o arquivo JSON de credenciais
path_to_credentials = 'projetoandreapassarellilopes-594ea4062e2e.json'

# Crie uma instância do cliente BigQuery com as credenciais fornecidas
client = bigquery.Client.from_service_account_json(path_to_credentials)

# Agora você pode usar o cliente BigQuery para realizar operações no BigQuery
# por exemplo, carregar os dados do DataFrame em uma tabela do BigQuery

# Especifique o projeto e o dataset onde você deseja armazenar os dados
project_id = 'projetoandreapassarellilopes'
dataset_id = 'projetoandreapassarellilopes'

# Especifique o nome da tabela onde você deseja armazenar os dados
table_id = 'noticias_bbc.diaria'

# Carregue o DataFrame no BigQuery
job_config = bigquery.LoadJobConfig()
job_config.write_disposition = bigquery.WriteDisposition.WRITE_TRUNCATE
job = client.load_table_from_dataframe(df, table_id, job_config=job_config)

# Aguarde a conclusão do job
job.result()

# Verifique se o job foi concluído com sucesso
table = client.get_table(table_id)
print(f"Os dados foram carregados no BigQuery: {table.full_table_id}")
