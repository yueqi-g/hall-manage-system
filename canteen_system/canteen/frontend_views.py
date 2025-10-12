from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django.views import View
import json

@method_decorator(csrf_exempt, name='dispatch')
class AuthAPIView(View):
    """处理认证相关的API请求"""
    
    def post(self, request):
        try:
            data = json.loads(request.body)
            action = data.get('action', 'login')
            
            if action == 'login':
                return self.handle_login(data)
            elif action == 'register':
                return self.handle_register(data)
            else:
                return JsonResponse({'success': False, 'message': '无效的操作'})
                
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'message': '无效的JSON数据'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    
    def handle_login(self, data):
        username = data.get('username')
        password = data.get('password')
        user_type = data.get('userType', 'user')
        
        # 简单的模拟登录逻辑
        if username and password:
            # 模拟成功登录
            return JsonResponse({
                'success': True,
                'user': {
                    'id': 1,
                    'username': username,
                    'type': user_type
                },
                'token': 'mock-token-' + str(hash(username + password))
            })
        else:
            return JsonResponse({'success': False, 'message': '用户名或密码不能为空'})
    
    def handle_register(self, data):
        username = data.get('username')
        password = data.get('password')
        email = data.get('email')
        user_type = data.get('userType', 'user')
        
        # 简单的模拟注册逻辑
        if username and password and email:
            # 模拟成功注册
            return JsonResponse({
                'success': True,
                'user': {
                    'id': 1,
                    'username': username,
                    'type': user_type,
                    'email': email
                }
            })
        else:
            return JsonResponse({'success': False, 'message': '请填写完整信息'})

@method_decorator(csrf_exempt, name='dispatch')
class MerchantAPIView(View):
    """处理商家相关的API请求"""
    
    def get(self, request, endpoint=''):
        if endpoint == 'dishes':
            return self.get_merchant_dishes()
        elif endpoint == 'traffic':
            return self.get_traffic_data()
        else:
            return JsonResponse({'success': False, 'message': '无效的端点'})
    
    def post(self, request, endpoint=''):
        try:
            data = json.loads(request.body)
            
            if endpoint == 'dishes':
                return self.add_dish(data)
            elif endpoint == 'traffic':
                return self.update_traffic(data)
            else:
                return JsonResponse({'success': False, 'message': '无效的端点'})
                
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'message': '无效的JSON数据'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    
    def delete(self, request, dish_id):
        # 模拟删除菜品
        return JsonResponse({'success': True, 'message': '菜品删除成功'})
    
    def get_merchant_dishes(self):
        # 模拟返回商家菜品列表
        mock_dishes = [
            {
                'id': 1,
                'name': '麻辣香锅',
                'price': 28.0,
                'category': 'rice',
                'taste': 'spicy',
                'description': '香辣可口，配料丰富'
            },
            {
                'id': 2,
                'name': '番茄牛肉面',
                'price': 22.0,
                'category': 'noodle',
                'taste': 'light',
                'description': '新鲜番茄熬制汤底，牛肉鲜嫩多汁'
            }
        ]
        return JsonResponse(mock_dishes, safe=False)
    
    def add_dish(self, data):
        # 模拟添加菜品
        return JsonResponse({'success': True, 'message': '菜品添加成功'})
    
    def get_traffic_data(self):
        # 模拟返回客流量数据
        return JsonResponse({
            'currentCount': 15,
            'avgWaitTime': 8.5,
            'lastUpdate': '14:30'
        })
    
    def update_traffic(self, data):
        # 模拟更新客流量
        return JsonResponse({'success': True, 'message': '客流量更新成功'})

def index_view(request):
    """首页视图"""
    return render(request, 'index.html')

def user_dashboard_view(request):
    """用户仪表板视图"""
    return render(request, 'user_dashboard.html')

def merchant_dashboard_view(request):
    """商家仪表板视图"""
    return render(request, 'merchant_dashboard.html')
