from django.urls import path, include
from rest_framework import routers
from .views import (
    BotUserListCreateApiViewSet,
    ProductListCreateApiViewSet,
    SavatListCreateApiViewSet,
    BuyurtmaListCreateApiViewSet
)

router = routers.DefaultRouter()
router.register(r'bot_users', BotUserListCreateApiViewSet)
router.register(r'products', ProductListCreateApiViewSet)
router.register(r'savat', SavatListCreateApiViewSet, basename='savat')
router.register(r'buyurtma', BuyurtmaListCreateApiViewSet, basename='buyurtma')

urlpatterns = [
    path('', include(router.urls)),
    path('savat-list/<int:user_id>/', SavatListCreateApiViewSet.as_view({'get': 'list'}), name='savat-list'),
    path('buyurtma-list/<int:user_id>/', BuyurtmaListCreateApiViewSet.as_view({'get': 'list'}), name='buyurtma-list')
]
