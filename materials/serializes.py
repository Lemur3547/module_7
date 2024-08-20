from rest_framework import serializers

from materials.models import Course, Lesson
from materials.validators import VideoLinkValidator


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'
        validators = [VideoLinkValidator(field='video_link')]


class CourseSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, source='lesson_set')

    class Meta:
        model = Course
        fields = '__all__'

    def get_lessons_count(self, instance):
        return instance.lesson_set.all().count()


class CreateCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'
