from django.conf.urls import url

from ..views.oj import CouseAnnouncementListAPI
from ..views.oj import CourseAccessAPI
from ..views.oj import CourseAPI

urlpatterns = [
    url(r"^course/?$", CourseAPI.as_view(), name="course_api"),
    url(r"^course/announcement/?$", CourseAnnouncementListAPI.as_view(), name="contest_announcement_api"),
]
