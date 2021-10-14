# Generated by Django 2.1.7 on 2021-10-14 14:44

import course.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import utils.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('problem', '0014_problem_share_submission'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Assignment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField()),
                ('description', utils.models.RichTextField()),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('last_update_time', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'assignment',
                'ordering': ('-create_time',),
            },
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField()),
                ('description', utils.models.RichTextField()),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('last_update_time', models.DateTimeField(auto_now=True)),
                ('visible', models.BooleanField(default=True)),
                ('created_by', models.ForeignKey(on_delete=models.SET(course.models.get_super_admin), to=settings.AUTH_USER_MODEL)),
                ('students', models.ManyToManyField(related_name='course_student', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'course',
                'ordering': ('-create_time',),
            },
        ),
        migrations.CreateModel(
            name='CourseAnnouncement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField()),
                ('content', utils.models.RichTextField()),
                ('visible', models.BooleanField(default=True)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('contest', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='course.Course')),
                ('created_by', models.ForeignKey(on_delete=models.SET(course.models.get_super_admin), to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'course_announcement',
                'ordering': ('-create_time',),
            },
        ),
        migrations.AddField(
            model_name='assignment',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='course.Course'),
        ),
        migrations.AddField(
            model_name='assignment',
            name='created_by',
            field=models.ForeignKey(on_delete=models.SET(course.models.get_super_admin), to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='assignment',
            name='problem_list',
            field=models.ManyToManyField(to='problem.Problem'),
        ),
    ]
