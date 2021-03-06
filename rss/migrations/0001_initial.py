# Generated by Django 3.2.13 on 2022-04-26 14:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Feed',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=250, null=True)),
                ('link', models.CharField(max_length=450)),
                ('last_update', models.DateTimeField(blank=True, editable=False, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='userfeed', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='FeedItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=400, null=True)),
                ('link', models.URLField(blank=True, null=True)),
                ('context', models.TextField(blank=True, null=True)),
                ('read', models.BooleanField(default=False)),
                ('date_fetched', models.DateTimeField(auto_now_add=True)),
                ('date_publish', models.CharField(blank=True, max_length=100, null=True)),
                ('feed', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='feed', to='rss.feed')),
            ],
        ),
    ]
