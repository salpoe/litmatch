# Generated by Django 2.0 on 2018-01-06 04:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recommendation',
            name='title',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]