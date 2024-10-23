# Generated by Django 5.1.2 on 2024-10-19 18:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('driver', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='driver',
            old_name='licence_no',
            new_name='licence',
        ),
        migrations.RenameField(
            model_name='driver',
            old_name='phone_no',
            new_name='phone',
        ),
        migrations.RenameField(
            model_name='driver',
            old_name='vehicle_no',
            new_name='vehicle',
        ),
        migrations.RenameField(
            model_name='temporarydriver',
            old_name='licence_no',
            new_name='licence',
        ),
        migrations.RenameField(
            model_name='temporarydriver',
            old_name='phone_no',
            new_name='phone',
        ),
        migrations.RenameField(
            model_name='temporarydriver',
            old_name='vehicle_no',
            new_name='vehicle',
        ),
        migrations.RemoveField(
            model_name='driver',
            name='current_location',
        ),
        migrations.RemoveField(
            model_name='driver',
            name='is_active',
        ),
        migrations.RemoveField(
            model_name='driver',
            name='rating',
        ),
        migrations.AlterField(
            model_name='driver',
            name='auto_img',
            field=models.ImageField(blank=True, null=True, upload_to='uploads/temporarydrivers/'),
        ),
    ]