from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import PermissionDenied
from rest_framework.filters import OrderingFilter
from rest_framework import viewsets, generics, serializers
from rest_framework.permissions import IsAuthenticated

from education.models import Course, Lesson, Payment, Subscription
from education.paginators import Paginator
from education.permissions import IsNotStaffUser, IsOwnerOrStaffUser
from education.serializers import LessonSerializer, CourseDetailSerializer, PaymentListSerializer, \
    SubscriptionSerializer, SubscriptionListSerializer


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseDetailSerializer
    queryset = Course.objects.all()
    permission_classes = [IsAuthenticated, IsOwnerOrStaffUser]
    pagination_class = Paginator

    def get_queryset(self):
        if not self.request.user.is_staff:
            return Course.objects.filter(owner=self.request.user)
        elif self.request.user.is_staff:
            return Course.objects.all()
        else:
            raise PermissionDenied

    def create(self, request, *args, **kwargs):
        if request.user.is_staff:
            raise PermissionDenied
        return super().create(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        if request.user.is_staff:
            raise PermissionDenied
        return super().destroy(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsNotStaffUser]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonListAPIView(generics.ListCreateAPIView):
    serializer_class = LessonSerializer
    pagination_class = Paginator

    def get_queryset(self):
        if not self.request.user.is_staff:
            return Lesson.objects.filter(owner=self.request.user)
        elif self.request.user.is_staff:
            return Lesson.objects.all()
        else:
            raise PermissionDenied


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsOwnerOrStaffUser]


class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsOwnerOrStaffUser]


class LessonDestroyAPIView(generics.DestroyAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsNotStaffUser]


class PaymentListAPIView(generics.ListAPIView):
    serializer_class = PaymentListSerializer
    queryset = Payment.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ('course', 'payment_method')
    ordering_fields = ('payment_date',)


class SubscriptionCreateAPIView(generics.CreateAPIView):
    serializer_class = SubscriptionSerializer
    permission_classes = [IsNotStaffUser]

    def create(self, request, *args, **kwargs):
        for subscription in Subscription.objects.filter(user=self.request.user):
            if subscription.course.id == request.data.get('course'):
                raise PermissionDenied('У вас уже есть подписка на этот курс.')
        if self.request.user.id != request.data.get('user'):
            raise PermissionDenied('Нельзя оформлять подписки на другого пользователя.')
        return super().create(request, *args, **kwargs)


class SubscriptionListAPIView(generics.ListAPIView):
    serializer_class = SubscriptionListSerializer

    def get_queryset(self):
        return Subscription.objects.filter(user=self.request.user)


class SubscriptionDestroyAPIView(generics.DestroyAPIView):
    serializer_class = SubscriptionSerializer
    permission_classes = [IsNotStaffUser]

    def get_queryset(self):
        return Subscription.objects.filter(user=self.request.user)
