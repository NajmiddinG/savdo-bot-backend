from rest_framework import viewsets, pagination
from .models import BotUser, Product, Savat, Buyurtma
from .serializers import BotUserSerializer, ProductSerializer, SavatSerializer, BuyurtmaSerializer

# Bot user
class BotUserListCreateApiViewSet(viewsets.ModelViewSet):
    queryset = BotUser.objects.all()
    serializer_class = BotUserSerializer

# product
class ProductPagination(pagination.PageNumberPagination):
    page_size = 1
    page_size_query_param = 'page_size'
    max_page_size = 100


class ProductListCreateApiViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = ProductPagination

# savat
class SavatListCreateApiViewSet(viewsets.ModelViewSet):
    queryset = Savat.objects.all()
    serializer_class = SavatSerializer

# buyurtma
class BuyurtmaListCreateApiViewSet(viewsets.ModelViewSet):
    queryset = Buyurtma.objects.all()
    serializer_class = BuyurtmaSerializer
