# Generated by Django 3.1.1 on 2020-09-26 17:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('urlbutcher', '0006_auto_20200926_1621'),
    ]

    operations = [
        migrations.RenameField(
            model_name='slugclick',
            old_name='clicks',
            new_name='click_counter',
        ),
    ]