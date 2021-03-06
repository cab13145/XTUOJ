# Generated by Django 3.0.3 on 2020-05-28 15:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contest', '0001_initial'),
        ('problem', '0001_initial'),
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='QuickTest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=64)),
                ('testin', models.TextField()),
                ('testout', models.TextField()),
                ('result', models.IntegerField(default=-1)),
                ('time', models.IntegerField()),
                ('memory', models.IntegerField()),
                ('language', models.CharField(max_length=64)),
                ('message', models.TextField()),
                ('problem', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='problem.Problem')),
            ],
            options={
                'db_table': 'quick_test',
            },
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('status_id', models.AutoField(primary_key=True, serialize=False)),
                ('result', models.IntegerField(default=-1)),
                ('time', models.IntegerField()),
                ('memory', models.IntegerField()),
                ('length', models.IntegerField()),
                ('language', models.CharField(max_length=64)),
                ('subtime', models.DateTimeField(auto_now_add=True)),
                ('judger', models.CharField(max_length=64)),
                ('message', models.TextField()),
                ('ip', models.CharField(default='unknown', max_length=150, null=True)),
                ('score', models.IntegerField(default=0)),
                ('contest', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='contest.Contest')),
                ('problem', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='problem.Problem')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.User')),
            ],
            options={
                'db_table': 'judge_status',
                'ordering': ('-subtime',),
            },
        ),
        migrations.CreateModel(
            name='SubmitCode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.TextField(max_length=65536)),
                ('status', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='submission.Status', unique=True)),
            ],
            options={
                'db_table': 'submit_code',
            },
        ),
        migrations.CreateModel(
            name='QuickTestCode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.TextField(max_length=15000)),
                ('test', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='submission.QuickTest', unique=True)),
            ],
            options={
                'db_table': 'quick_test_code',
            },
        ),
        migrations.CreateModel(
            name='CaseStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=64)),
                ('result', models.IntegerField()),
                ('time', models.IntegerField()),
                ('memory', models.IntegerField()),
                ('testcase', models.CharField(default='unknown', max_length=200)),
                ('inputdata', models.CharField(default='', max_length=200)),
                ('outputdata', models.CharField(default='', max_length=200)),
                ('useroutput', models.CharField(default='', max_length=200)),
                ('problem', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='problem.Problem')),
                ('status_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='submission.Status')),
            ],
            options={
                'db_table': 'case_status',
            },
        ),
    ]
