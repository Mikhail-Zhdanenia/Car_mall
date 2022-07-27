from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

#from user.views import UserProfileViewSet
from buyer.views import BuyerViewSet, BuyerHistoryViewSet, BuyerOfferViewSet
from car.views import CarViewSet
from dealership.views import (DealershipViewSet, DealershipGarageViewSet,
                              DealershipBuyHistoryViewSet, DealershipSaleHistoryViewSet)
from supplier.views import SupplierViewSet, SupplierGarageViewSet


from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions


#swagger
schema_view = get_schema_view(
    openapi.Info(
        title="Car Showrooms API",
        default_version='v1',
        description="Docs",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


# Application APIs
addresses = (
    #(r'user', UserProfileViewSet, 'user'),

    (r'buyer', BuyerViewSet, 'buyer'),
    (r'buyer_history', BuyerHistoryViewSet, 'buyer_history'),
    (r'buyer_offer', BuyerOfferViewSet, 'buyer_offer'),

    (r'car', CarViewSet, 'car'),

    (r'dealership', DealershipViewSet, 'dealership'),
    (r'dealership_garage', DealershipGarageViewSet, 'dealership_garage'),
    (r'dealership_buy', DealershipBuyHistoryViewSet, 'dealership_buy'),
    (r'dealership_sale', DealershipSaleHistoryViewSet, 'dealership_sale'),

    (r'supplier', SupplierViewSet, 'supplier'),
    (r'supplier_garage', SupplierGarageViewSet, 'supplier_garage'),
)

# Route API registrations
router = routers.DefaultRouter()  # List of routers at http://.../api
for addr in addresses:
    router.register(addr[0], addr[1], basename=addr[2])

urlpatterns = [

    path('admin/', admin.site.urls),
    path('', include('core.urls'), name='homepage-url'),

    path('api/auth/', include('djoser.urls')),
    path('api/auth/', include('djoser.urls.jwt')),
    path('api/auth/', include('djoser.urls.authtoken')),
    path('api/', include(router.urls)),
    #path('auth/', include('user.urls')),

    path('swagger(?P<format>\.json|\.yaml)', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]


#debug tool
if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns