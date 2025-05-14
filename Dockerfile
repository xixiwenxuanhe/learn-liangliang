FROM python:3.10-slim

WORKDIR /app

# 安装依赖
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# 复制代码（实际运行时会用挂载覆盖）
COPY . .

EXPOSE 60000

CMD ["gunicorn", "-w", "4", "-k", "gevent", "-b", "0.0.0.0:60000", "server_flask:app"]