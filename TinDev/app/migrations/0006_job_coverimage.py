# Generated by Django 4.1.3 on 2022-11-29 23:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_job_numcandidates'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='coverImage',
            field=models.ImageField(default='../app/static/images/errorImage.jpg', upload_to='uploads/'),
            preserve_default=False,
        ),
    ]
