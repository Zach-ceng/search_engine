from elasticsearch import Elasticsearch
import os

es = Elasticsearch(
    hosts=["http://localhost:9200"],
    # 如果启用安全认证需添加：
    # basic_auth=("elastic", "your_password")  
)

def index_documents(doc_dir, index_name, language):
    for filename in os.listdir(doc_dir):
        if filename.endswith(".txt"):
            with open(os.path.join(doc_dir, filename), 'r', encoding='utf-8') as f:
                content = f.read()

            doc = {
                "title": filename,
                "content": content,
                "language": language
            }

            es.index(index=index_name, body=doc)

# 索引中文文档（E:\materials\SWORD_token）
index_documents(r"D:\\search_engine\\ch_afterprogress", "docs_chinese", "chinese")

# 索引英文文档（E:\materials\WAR&PEACE_test\4_stemmed_final）
index_documents(r"E:\\大学学习\\大三\\搜索引擎\\项目2\\eng_afterprocess", "docs_english", "english")