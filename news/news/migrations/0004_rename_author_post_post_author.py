# Generated by Django 5.0.6 on 2024-05-24 13:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0003_alter_comment_comment_rating_alter_post_rating_post'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='author_post',
            new_name='author',
        ),
    ]