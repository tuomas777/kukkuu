# Generated by Django 2.2.10 on 2020-04-08 08:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("projects", "0001_initial"),
        ("children", "0004_add_child_postal_code"),
    ]

    operations = [
        migrations.AddField(
            model_name="child",
            name="project",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="children",
                to="projects.Project",
                verbose_name="project",
            ),
            preserve_default=False,
        ),
    ]
