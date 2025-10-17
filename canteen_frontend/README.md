# 美食食堂前端项目

这是一个基于Vue 3的美食食堂前端项目，提供智能菜品推荐功能。

## 项目结构

```
frontend/
├── public/
│   └── index.html              # HTML模板
├── src/
│   ├── App.vue                 # 根组件
│   ├── main.js                 # 入口文件
│   ├── assets/                 # 静态资源
│   │   ├── css/               # 样式文件
│   │   │   ├── style.css      # 全局样式
│   │   │   ├── auth.css       # 认证页面样式
│   │   │   ├── user.css       # 用户页面样式
│   │   │   └── merchant.css   # 商家页面样式
│   │   └── images/            # 图片资源
│   ├── components/            # 通用组件
│   ├── views/                 # 页面组件
│   ├── router/                # 路由配置
│   ├── store/                 # 状态管理
│   └── services/              # API服务
└── package.json               # 项目配置
```

## 功能特性

- 智能菜品推荐系统
- 用户/商家双角色登录
- 实时网络状态检测
- 响应式设计
- 多语言支持


## 初次运行流程
1. 安装Node.js 官方网站：https://nodejs.org/
    验证安装成功 `node -v` 、`npm -v`
    （PS: 如果遇到npm运行权限问题，参考 https://www.cnblogs.com/520BigBear/p/15579723.html）
2. 进入本项目目录 cd canteen_frontend
    ```cmd
    npm install
    ```
3. 运行项目
    ```cmd
    npm run serve
    ```
    访问服务启动的网页