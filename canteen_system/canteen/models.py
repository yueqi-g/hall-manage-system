from django.db import models
from django.contrib.auth.models import User

class Merchant(models.Model):
    CATEGORY_CHOICES = [
        ('饭', '饭'),
        ('面', '面'),
        ('饺子', '饺子'),
        ('其他', '其他'),
    ]
    
    TASTE_CHOICES = [
        ('辣', '辣'),
        ('咸', '咸'),
        ('淡', '淡'),
        ('酸甜', '酸甜'),
    ]
    
    id = models.AutoField(primary_key=True, verbose_name='商家编号')
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='merchant_profile', verbose_name='关联用户')
    name = models.CharField(max_length=100, verbose_name='商家名称')
    hall = models.CharField(max_length=50, verbose_name='食堂号')
    location = models.CharField(max_length=50, verbose_name='窗口号')
    contact_info = models.CharField(max_length=100, blank=True, null=True, verbose_name='联系方式')
    description = models.TextField(blank=True, null=True, verbose_name='商家描述')
    status = models.BooleanField(default=True, verbose_name='营业状态')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        db_table = 'merchants'
        verbose_name = '商家'
        verbose_name_plural = '商家'
        unique_together = ['hall', 'location']
    
    def __str__(self):
        return f"{self.name} ({self.hall}-{self.location})"

class Dish(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='菜品编号')
    merchant = models.ForeignKey(Merchant, on_delete=models.CASCADE, related_name='dishes', verbose_name='商家')
    name = models.CharField(max_length=100, verbose_name='菜品名称')
    description = models.TextField(blank=True, null=True, verbose_name='菜品描述')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='价格')
    category = models.CharField(max_length=10, choices=Merchant.CATEGORY_CHOICES, verbose_name='品类')
    taste = models.CharField(max_length=10, choices=Merchant.TASTE_CHOICES, verbose_name='口味')
    spice_level = models.IntegerField(default=0, verbose_name='辣度等级')
    image_url = models.URLField(blank=True, null=True, verbose_name='菜品图片')
    is_available = models.BooleanField(default=True, verbose_name='是否可用')
    stock_quantity = models.IntegerField(default=0, verbose_name='库存数量')
    ai_tags = models.JSONField(default=dict, blank=True, verbose_name='AI标签')  # 预留AI字段
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        db_table = 'dishes'
        verbose_name = '菜品'
        verbose_name_plural = '菜品'
    
    def __str__(self):
        return self.name

class UserPreference(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='用户')
    preferred_categories = models.JSONField(default=list, verbose_name='偏好品类')
    preferred_tastes = models.JSONField(default=list, verbose_name='偏好口味')
    price_range_min = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='最低价格')
    price_range_max = models.DecimalField(max_digits=10, decimal_places=2, default=999.99, verbose_name='最高价格')
    dietary_restrictions = models.JSONField(default=list, verbose_name='饮食限制')
    ai_profile = models.JSONField(default=dict, blank=True, verbose_name='AI用户画像')  # 预留AI字段
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        db_table = 'user_preferences'
        verbose_name = '用户偏好'
        verbose_name_plural = '用户偏好'
    
    def __str__(self):
        return f"{self.user.username}的偏好"

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', '待确认'),
        ('confirmed', '已确认'),
        ('preparing', '制作中'),
        ('ready', '待取餐'),
        ('completed', '已完成'),
        ('cancelled', '已取消'),
    ]
    
    id = models.AutoField(primary_key=True, verbose_name='订单编号')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户')
    merchant = models.ForeignKey(Merchant, on_delete=models.CASCADE, verbose_name='商家')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='订单总金额')
    item_count = models.IntegerField(verbose_name='菜品总数')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='订单状态')
    ai_recommendation_score = models.FloatField(null=True, blank=True, verbose_name='AI推荐得分')  # 预留AI字段
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        db_table = 'orders'
        verbose_name = '订单'
        verbose_name_plural = '订单'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"订单{self.id} - {self.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name='订单')
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE, verbose_name='菜品')
    quantity = models.IntegerField(verbose_name='数量')
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='单价')
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='小计')
    
    class Meta:
        db_table = 'order_items'
        verbose_name = '订单项'
        verbose_name_plural = '订单项'
    
    def __str__(self):
        return f"{self.dish.name} x{self.quantity}"

class FootTraffic(models.Model):
    TIME_SLOT_CHOICES = [
        ('早餐', '早餐'),
        ('午餐', '午餐'),
        ('晚餐', '晚餐'),
    ]
    
    id = models.AutoField(primary_key=True, verbose_name='主键')
    merchant = models.ForeignKey(Merchant, on_delete=models.CASCADE, verbose_name='商家')
    traffic_count = models.IntegerField(verbose_name='客流量')
    record_date = models.DateField(verbose_name='记录日期')
    time_slot = models.CharField(max_length=10, choices=TIME_SLOT_CHOICES, verbose_name='时间段')
    ai_prediction = models.JSONField(default=dict, blank=True, verbose_name='AI预测数据')  # 预留AI字段
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='记录时间')
    
    class Meta:
        db_table = 'foot_traffic'
        verbose_name = '客流量'
        verbose_name_plural = '客流量'
        unique_together = ['merchant', 'record_date', 'time_slot']
    
    def __str__(self):
        return f"{self.merchant.name} - {self.record_date} {self.time_slot}"