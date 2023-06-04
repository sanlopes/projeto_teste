import pandas as pd
import json

# Carregar o arquivo JSON em um DataFrame
with open('noticias.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

df = pd.DataFrame(data)

# Remover linhas duplicadas
df = df.drop_duplicates()

# Realizar a substituição em uma coluna específica
df['text'] = df['text'].str.replace('This video can not be played', 'Contém Vídeo na Notícia - ')

# Converter a coluna "date" para o formato desejado, incluindo hora e minutos, ignorando as linhas com valor nulo
df['date'] = df['date'].apply(lambda x: pd.to_datetime(x).strftime('%d/%m/%Y %H:%M') if x is not None else None)

# Drop da coluna "author"
df = df.drop('author', axis=1)

# Remover as linhas em que o campo "text" é None
df = df.dropna(subset=['text'])

# Renomear os nomes dos campos
df = df.rename(columns={'title': 'titulo_noticia', 'url': 'url_noticia', 'date': 'data_noticia', 'text': 'texto_noticia'})

# Substituir "None" por "Null" na coluna "data_noticia"
df['data_noticia'] = df['data_noticia'].replace('None', 'Null')

# Salvar o DataFrame em um arquivo pickle
df.to_pickle('dfbbc.pkl')

# Exibir o DataFrame atualizado
print(df)
