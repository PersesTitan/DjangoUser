# Generated by Django 4.1.1 on 2022-09-23 03:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_alter_member_login_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='login_id',
            field=models.CharField(max_length=256, unique=True),
        ),
    ]