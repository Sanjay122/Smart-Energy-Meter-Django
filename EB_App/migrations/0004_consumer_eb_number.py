# Generated by Django 3.2.9 on 2021-11-24 14:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EB_App', '0003_auto_20211124_1948'),
    ]

    operations = [
        migrations.AddField(
            model_name='consumer',
            name='eb_number',
            field=models.CharField(default=0, max_length=14),
        ),
    ]
