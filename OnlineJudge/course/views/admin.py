import copy
import os
import zipfile
from ipaddress import ip_network

import dateutil.parser
from django.http import FileResponse

from account.decorators import check_course_permission, ensure_created_by
from account.models import User
from submission.models import Submission, JudgeStatus
from utils.api import APIView, validate_serializer
from utils.cache import cache
from utils.constants import CacheKey
from utils.shortcuts import rand_str
from utils.tasks import delete_files
from ..models import Course, CourseAnnouncement
from ..serializers import (CourseAnnouncementSerializer, CourseAdminSerializer,
                           CreateCourseSeriaizer, EditCourseSeriaizer,
                           CreateCourseAnnouncementSerializer, EditCourseAnnouncementSerializer)


class CourseAPI(APIView):
    @validate_serializer(CreateCourseSeriaizer)
    def post(self, request):
        data = request.data
      
        students = data.pop("students")
        data["created_by"] = request.user       
        course = Course.objects.create(**data)
        
        for item in students :
            try :
                student = User.objects.get(username=item)
                course.students.add(student)
            except User.DoesNotExist :
                pass
        
        return self.success(CourseAdminSerializer(course).data)

    @validate_serializer(EditCourseSeriaizer)
    def put(self, request):
        data = request.data
        try:
            course = Course.objects.get(id=data.pop("id"))
            ensure_created_by(course, request.user)
        except Course.DoesNotExist:
            return self.error("Course does not exist")

        students = data.pop("students")

        for k, v in data.items():
            setattr(course, k, v)
        course.save()

        course.students.remove(*course.students.all())
        for item in students :
            try :
                student = User.objects.get(username=item)
                course.students.add(student)
            except User.DoesNotExist :
                pass

        return self.success(CourseAdminSerializer(course).data)

    def get(self, request):
        course_id = request.GET.get("id")
        if course_id:
            try:
                course = Course.objects.get(id=course_id)
                ensure_created_by(course, request.user)
                return self.success(CourseAdminSerializer(course).data)
            except Course.DoesNotExist:
                return self.error("Course does not exist")

        courses = Course.objects.all().order_by("-create_time")
        if request.user.is_admin():
            courses = courses.filter(created_by=request.user)

        keyword = request.GET.get("keyword")
        if keyword:
            courses = courses.filter(title__contains=keyword)
        return self.success(self.paginate_data(request, courses, CourseAdminSerializer))


class CourseAnnouncementAPI(APIView):
    @validate_serializer(CreateCourseAnnouncementSerializer)
    def post(self, request):
        """
        Create one course_announcement.
        """
        data = request.data
        try:
            course = Course.objects.get(id=data.pop("course_id"))
            ensure_created_by(course, request.user)
            data["course"] = course
            data["created_by"] = request.user
        except Course.DoesNotExist:
            return self.error("Course does not exist")
        announcement = CourseAnnouncement.objects.create(**data)
        return self.success(CourseAnnouncementSerializer(announcement).data)

    @validate_serializer(EditCourseAnnouncementSerializer)
    def put(self, request):
        """
        update course_announcement
        """
        data = request.data
        try:
            course_announcement = CourseAnnouncement.objects.get(id=data.pop("id"))
            ensure_created_by(course_announcement, request.user)
        except CourseAnnouncement.DoesNotExist:
            return self.error("Course announcement does not exist")
        for k, v in data.items():
            setattr(course_announcement, k, v)
        course_announcement.save()
        return self.success()

    def delete(self, request):
        """
        Delete one course_announcement.
        """
        course_announcement_id = request.GET.get("id")
        if course_announcement_id:
            if request.user.is_admin():
                CourseAnnouncement.objects.filter(id=course_announcement_id,
                                                   course__created_by=request.user).delete()
            else:
                CourseAnnouncement.objects.filter(id=course_announcement_id).delete()
        return self.success()

    def get(self, request):
        """
        Get one course_announcement or course_announcement list.
        """
        course_announcement_id = request.GET.get("id")
        if course_announcement_id:
            try:
                course_announcement = CourseAnnouncement.objects.get(id=course_announcement_id)
                ensure_created_by(course_announcement, request.user)
                return self.success(CourseAnnouncementSerializer(course_announcement).data)
            except CourseAnnouncement.DoesNotExist:
                return self.error("Course announcement does not exist")

        course_id = request.GET.get("course_id")
        if not course_id:
            return self.error("Parameter error")
        course_announcements = CourseAnnouncement.objects.filter(course_id=course_id)
        if request.user.is_admin():
            course_announcements = course_announcements.filter(created_by=request.user)
        keyword = request.GET.get("keyword")
        if keyword:
            course_announcements = course_announcements.filter(title__contains=keyword)
        return self.success(CourseAnnouncementSerializer(course_announcements, many=True).data)


#TODO
class AssignmentAPI(APIView) :
    def post() :
        pass

    def put() :
        pass

    def delete() :
        pass

    def get() :
        pass