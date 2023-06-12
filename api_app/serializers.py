from rest_framework import serializers, viewsets
from .models import BotUser, Product, Savat, Buyurtma


class BotUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = BotUser
        fields = ['id', 'name', 'lan', 'username', 'date']


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name_uz', 'name_ru', 'kelish_narx', 'sotish_narx', 'brend', 'image', 'shtrix', 'xarakteristika_uz', 'xarakteristika_ru']


class SavatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Savat
        fields = ['id', 'user', 'product', 'count', 'location', 'tel', 'date']


class BuyurtmaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Buyurtma
        fields = ['id', 'user', 'product', 'count', 'yakunlandi', 'location', 'tel', 'date']
