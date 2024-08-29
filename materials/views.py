import datetime

from django.conf import settings
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from materials.models import Course, Lesson, Subscription
from materials.paginators import MaterialsPaginator
from materials.serializes import CourseSerializer, LessonSerializer
from materials.tasks import update_course_email
from users.permissions import IsModerator, IsOwner


# Create your views here.

class CourseViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    pagination_class = MaterialsPaginator
    serializer_class = CourseSerializer

    def get_permissions(self):
        if self.action in ['retrieve', 'update']:
            self.permission_classes = [IsModerator | IsOwner]
        elif self.action == 'create':
            self.permission_classes = [~IsModerator]
        elif self.action == 'destroy':
            self.permission_classes = [IsOwner]
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        if self.request.user.groups.filter(name='moderator').exists():
            queryset = Course.objects.all()
        else:
            queryset = Course.objects.filter(user=self.request.user)
        return queryset

    def perform_update(self, serializer):
        course = serializer.save()
        if course.last_update:
            if timezone.now() - course.last_update > datetime.timedelta(hours=4):
                update_course_email.delay(course)
        else:
            update_course_email.delay(course)
        course.last_update = timezone.now()
        course.save()


class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, ~IsModerator]

    def perform_create(self, serializer):
        lesson = serializer.save()
        lesson.user = self.request.user
        if lesson.course.last_update:
            if timezone.now() - lesson.course.last_update > datetime.timedelta(hours=4):
                update_course_email.delay(lesson.course)
        else:
            update_course_email.delay(lesson.course)
        lesson.course.last_update = timezone.now()
        lesson.course.save()
        lesson.last_update = timezone.now()
        lesson.save()


class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModerator | IsOwner]
    pagination_class = MaterialsPaginator

    def get_queryset(self):
        if self.request.user.groups.filter(name='moderator').exists():
            queryset = Lesson.objects.all()
        else:
            queryset = Lesson.objects.filter(user=self.request.user)
        return queryset


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsModerator | IsOwner]


class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsModerator | IsOwner]

    def perform_update(self, serializer):
        lesson = serializer.save()
        if lesson.course.last_update:
            if timezone.now() - lesson.course.last_update > datetime.timedelta(hours=4):
                update_course_email.delay(lesson.course)
        else:
            update_course_email.delay(lesson.course)
        lesson.course.last_update = timezone.now()
        lesson.course.save()
        lesson.last_update = timezone.now()
        lesson.save()


class LessonDestroyAPIView(generics.DestroyAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]


class SubscriptionAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, *args, **kwargs):
        user = self.request.user
        course_id = self.request.parser_context['kwargs']['pk']
        course_item = get_object_or_404(Course, pk=course_id)
        subs_item = Subscription.objects.filter(user=user, course=course_item)

        if subs_item.exists():
            subs_item.delete()
            message = 'подписка удалена'
        else:
            Subscription.objects.create(user=user, course=course_item)
            message = 'подписка добавлена'
        return Response({"message": message})
