# Generated by Django 4.2.3 on 2023-07-06 17:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('malpractice_tracking', '0004_alter_fillformmodel_options_alter_fillformmodel_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fillformmodel',
            name='date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
