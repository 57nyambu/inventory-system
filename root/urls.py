from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    #path('', include('apps.core.urls')),
    path('api/v1/auth/', include('apps.core.urls.auth')),
    path('api/v1/mgt/', include('apps.core.urls.mgt')),
    path('api/v1/analytics/', include('apps.analytics.urls')),
    path('api/v1/integrate/', include('apps.integrations.urls')),
    #path('api/v1/inventory/', include('apps.inventory.urls')),
    path('api/v1/orders/', include('apps.orders.urls')),
    path('api/v1/procurement/', include('apps.procurement.urls')),
    path('api/v1/products/', include('apps.products.urls')),
    path('api/v1/sales/', include('apps.sales.urls')),
    path('api/v1/transactions/', include('apps.transactions.urls')),
]
