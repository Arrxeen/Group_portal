# Generated by Django 5.1.3 on 2024-12-21 17:27

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0004_alter_dislike_unique_together_remove_dislike_comment_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('media', models.FileField(blank=True, null=True, upload_to='post_media')),
                ('type', models.CharField(choices=[('news', 'News'), ('update', 'Update'), ('event', 'Event'), ('question', 'Question')], max_length=20)),
                ('priority', models.CharField(choices=[('close', 'Close'), ('open', 'Open')], default='open', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='category', to='forum.category')),
                ('creater', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='posts', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('media', models.FileField(blank=True, null=True, upload_to='comments_media')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='comments', to=settings.AUTH_USER_MODEL)),
                ('psot_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='forum.post')),
            ],
        ),
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='liked_comments', to=settings.AUTH_USER_MODEL)),
                ('comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='likes', to='forum.post')),
            ],
            options={
                'unique_together': {('user', 'comment')},
            },
        ),
        migrations.CreateModel(
            name='Dislike',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='disliked_comments', to=settings.AUTH_USER_MODEL)),
                ('comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dislikes', to='forum.post')),
            ],
            options={
                'unique_together': {('user', 'comment')},
            },
        ),
    ]
