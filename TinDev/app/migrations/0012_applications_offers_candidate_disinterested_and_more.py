# Generated by Django 4.1.3 on 2022-11-30 19:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_remove_job_inactive'),
    ]

    operations = [
        migrations.CreateModel(
            name='Applications',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('job_id', models.CharField(max_length=50)),
                ('candidate_id', models.CharField(max_length=50)),
                ('recruiter_id', models.CharField(max_length=50)),
                ('compatibility_score', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Offers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('job_id', models.CharField(max_length=50)),
                ('candidate_id', models.CharField(max_length=50)),
                ('recruiter_id', models.CharField(max_length=50)),
                ('offerDeadline', models.DateTimeField()),
                ('salary', models.FloatField()),
                ('response', models.BooleanField()),
                ('accepted', models.BooleanField()),
            ],
        ),
        migrations.AddField(
            model_name='candidate',
            name='disinterested',
            field=models.CharField(default='', max_length=500),
        ),
        migrations.AddField(
            model_name='candidate',
            name='interested',
            field=models.CharField(default='', max_length=500),
        ),
        migrations.AlterField(
            model_name='candidate',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='recruiter',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
