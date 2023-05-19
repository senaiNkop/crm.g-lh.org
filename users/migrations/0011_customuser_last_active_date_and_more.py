# Generated by Django 4.2.1 on 2023-05-10 16:29

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_alter_customuser_gender'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='last_active_date',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='Last active date'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='blood_group',
            field=models.CharField(choices=[('-', 'Unknown'), ('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'), ('AB+', 'AB-'), ('O+', 'O+'), ('O-', 'O-')], max_length=10, verbose_name='Blood Group'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='genotype',
            field=models.CharField(choices=[('-', 'Unknown'), ('AA', 'AA'), ('AB', 'AB'), ('AO', 'AO'), ('BB', 'BB'), ('BO', 'BO'), ('OO', 'OO'), ('AS', 'AS'), ('SS', 'SS')], max_length=10, verbose_name='Genotype'),
        ),
    ]
