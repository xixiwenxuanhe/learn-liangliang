from flask import Flask, send_from_directory, abort
import os
import urllib.parse

app = Flask(__name__)
BASE_DIR = "."

@app.route('/')
def index():
    index_path = os.path.join(BASE_DIR, 'index.html')
    if os.path.isfile(index_path):
        return send_from_directory(BASE_DIR, 'index.html')
    else:
        abort(404)

@app.route('/<path:filename>')
def serve_static(filename):
    filename = urllib.parse.unquote(filename)  # 先URL解码

    if filename.startswith('.') or '..' in filename:
        abort(403)

    file_path = os.path.join(BASE_DIR, filename)

    if os.path.isfile(file_path):
        return send_from_directory(BASE_DIR, filename)
    elif os.path.isdir(file_path):  # 🔥 如果是目录
        index_path = os.path.join(file_path, 'index.html')
        if os.path.isfile(index_path):
            return send_from_directory(file_path, 'index.html')
        else:
            abort(404)
    else:
        abort(404)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=60005)


# 生产环境启动
# gunicorn -w 4 -k gevent -b 127.0.0.1:60000 server_flask:app


