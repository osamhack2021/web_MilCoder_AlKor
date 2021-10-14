from utils.api import UsernameSerializer, OnlyUsernameSerializer, serializers

from .models import Course, CourseAnnouncement
from account.serializers import RankInfoSerializer, UserSerializer


class CreateCourseSeriaizer(serializers.Serializer):
    title = serializers.CharField(max_length=128)
    description = serializers.CharField()  

    #List of username
    students = serializers.ListField(child=serializers.CharField(max_length=32), allow_empty=True)
   
    visible = serializers.BooleanField()

class EditCourseSeriaizer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=128)
    description = serializers.CharField()  

    #List of username
    students = serializers.ListField(child=serializers.CharField(max_length=32), allow_empty=True)
   
    visible = serializers.BooleanField()


class CourseAdminSerializer(serializers.ModelSerializer):
    created_by = UsernameSerializer()
    students = serializers.StringRelatedField(many=True)

    class Meta:
        model = Course        
        fields = "__all__"


class CourseSerializer(CourseAdminSerializer):
    class Meta:
        model = Course


class CourseAnnouncementSerializer(serializers.ModelSerializer):
    created_by = UsernameSerializer()

    class Meta:
        model = CourseAnnouncement
        fields = "__all__"


class CreateCourseAnnouncementSerializer(serializers.Serializer):
    course_id = serializers.IntegerField()
    title = serializers.CharField(max_length=128)
    content = serializers.CharField()
    visible = serializers.BooleanField()


class EditCourseAnnouncementSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=128, required=False)
    content = serializers.CharField(required=False, allow_blank=True)
    visible = serializers.BooleanField(required=False)
