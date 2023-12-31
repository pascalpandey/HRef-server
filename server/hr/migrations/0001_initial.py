# Generated by Django 4.2.5 on 2023-10-01 03:40

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Candidate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('keywords', models.JSONField(default=list)),
                ('color', models.CharField(max_length=255)),
                ('resume_link', models.URLField()),
                ('score', models.DecimalField(decimal_places=1, max_digits=3)),
                ('x', models.FloatField()),
                ('y', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('keywords', models.JSONField(default=list)),
                ('color', models.CharField(max_length=255)),
                ('resume_link', models.URLField()),
                ('score', models.DecimalField(decimal_places=1, max_digits=3)),
                ('x', models.FloatField()),
                ('y', models.FloatField()),
            ],
        ),
    ]
