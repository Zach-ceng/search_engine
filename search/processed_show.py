from flask import Flask, request, render_template
from elasticsearch import Elasticsearch
import os

app = Flask(__name__)

# 解决Windows路径问题
template_dir = os.path.abspath('templates')
app.template_folder = template_dir

es = Elasticsearch(
    hosts=["http://localhost:9200"],
    verify_certs=False
)

@app.route('/')
def home():
    return render_template('search.html')

@app.route('/search')
def search():
    try:
        query = request.args.get('q', '')
        lang = request.args.get('lang', 'chinese')

        body = {
            "query": {"match": {"content": query}},
            "highlight": {"fields": {"content": {}}}
        }

        resp = es.search(index=f"docs_{lang}", body=body)
        return render_template('results.html',
                           results=resp['hits']['hits'],
                           query=query)
    except Exception as e:
        return str(e), 5000

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)