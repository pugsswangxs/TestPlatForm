# 使用官方 Redis 基础镜像
FROM redis:alpine

# 维护者信息（可选）
LABEL maintainer="wxs15852445352@163.com"
LABEL description="Redis 镜像"

# 拷贝自定义的 redis.conf 配置文件到容器中
COPY ./redis.conf /usr/local/etc/redis/redis.conf

RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.aliyun.com/g' /etc/apk/repositories && \
    apk update && \
    apk upgrade && \
    apk add tzdata && \
    cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && \
    echo "Asia/Shanghai" > /etc/timezone && \
    apk del tzdata && \
    rm -rf /var/cache/apk/*


# 挂载持久化卷（用于保存 Redis 数据）
VOLUME /data/redis

VOLUME /usr/local/etc/redis/
# 暴露 Redis 默认端口
EXPOSE 6379

# 启动 Redis 服务时使用自定义配置文件
CMD ["redis-server", "/usr/local/etc/redis/redis.conf"]
