@echo off
echo =========================================
echo 启动美食食堂前端开发环境
echo =========================================

echo 启动Vue前端开发服务器...
start "Vue Frontend" cmd /k "npm run serve"

echo =========================================
echo 服务启动完成！
echo 前端地址: http://localhost:8080
echo 后端API: http://localhost:8000/api
echo =========================================
echo.
echo 提示:
echo 1. 请先启动后端Django服务器
echo    cd canteen_new
echo    python manage.py runserver
echo.
echo 2. 然后访问前端页面
echo    http://localhost:8080
echo =========================================

pause
