# 动态指定变量 --build-arg python_version=python:3.8-alpine
ARG python_version='python:3.8-alpine'
FROM ${python_version}

LABEL maintainer="wxs15852445352@163.com"
LABEL description="Django配置"

ARG PROJECT_NAME=Pugss
ENV PROJECT_NAME=${PROJECT_NAME}
WORKDIR  /app
COPY ./${PROJECT_NAME}/  /app/${PROJECT_NAME}/

WORKDIR /app/${PROJECT_NAME}/


COPY ./gunicorn_conf.py  ./
COPY ./supervisor.conf  ./
COPY ./docker-entrypoint.sh  /entrypoint.sh

# 配置 APK 源为阿里云镜像，并更新软件包列表
RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.aliyun.com/g' /etc/apk/repositories && \
    apk update && \
    apk upgrade

# 安装构建依赖和常用工具
RUN apk add --allow-untrusted build-base curl iputils ca-certificates openssl-dev musl-dev && \
    apk add --virtual build-deps gcc libc-dev libffi-dev python3-dev --no-cache mariadb-connector-c-dev
# 安装并配置时区
RUN apk add tzdata && \
    cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && \
    echo "Asia/Shanghai" > /etc/timezone && \
    apk del tzdata && \
    apk update && \
    apk upgrade && \
    rm -rf /var/cache/apk/* && \
    chmod +x /entrypoint.sh

# 升级 pip 并安装依赖
RUN pip install -i https://mirrors.aliyun.com/pypi/simple/ --upgrade pip && pip install -i https://mirrors.aliyun.com/pypi/simple/  --no-cache-dir -U pip && \
    pip install --no-cache-dir -i https://mirrors.aliyun.com/pypi/simple/ -r requirements.txt

VOLUME /app/$PROJECT_NAME/logs
VOLUME /app/$PROJECT_NAME/

EXPOSE 8000
ENTRYPOINT ["/entrypoint.sh"]