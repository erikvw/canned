# Generated by Django 3.2.13 on 2022-06-17 20:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('canned_views', '0004_auto_20220617_2306'),
    ]

    operations = [
        migrations.AddField(
            model_name='cannedviews',
            name='instructions',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='historicalcannedviews',
            name='instructions',
            field=models.TextField(null=True),
        ),
    ]