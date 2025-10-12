# 数据库大作业

需要在本地安装mySQL

安装依赖：

pip install django djangorestframework

pip install django-cors-headers

## 重构后的项目运行流程
1. 在MySQL中新建项目数据库，无需建表
2. 修改配置文件 canteen_new/config/settings.py
    ```python
    # Database
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'canteen', #更改为本地数据库名称
            'USER': 'root', #更改为用户名
            'PASSWORD': 'test', #更改为本地数据库密码
            'HOST': 'localhost',
            'PORT': '3306',
            'OPTIONS': {
                'charset': 'utf8mb4',
            }
        }
    }
    ```
3. 输入指令
    `cd canteen_new; python manage.py runserver 3000`
    启动后端服务
4. 启动前端服务，仓库地址： https://github.com/AdaChangL/canteen_frontend