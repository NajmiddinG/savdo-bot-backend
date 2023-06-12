from rest_framework import viewsets, pagination
from .models import BotUser, Product, Savat, Buyurtma
from .serializers import BotUserSerializer, ProductSerializer, SavatSerializer, BuyurtmaSerializer

# Bot user
class BotUserListCreateApiViewSet(viewsets.ModelViewSet):
    queryset = BotUser.objects.all()
    serializer_class = BotUserSerializer

# product
class ProductPagination(pagination.PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class ProductListCreateApiViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all().order_by('-id')
    serializer_class = ProductSerializer
    pagination_class = ProductPagination

# savat
class SavatListCreateApiViewSet(viewsets.ModelViewSet):
    serializer_class = SavatSerializer
    
    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        return Savat.objects.filter(user_id=user_id)

# buyurtma
class BuyurtmaListCreateApiViewSet(viewsets.ModelViewSet):
    serializer_class = BuyurtmaSerializer

    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        return Buyurtma.objects.filter(user_id=user_id)