# Generated by Django 4.1.7 on 2023-04-11 21:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feedback', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feedback',
            name='message',
            field=models.CharField(max_length=100),
        ),
    ]