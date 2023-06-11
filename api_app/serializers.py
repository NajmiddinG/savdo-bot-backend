from rest_framework import serializers, viewsets
from .models import BotUser, Product, Savat, Buyurtma


class BotUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = BotUser
        fields = ['id', 'user_id', 'name', 'lan', 'username', 'date']


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'kelish_narx', 'sotish_narx', 'brend', 'image', 'shtrix', 'xarakteristika']


class SavatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Savat
        fields = ['id', 'user', 'product', 'count', 'location', 'tel', 'date']


class BuyurtmaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Buyurtma
        fields = ['id', 'user', 'product', 'count', 'location', 'tel', 'date']
