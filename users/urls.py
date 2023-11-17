from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.views import UserRetrieveAPIView, UserUpdateAPIView, UserCreateAPIView

urlpatterns = [
    path('register/', UserCreateAPIView.as_view(), name='user-create'),
    path('<int:pk>/', UserRetrieveAPIView.as_view(), name='user-detail'),
    path('<int:pk>/update/', UserUpdateAPIView.as_view(), name='user-update'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
