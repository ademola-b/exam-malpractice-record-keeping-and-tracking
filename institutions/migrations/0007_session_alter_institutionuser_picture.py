# Generated by Django 4.2.3 on 2023-07-06 13:52

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('institutions', '0006_alter_institutionuser_institution_user_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='Session',
            fields=[
                ('session_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('session', models.CharField(max_length=10)),
            ],
        ),
        migrations.AlterField(
            model_name='institutionuser',
            name='picture',
            field=models.ImageField(blank=True, default='img/default.jpg', null=True, upload_to=''),
        ),
    ]
