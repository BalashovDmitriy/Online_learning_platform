from django.urls import path

from users.views import UserRetrieveAPIView

urlpatterns = [
    path('<int:pk>/', UserRetrieveAPIView.as_view(), name='user-detail'),
]
