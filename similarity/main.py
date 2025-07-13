import os
import glob
import tkinter as tk
from tkinter import ttk, scrolledtext
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class DocumentComparator:
    def __init__(self, master, doc_dir):
        self.master = master
        self.doc_dir = doc_dir
        self.docs = {}
        self.filenames = []
        self.cos_sim = None

        self.load_documents()
        self.vectorize_documents()
        self.setup_ui()

    def load_documents(self):
        file_paths = glob.glob(os.path.join(self.doc_dir, "*.txt"))
        for file_path in file_paths:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                filename = os.path.basename(file_path)
                self.docs[filename] = content
                self.filenames.append(filename)
            except Exception as e:
                print(f"Error loading {file_path}: {str(e)}")

    def vectorize_documents(self):
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform(self.docs.values())
        self.cos_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

    def setup_ui(self):
        self.master.title("文档相似度比较器")
        self.master.geometry("1000x800")

        # 创建选择框框架
        selection_frame = ttk.Frame(self.master)
        selection_frame.pack(pady=10)

        self.combo1 = ttk.Combobox(selection_frame, values=self.filenames, width=40)
        self.combo2 = ttk.Combobox(selection_frame, values=self.filenames, width=40)
        self.combo1.pack(side=tk.LEFT, padx=5)
        self.combo2.pack(side=tk.LEFT, padx=5)

        # 创建文本显示框架
        text_frame = ttk.Frame(self.master)
        text_frame.pack(fill=tk.BOTH, expand=True)

        self.text1 = scrolledtext.ScrolledText(text_frame, wrap=tk.WORD, width=50)
        self.text2 = scrolledtext.ScrolledText(text_frame, wrap=tk.WORD, width=50)
        self.text1.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        self.text2.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)

        # 创建结果显示区域
        result_frame = ttk.Frame(self.master)
        result_frame.pack(pady=10)

        self.result_label = ttk.Label(result_frame, text="余弦距离：", font=('Arial', 12))
        self.result_label.pack()

        # 绑定事件
        self.combo1.bind("<<ComboboxSelected>>", self.update_display)
        self.combo2.bind("<<ComboboxSelected>>", self.update_display)

    def update_display(self, event):
        file1 = self.combo1.get()
        file2 = self.combo2.get()

        if not file1 or not file2:
            return

        # 更新文档内容
        self.text1.delete(1.0, tk.END)
        self.text1.insert(tk.END, self.docs[file1])
        self.text2.delete(1.0, tk.END)
        self.text2.insert(tk.END, self.docs[file2])

        # 计算并显示相似度
        idx1 = self.filenames.index(file1)
        idx2 = self.filenames.index(file2)
        similarity = self.cos_sim[idx1][idx2]
        distance = max(0.0, 1 - similarity)
        self.result_label.config(text=f"余弦距离：{distance:.4f}\n相似度：{similarity:.4f}")


if __name__ == "__main__":
    doc_dir = r"D:\search_engine\ch_doc"

    root = tk.Tk()
    app = DocumentComparator(root, doc_dir)
    root.mainloop()