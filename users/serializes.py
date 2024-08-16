from rest_framework import serializers

from users.models import User, Payment


class PaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payment
        fields = '__all__'


class SelfUserSerializer(serializers.ModelSerializer):
    payments = PaymentSerializer(many=True, source='payment_set')

    class Meta:
        model = User
        fields = '__all__'


class AnotherUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'email', 'phone', 'city', 'avatar')


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
