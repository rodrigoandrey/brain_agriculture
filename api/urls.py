from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api import views

router_v1 = DefaultRouter()
router_v1.register(r'produtores', views.ProdutorViewSet)
router_v1.register(r'fazendas', views.FazendaViewSet)
router_v1.register(r'safras', views.SafraViewSet)
router_v1.register(r'culturas', views.CulturaViewSet)

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
]
