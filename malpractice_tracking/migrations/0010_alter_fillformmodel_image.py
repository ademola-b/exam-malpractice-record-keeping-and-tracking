# Generated by Django 4.2.3 on 2023-07-10 05:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('malpractice_tracking', '0009_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fillformmodel',
            name='image',
            field=models.ImageField(upload_to=''),
        ),
    ]
