# Generated by Django 3.0.8 on 2020-07-30 01:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forward_app', '0003_thread'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='next_comment_id',
            field=models.IntegerField(default=0),
        ),
    ]
