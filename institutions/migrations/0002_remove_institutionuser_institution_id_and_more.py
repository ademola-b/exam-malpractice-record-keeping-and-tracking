# Generated by Django 4.2.3 on 2023-07-05 17:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('institutions', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='institutionuser',
            name='institution_id',
        ),
        migrations.RemoveField(
            model_name='institutionuser',
            name='user_id',
        ),
        migrations.DeleteModel(
            name='InstitutionProfile',
        ),
        migrations.DeleteModel(
            name='InstitutionUser',
        ),
    ]