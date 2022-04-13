"""ecommerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from account.api.viewsets import UserCreateViewSet, UsersViewSet
from customers.api.viewsets import CustomersViewSet
from django.contrib import admin
from django.urls import include, path
from django.views.decorators.csrf import csrf_exempt
from products.api.viewsets import ProductsViewSet
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter
from sales.api.viewsets import (SalesDetailViewSet, SalesItemsViewSet,
                                SalesViewSet)
from sellers import views as sellers_view
from sellers.api.viewsets import SellersViewSet

router = DefaultRouter()
router.register(r'costumers', CustomersViewSet, basename="clientes")
router.register(r'products', ProductsViewSet, basename="produtos")
router.register(r'sales', SalesViewSet, basename="vendas")
router.register(r'detail_sales', SalesDetailViewSet, basename="detalhe_vendas")
router.register(r'sales_items', SalesItemsViewSet, basename="itens_vendas")
router.register(r'sellers', SellersViewSet, basename="vendedores")
router.register(r'accounts', UsersViewSet, basename="usuarios")
router.register(r'accounts/create/', UserCreateViewSet,
                basename="novo_usuario")

urlpatterns = [
    path('api/comission/seller/<int:id>/start_date/<str:start_date>/end_date/<str:end_date>/',
         csrf_exempt(sellers_view.SellersComission.as_view())),
    path('api/login/', obtain_auth_token, name="login"),
    path('api/', include(router.urls)),
    path('admin/', admin.site.urls),
]
