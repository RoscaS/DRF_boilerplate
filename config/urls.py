from django.conf.urls.static import static
from django.contrib.auth import logout
from django.urls import include
from django.urls import path

from config import settings
from config.api import api

from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path('logout/', logout, {'next_page': '/'}, name='logout'),

    # API ROOT
    path('api/', include(api.urls)),

    # DRF API authentification
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    # JWT
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
