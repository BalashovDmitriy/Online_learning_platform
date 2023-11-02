from rest_framework import serializers

from education.models import Course, Lesson, Payment
from education.validators import LinkValidator


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ('title',)


class LessonListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ('title',)


class CourseDetailSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField()
    lessons = LessonListSerializer(many=True, read_only=True)

    def get_lessons_count(self, obj):
        return Lesson.objects.all().filter(course=obj).count()

    class Meta:
        model = Course
        fields = '__all__'
        read_only_fields = ('owner', 'lessons_count')


class LessonSerializer(serializers.ModelSerializer):
    course = serializers.SlugRelatedField(slug_field='title', queryset=Course.objects.all())
    validators = [LinkValidator(link='link')]

    class Meta:
        model = Lesson
        fields = ('title', 'description', 'image', 'link', 'course')


class PaymentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ('user', 'course', 'payment_date', 'payment_sum', 'payment_method')


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ('course', 'payment_date', 'payment_sum', 'payment_method')
