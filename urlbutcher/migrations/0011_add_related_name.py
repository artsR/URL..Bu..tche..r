# Generated by Django 3.1.1 on 2020-09-28 14:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('urlbutcher', '0010_create_SlugClickCounter_model'),
    ]

    operations = [
        migrations.AlterField(
            model_name='slugclickcounter',
            name='slug',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='counter', serialize=False, to='urlbutcher.url'),
        ),
    ]
