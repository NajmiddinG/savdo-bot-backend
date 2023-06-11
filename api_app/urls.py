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
router.register(r'savat', SavatListCreateApiViewSet)
router.register(r'buyurtma', BuyurtmaListCreateApiViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]
