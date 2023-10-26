from rest_framework import serializers

from education.serializers import PaymentSerializer
from users.models import User


class UserRetrieveSerializer(serializers.ModelSerializer):
    payments = PaymentSerializer(source='user_payments', many=True)

    class Meta:
        model = User
        fields = ('email', 'payments', 'phone', 'city', 'avatar')


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('phone', 'city', 'avatar')
