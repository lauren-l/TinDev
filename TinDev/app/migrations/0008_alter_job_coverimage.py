# Generated by Django 4.1.3 on 2022-11-29 23:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_alter_job_coverimage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='coverImage',
            field=models.ImageField(default='../../static/images/errorImage.jpg', upload_to='app/static/images'),
        ),
    ]