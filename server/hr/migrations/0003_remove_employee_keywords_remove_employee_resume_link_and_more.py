# Generated by Django 4.2.5 on 2023-10-01 16:22

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("hr", "0002_remove_candidate_name_remove_employee_name_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="employee",
            name="keywords",
        ),
        migrations.RemoveField(
            model_name="employee",
            name="resume_link",
        ),
        migrations.AlterField(
            model_name="candidate",
            name="id",
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name="employee",
            name="id",
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]