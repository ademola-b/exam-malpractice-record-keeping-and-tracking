# Generated by Django 4.2.3 on 2023-07-06 17:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('malpractice_tracking', '0003_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='fillformmodel',
            options={'verbose_name_plural': 'Fill Form'},
        ),
        migrations.AlterField(
            model_name='fillformmodel',
            name='name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='fillformmodel',
            name='registration_no',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]
