# Generated by Django 3.2.6 on 2021-08-08 14:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_post_claps'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='claps',
            field=models.PositiveSmallIntegerField(default=0),
        ),
    ]
