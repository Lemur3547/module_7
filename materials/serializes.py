from rest_framework import serializers

from materials.models import Course, Lesson, Subscription
from materials.validators import VideoLinkValidator


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'
        validators = [VideoLinkValidator(field='video_link')]


class CourseSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, source='lesson_set')
    is_subscribed = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Course
        fields = '__all__'

    def get_lessons_count(self, instance):
        return instance.lesson_set.all().count()

    def get_is_subscribed(self, instance):
        return Subscription.objects.filter(user=self.context['request'].user, course=instance.pk).exists()


class CreateCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'
