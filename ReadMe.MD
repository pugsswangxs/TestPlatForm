## 文件夹结构介绍
```
DjangoDeploy\DeployDocker 文件夹结构
├── docker-compose.yaml      # Docker容器编排主配置文件，定义所有服务(web, redis, mysql等)的关联关系
├── .env                     # 全局环境变量配置文件，包含数据库密码、密钥等敏感信息（建议加入.gitignore）
├── redis_docker/            
│   ├── redis.conf           # Redis服务器配置文件，可配置持久化、密码验证等
│   └── Dockerfile           # Redis镜像构建文件，可定制Redis版本和插件
├── Django_docker/
│   ├── Pugss/               # Django项目主目录
│   │   ├── settings/        # 项目配置目录（分环境配置）
│   │   │   ├── base_setting.py  # 基础配置（被其他配置继承）
│   │   │   ├── dev.py       # 开发环境专用配置
│   │   │   └── pro.py       # 生产环境专用配置（含数据库配置）
│   │   └── logs/            # 应用日志存储目录（需确保Docker有写入权限）
│   │
│   ├── gunicorn_conf.py     # Gunicorn WSGI服务器配置（worker数量、超时等）
│   ├── requirements.txt     # Python依赖清单（pip freeze > requirements.txt生成）
│   ├── supervisord.conf     # 进程管理配置（可管理Gunicorn、Celery等）
│   └── Dockerfile           # Django应用镜像构建文件（包含Python环境安装）
├── nginx_docker/
│   ├── dist/                # 前端静态文件目录（Vue/React打包产物应放入此处）
│   ├── nginx.conf           # Nginx主配置文件（全局配置）
│   ├── default.conf         # 站点配置（server块、反向代理规则等）
│   ├── Dockerfile           # Nginx镜像构建文件（可添加自定义模块）
│   ├── supervisord.conf     # Nginx进程管理配置（可选）
│   └── docker-entrypoint.sh # 启动脚本（可添加预启动命令）

```
## 配置账号密码
### mysql 密码修改（上下保持一致）
#### Django配置mysql账号密码

 - 进入到Django项目配置目录下
```shell
cd Django_docker/Pugss/Pugss/settings
```
 - 修改 pro.py 下的 DATABASES的值
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME':'数据库名称',
        'USER':'用户名',   #登录mysql 的用户名
        'PASSWORD':'密码',    # 登录mysql 的密码
        'HOST':'pugss_mysql',   # mysql 容器名称（根据需要配置）
        'PORT':'3306',          # mysql 端口
        'OPTIONS':{
            'charset':'utf8mb4',
        }
    }
}
```
#### Mysql 容器配置账号密码
 - 直接修改 .env 下的内容即可
```shell
MYSQL_ROOT_PASSWORD=root用户密码
MYSQL_DATABASE=数据库名称
MYSQL_USER=用户名
MYSQL_PASSWORD=密码
```
### redis 配置账号密码
 - 修改 redis.conf 文件
```
user 用户名 on >密码 ~* &* +@all
例如：
user redisuser on >asdbi3asudfhaf ~* &* +@all
```

## 日志路径修改
### Django 配置日志路径
- 进入到Django项目配置目录下
- 修改 base_settings.py 配置文件
```shell
 {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',  # 或者保持 TimedRotatingFileHandler
            'filename': BASE_DIR / 'logs/django.log',
            'maxBytes': 1024 * 1024 * 30,  # 每个日志文件最大 5MB
            'backupCount': 10,  # 保留最近 7 个日志文件
            'encoding': 'utf-8',
            'formatter': 'verbose',
        }
```

### gunicorn 配置日志路径
- 进入到Django项目目录下
- 修改 gunicorn_conf.py 配置文件
```
pidfile = '/tmp/gunicorn.pid'
# 日志设置（建议输出到 stdout/stderr，Docker 日志系统会捕获）
accesslog = str(BASE_DIR / 'logs/gunicorn_access.log')  # 输出到标准输出
errorlog =  str(BASE_DIR / 'logs/gunicorn_error.log')
```

### supervisor 配置日志路径

- 进入到Django项目目录下
- 修改 supervisor.conf 配置文件
```
logfile=/tmp/supervisor.log  ; 日志文件路径（容器中建议使用 tmp 或 stdout）
```
## 部署环境
1. 创建网络
```shell
docker network create \
  --driver bridge \
  --subnet 172.18.0.0/24 \
  --gateway 172.18.0.1 \
  mybridge
 ```
2. 创建镜像和容器
```shell
docker-compose -p myapp up -d
```
3. 结果查看
```
启动成功后，访问 http://ip:5204
```

## 问题排查
使用  ReadMeDeployByDockerFile.MD 文件 逐步排查即可