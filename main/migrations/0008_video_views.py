# Generated by Django 5.0.2 on 2024-12-07 13:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_alter_article_intro_alter_article_intro_en_us_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='views',
            field=models.IntegerField(default=0, verbose_name="Ko'rish soni"),
        ),
    ]