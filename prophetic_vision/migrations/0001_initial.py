# Generated by Django 4.1.7 on 2023-03-26 23:56

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PropheticVision',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=django.utils.timezone.now)),
                ('title', models.CharField(blank=True, max_length=1000, null=True)),
                ('body', models.TextField()),
            ],
            options={
                'ordering': ('-date',),
            },
        ),
    ]
