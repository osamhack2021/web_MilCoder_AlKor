# Generated by Django 2.1.7 on 2021-10-17 04:10

from django.conf import settings
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion
import problem.models
import utils.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contest', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Problem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('_id', models.TextField(db_index=True)),
                ('is_public', models.BooleanField(default=False)),
                ('title', models.TextField()),
                ('description', utils.models.RichTextField()),
                ('input_description', utils.models.RichTextField()),
                ('output_description', utils.models.RichTextField()),
                ('samples', django.contrib.postgres.fields.jsonb.JSONField()),
                ('test_case_id', models.TextField()),
                ('test_case_score', django.contrib.postgres.fields.jsonb.JSONField()),
                ('hint', utils.models.RichTextField(null=True)),
                ('languages', django.contrib.postgres.fields.jsonb.JSONField()),
                ('template', django.contrib.postgres.fields.jsonb.JSONField()),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('last_update_time', models.DateTimeField(null=True)),
                ('time_limit', models.IntegerField()),
                ('memory_limit', models.IntegerField()),
                ('io_mode', django.contrib.postgres.fields.jsonb.JSONField(default=problem.models._default_io_mode)),
                ('spj', models.BooleanField(default=False)),
                ('spj_language', models.TextField(null=True)),
                ('spj_code', models.TextField(null=True)),
                ('spj_version', models.TextField(null=True)),
                ('spj_compile_ok', models.BooleanField(default=False)),
                ('rule_type', models.TextField()),
                ('visible', models.BooleanField(default=True)),
                ('difficulty', models.TextField()),
                ('source', models.TextField(null=True)),
                ('total_score', models.IntegerField(default=0)),
                ('submission_number', models.BigIntegerField(default=0)),
                ('accepted_number', models.BigIntegerField(default=0)),
                ('statistic_info', django.contrib.postgres.fields.jsonb.JSONField(default=dict)),
                ('share_submission', models.BooleanField(default=False)),
                ('contest', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='contest.Contest')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'problem',
                'ordering': ('create_time',),
            },
        ),
        migrations.CreateModel(
            name='ProblemTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
            ],
            options={
                'db_table': 'problem_tag',
            },
        ),
        migrations.AddField(
            model_name='problem',
            name='tags',
            field=models.ManyToManyField(to='problem.ProblemTag'),
        ),
        migrations.AlterUniqueTogether(
            name='problem',
            unique_together={('_id', 'contest')},
        ),
    ]
