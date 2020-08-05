# Generated by Django 3.1 on 2020-08-05 01:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('forward_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Policy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('category', models.IntegerField()),
                ('name', models.CharField(blank=True, default='', max_length=100)),
                ('statement', models.CharField(blank=True, default='', max_length=500)),
                ('description', models.TextField(blank=True, default='')),
            ],
            options={
                'ordering': ['created'],
            },
        ),
        migrations.CreateModel(
            name='Thread',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lead_comment_id', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Popularity',
            fields=[
                ('policy', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='forward_app.policy')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('likes', models.IntegerField(default=0)),
            ],
            options={
                'ordering': ['created'],
            },
        ),
        migrations.CreateModel(
            name='Persona',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('num_followers', models.IntegerField(default=0)),
                ('stage', models.IntegerField(default=1)),
                ('line1', models.CharField(blank=True, default='', max_length=200)),
                ('city', models.CharField(blank=True, default='', max_length=200)),
                ('state', models.CharField(blank=True, default='', max_length=20)),
                ('zipcode', models.IntegerField()),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('users', models.ManyToManyField(related_name='followers', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['created'],
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('next_comment_id', models.IntegerField(default=0)),
                ('content', models.CharField(blank=True, default='', max_length=1000)),
                ('likes', models.IntegerField(default=0)),
                ('thread', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='forward_app.thread')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['time'],
            },
        ),
        migrations.AddField(
            model_name='thread',
            name='popularity',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='forward_app.popularity'),
        ),
    ]
