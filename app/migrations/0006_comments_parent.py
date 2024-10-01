# Generated by Django 5.0.2 on 2024-03-06 17:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_comments'),
    ]

    operations = [
        migrations.AddField(
            model_name='comments',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='replies', to='app.comments'),
        ),
    ]
