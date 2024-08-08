from django.urls import path
from rest_framework.routers import DefaultRouter

from materials.apps import MaterialsConfig
from materials.views import CourseViewSet, LessonListAPIView, LessonCreateAPIView, LessonRetrieveAPIView, \
    LessonUpdateAPIView, LessonDestroyAPIView
from users.views import PaymentViewSet

app_name = MaterialsConfig.name

router = DefaultRouter()
router.register(r'course', CourseViewSet, basename='course')
router.register(r'payment', PaymentViewSet, basename='payment')

urlpatterns = [
    path('lesson/', LessonListAPIView.as_view(), name='lesson_view'),
    path('lesson/create/', LessonCreateAPIView.as_view(), name='lesson_create'),
    path('lesson/<int:pk>/', LessonRetrieveAPIView.as_view(), name='lesson_view'),
    path('lesson/update/<int:pk>/', LessonUpdateAPIView.as_view(), name='lesson_update'),
    path('lesson/delete/<int:pk>/', LessonDestroyAPIView.as_view(), name='lesson_delete'),
] + router.urls
