from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'evenements', views.EvenementViewSet, basename='evenement')
router.register(r'groupes', views.GroupeViewSet, basename='groupe')

urlpatterns = [
    path('', include(router.urls)),
]