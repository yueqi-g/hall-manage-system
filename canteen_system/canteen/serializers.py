from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Merchant, Dish, UserPreference, Order, OrderItem, FootTraffic

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

class MerchantSerializer(serializers.ModelSerializer):
    dish_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Merchant
        fields = '__all__'
    
    def get_dish_count(self, obj):
        return obj.dishes.count()

class DishSerializer(serializers.ModelSerializer):
    merchant_name = serializers.CharField(source='merchant.name', read_only=True)
    hall = serializers.CharField(source='merchant.hall', read_only=True)
    location = serializers.CharField(source='merchant.location', read_only=True)
    
    class Meta:
        model = Dish
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']
    
    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("价格必须大于0")
        if value > 999.99:
            raise serializers.ValidationError("价格不能超过999.99元")
        return value
    
    def validate_spice_level(self, value):
        if value < 0 or value > 5:
            raise serializers.ValidationError("辣度等级必须在0-5之间")
        return value

class UserPreferenceSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = UserPreference
        fields = '__all__'

class OrderItemSerializer(serializers.ModelSerializer):
    dish_name = serializers.CharField(source='dish.name', read_only=True)
    dish_image = serializers.CharField(source='dish.image_url', read_only=True)
    
    class Meta:
        model = OrderItem
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)
    merchant_name = serializers.CharField(source='merchant.name', read_only=True)
    
    class Meta:
        model = Order
        fields = '__all__'

class FootTrafficSerializer(serializers.ModelSerializer):
    merchant_name = serializers.CharField(source='merchant.name', read_only=True)
    
    class Meta:
        model = FootTraffic
        fields = '__all__'

# AI相关序列化器
class AIRecommendationRequestSerializer(serializers.Serializer):
    user_id = serializers.IntegerField(required=False)
    categories = serializers.ListField(child=serializers.CharField(), required=False)
    tastes = serializers.ListField(child=serializers.CharField(), required=False)
    max_price = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    max_results = serializers.IntegerField(default=5)

class AIPredictionRequestSerializer(serializers.Serializer):
    merchant_id = serializers.IntegerField(required=False)
    date = serializers.DateField(required=False)
    time_slot = serializers.CharField(required=False)

