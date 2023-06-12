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
        # Filter the queryset based on the bot user
        return Savat.objects.filter(user=self.request.user)

# buyurtma
class BuyurtmaListCreateApiViewSet(viewsets.ModelViewSet):
    serializer_class = BuyurtmaSerializer

    def get_queryset(self):
        # Filter the queryset based on the bot user
        return Buyurtma.objects.filter(user=self.request.user)
