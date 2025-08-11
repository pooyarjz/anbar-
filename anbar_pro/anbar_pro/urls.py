
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from rest_framework import routers
from inventory.views import ItemViewSet, TransactionViewSet, StockView, ImportStatusView, DashboardView, purchase_new

router = routers.DefaultRouter()
router.register(r'items', ItemViewSet, basename='item')
router.register(r'transactions', TransactionViewSet, basename='transaction')

urlpatterns = [
    path('', RedirectView.as_view(pattern_name='dashboard', permanent=False)),
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/stock/', StockView.as_view(), name='stock'),
    path('api/import-status/', ImportStatusView.as_view(), name='import-status'),
    path('purchase/new/', purchase_new, name='purchase-new'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
]
