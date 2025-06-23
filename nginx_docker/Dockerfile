
FROM alpine:latest

LABEL maintainer="wxs15852445352@163.com"
LABEL description="Django配置"

ARG SERVER_ADDR="111.229.50.58"
ENV SERVER_ADDR=${SERVER_ADDR}

COPY ./docker-entrypoint.sh  /entrypoint.sh

# 配置 APK 源为阿里云镜像，并更新软件包列表
RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.aliyun.com/g' /etc/apk/repositories && \
    apk update && \
    apk upgrade

# 安装构建依赖和常用工具
RUN apk add --allow-untrusted build-base curl iputils ca-certificates openssl-dev musl-dev && \
    apk add --update supervisor nginx
# 安装并配置时区
RUN apk add tzdata && \
    cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && \
    echo "Asia/Shanghai" > /etc/timezone && \
    apk del tzdata && \
    apk update && \
    apk upgrade && \
    rm -rf /var/cache/apk/* && \
    mkdir -p /var/www/html && \
    chown -R nginx:nginx /var/www/html && \
    mkdir -p /var/log/supervisor && \
    chmod +x /entrypoint.sh

COPY supervisord.conf /etc/supervisord.conf
COPY nginx.conf /etc/nginx/nginx.conf
COPY defalut.conf /etc/nginx/conf.d/default.conf

VOLUME /var/www/html/
VOLUME /var/log/nginx/
VOLUME /var/log/supervisor/


EXPOSE 8000 80 443
ENTRYPOINT ["/entrypoint.sh"]