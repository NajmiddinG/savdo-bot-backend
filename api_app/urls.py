from django.urls import path, include
from rest_framework import routers
from .views import (
    BotUserListCreateApiViewSet,
    ProductListCreateApiViewSet,
    SavatListCreateApiViewSet,
    BuyurtmaListCreateApiViewSet,
    get_buyurtma_data, get_savat_data
)

router = routers.DefaultRouter()
router.register(r'bot_users', BotUserListCreateApiViewSet)
router.register(r'products', ProductListCreateApiViewSet)
router.register(r'savat', SavatListCreateApiViewSet, basename='savat')
router.register(r'buyurtma', BuyurtmaListCreateApiViewSet, basename='buyurtma')

urlpatterns = [
    path('', include(router.urls)),
    path('savat-list/<int:user_id>/', get_savat_data, name='savat-list'),
    path('buyurtma-list/<int:user_id>/', get_buyurtma_data, name='buyurtma-list')
]
