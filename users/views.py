import datetime

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics
from rest_framework.exceptions import ValidationError
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated

from users.models import User, Payment
from users.permissions import IsSelfUser
from users.serializes import SelfUserSerializer, AnotherUserSerializer, PaymentSerializer, UserRegisterSerializer
from users.services import create_product, create_price, create_session


# Create your views here.
class UserCreateAPIView(generics.CreateAPIView):
    serializer_class = UserRegisterSerializer

    def perform_create(self, serializer):
        user = serializer.save()
        user.set_password(user.password)
        user.save()


class UserListAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AnotherUserSerializer
    queryset = User.objects.all()


class UserRetrieveAPIView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.request.user.pk == self.kwargs['pk']:
            return SelfUserSerializer
        return AnotherUserSerializer


class UserUpdateAPIView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated, IsSelfUser]
    serializer_class = SelfUserSerializer
    queryset = User.objects.all()


class UserDestroyAPIView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated, IsSelfUser]
    queryset = User.objects.all()


class PaymentViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ('course', 'lesson', 'payment_method')
    ordering_fields = ('date',)

    def perform_create(self, serializer):
        payment = serializer.save(user=self.request.user)
        if payment.course is None and payment.lesson is None:
            raise ValidationError('Выберите курс или урок для оплаты')
        elif payment.course is not None and payment.lesson is not None:
            raise ValidationError('Выберите только один курс или урок для оплаты')
        else:
            if payment.course:
                product = create_product(payment.course)
            else:
                product = create_product(payment.lesson)
        price = create_price(price=payment.summ, product=product)
        session_id, session_url, payment_method = create_session(price)
        payment.session_id = session_id
        payment.payment_link = session_url
        payment.date = datetime.datetime.now()
        payment.payment_method = payment_method
        payment.save()

