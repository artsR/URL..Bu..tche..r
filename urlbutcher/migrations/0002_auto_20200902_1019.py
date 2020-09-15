# Generated by Django 3.1.1 on 2020-09-02 10:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('urlbutcher', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FunnyQuote',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('quote', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='Url',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('url', models.CharField(max_length=512)),
                ('slug', models.CharField(max_length=150)),
                ('created_at', models.DateTimeField()),
            ],
        ),
        migrations.DeleteModel(
            name='FunnyQuotes',
        ),
        migrations.DeleteModel(
            name='Urls',
        ),
    ]
