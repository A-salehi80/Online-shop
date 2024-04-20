from django.urls import path, include
from .views import ItemApi
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

app_name = 'api_v1'
urlpatterns = [
    path('item/<id>/', ItemApi.as_view(), name='item_api'),
    # Token
    path('token', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),

]