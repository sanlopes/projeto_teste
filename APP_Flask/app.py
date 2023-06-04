from flask import Flask, request, jsonify
from google.cloud import bigquery

# Configure o cliente BigQuery fornecendo as credenciais do serviço
path_to_credentials = 'projetoandreapassarellilopes-594ea4062e2e.json'
client = bigquery.Client.from_service_account_json(path_to_credentials)

# Crie uma instância do Flask
app = Flask(__name__)

@app.route('/search', methods=['GET'])
def search_articles():
    keyword = request.args.get('keyword')
    if not keyword:
        return jsonify({'error': 'Keyword parameter is missing'}), 400

    query = f"""
        SELECT *
        FROM `projetoandreapassarellilopes.noticias_bbc.diaria`
        WHERE titulo_noticia LIKE '%{keyword}%'
        OR url_noticia LIKE '%{keyword}%'
        OR data_noticia LIKE '%{keyword}%'
        OR texto_noticia LIKE '%{keyword}%'
        LIMIT 10
    """
    job = client.query(query)
    results = job.result()

    articles = []
    for row in results:
        article = {
            'title': row['titulo_noticia'],
            'url': row['url_noticia'],
            'date': row['data_noticia'],
            'text': row['texto_noticia']
        }
        articles.append(article)

    return jsonify({'articles': articles})

if __name__ == '__main__':
    app.run(debug=True)
