# Generated by Django 4.2.7 on 2023-12-08 17:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinfo',
            name='avatarBinary',
            field=models.BinaryField(null=True),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='avatar',
            field=models.FileField(null=True, upload_to='avatar/'),
        ),
    ]
