from rest_framework import serializers

from education.serializers import PaymentSerializer
from users.models import User


class UserDetailSerializer(serializers.ModelSerializer):
    payments = PaymentSerializer(source='user_payments', many=True)

    class Meta:
        model = User
        fields = ('email', 'payments')
