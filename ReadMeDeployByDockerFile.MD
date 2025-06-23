## 创建 docker网络
```
docker network create \
  --driver bridge \
  --subnet 172.18.0.0/24 \
  --gateway 172.18.0.1 \
  mybridge
```

## 启动redis

```shell
cd DeployDocker/redis_docker

docker build -t pugss_redis_images .

docker run -tid --name pugss_redis \
  -p 5201:6379 \
  --restart=always \
  --network mybridge \
  --ip 172.18.0.10 \
  -v ./redis.conf:/usr/local/etc/redis/redis.conf \
  pugss_redis_images 
```

## 启动mysql
```
docker run -d --name pugss_mysql \
  --restart=always \
  -p 5202:3306 \
  --network mybridge \
  --ip 172.18.0.11 \
  -v /data/mysql:/var/lib/mysql \
  -e MYSQL_ROOT_PASSWORD=lMqf1zte32 \
  -e MYSQL_DATABASE=pugssdb \
  -e MYSQL_USER=pugss \
  -e MYSQL_PASSWORD=bf8C0CC1me \
  mysql:latest \
  --character-set-server=utf8mb4 \
  --collation-server=utf8mb4_unicode_ci
```

## 启动Django
 ```shell
cd DeployDocker/Django_docker
docker build -t pugss_django_images .
docker run -tid --name pugss_Django \
  --restart=always \
  -p 5203:8000 \
  --network mybridge \
  -v /data/Django/:/app/Pugss/logs \
  --ip 172.18.0.12 \
  -e ENV=production \
  pugss_django_images 
```

## 启动nginx
```shell
cd DeployDocker/nginx_docker
docker build -t pugss_nginx_images .
docker run -tid --name pugss_nginx \
  --restart=always \
  -p 5204:80 \
  -p 5205:443 \
  -p 5206:8000 \
  --network mybridge \
  --ip 172.18.0.13 \
  -v ./dist:/var/www/html \
  -v /data/nginx/log/:/var/log/nginx/ \
  pugss_nginx_images
```
