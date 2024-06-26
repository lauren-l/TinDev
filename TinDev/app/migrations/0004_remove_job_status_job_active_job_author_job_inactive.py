# Generated by Django 4.1.3 on 2022-11-29 16:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_alter_job_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='job',
            name='status',
        ),
        migrations.AddField(
            model_name='job',
            name='active',
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='job',
            name='author',
            field=models.CharField(default='John Doe', max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='job',
            name='inactive',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
    ]
