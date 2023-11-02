from django.urls import path
from rest_framework import routers

from education.views import CourseViewSet, LessonCreateAPIView, LessonListAPIView, LessonRetrieveAPIView, \
    LessonUpdateAPIView, LessonDestroyAPIView, PaymentListAPIView, SubscriptionDestroyAPIView, SubscriptionListAPIView, \
    SubscriptionCreateAPIView

urlpatterns = [
    # lessons
    path('lessons/create/', LessonCreateAPIView.as_view(), name='lesson-create'),
    path('lessons/', LessonListAPIView.as_view(), name='lesson-list'),
    path('lessons/<int:pk>/', LessonRetrieveAPIView.as_view(), name='lesson-retrieve'),
    path('lessons/<int:pk>/update/', LessonUpdateAPIView.as_view(), name='lesson-update'),
    path('lessons/<int:pk>/delete/', LessonDestroyAPIView.as_view(), name='lesson-delete'),

    # payments
    path('payments/', PaymentListAPIView.as_view(), name='payment-list'),

    # subscriptions
    path('subscriptions/create/', SubscriptionCreateAPIView.as_view(), name='subscription-create'),
    path('subscriptions/', SubscriptionListAPIView.as_view(), name='subscription-list'),
    path('subscriptions/<int:pk>/delete/', SubscriptionDestroyAPIView.as_view(), name='subscription-delete'),
]

router = routers.DefaultRouter()
router.register(r'course', CourseViewSet)

urlpatterns += router.urls
