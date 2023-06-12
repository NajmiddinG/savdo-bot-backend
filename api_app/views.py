from rest_framework import viewsets, pagination, status
from .models import BotUser, Product, Savat, Buyurtma
from .serializers import BotUserSerializer, ProductSerializer, SavatSerializer, BuyurtmaSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view

# Bot user
class BotUserListCreateApiViewSet(viewsets.ModelViewSet):
    queryset = BotUser.objects.all()
    serializer_class = BotUserSerializer

# product
class ProductPagination(pagination.PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 100


class ProductListCreateApiViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all().order_by('-id')
    serializer_class = ProductSerializer
    pagination_class = ProductPagination

@api_view(['GET'])
def get_savat_data(request, user_id):
    queryset = Savat.objects.filter(user_id=user_id)
    serializer = SavatSerializer(queryset, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_buyurtma_data(request, user_id):
    queryset = Buyurtma.objects.filter(user_id=user_id)
    serializer = BuyurtmaSerializer(queryset, many=True)
    return Response(serializer.data)

class SavatListCreateApiViewSet(viewsets.ModelViewSet):
    queryset = Savat.objects.all().order_by('-date')
    serializer_class = SavatSerializer


# buyurtma
class BuyurtmaListCreateApiViewSet(viewsets.ModelViewSet):
    queryset = Buyurtma.objects.all().order_by('-date')
    serializer_class = BuyurtmaSerializer