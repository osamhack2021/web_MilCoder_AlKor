from django.db import models
from django.utils.timezone import now

from account.models import User, AdminType
from problem.models import Problem
#from board.models import Board

from utils.models import RichTextField

def get_super_admin():
    return User.objects.get(admin_type = AdminType.SUPER_ADMIN)[0]

class Course(models.Model) :
    title = models.TextField()
    description = RichTextField()

    students = models.ManyToManyField(User, related_name="course_student")

    create_time = models.DateTimeField(auto_now_add=True)
    last_update_time = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET(get_super_admin))
    
    visible = models.BooleanField(default=True)

    class Meta:
        db_table = "course"
        ordering = ("-create_time",)


class Assignment(models.Model) :
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    title = models.TextField()
    description = RichTextField()

    problem_list = models.ManyToManyField(Problem)

    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    create_time = models.DateTimeField(auto_now_add=True)
    last_update_time = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET(get_super_admin))

    class Meta:
        db_table = "assignment"
        ordering = ("-create_time",)


class CourseAnnouncement(models.Model):
    contest = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.TextField()
    content = RichTextField()

    created_by = models.ForeignKey(User, on_delete=models.SET(get_super_admin))
    
    visible = models.BooleanField(default=True)
    create_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "course_announcement"
        ordering = ("-create_time",)
