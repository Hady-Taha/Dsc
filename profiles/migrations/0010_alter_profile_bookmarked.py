# Generated by Django 3.2 on 2021-05-10 10:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0011_alter_comments_content'),
        ('profiles', '0009_alter_profile_bookmarked'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='bookmarked',
            field=models.ManyToManyField(to='article.Article'),
        ),
    ]