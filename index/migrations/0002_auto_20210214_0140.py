# Generated by Django 3.1.4 on 2021-02-13 16:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='portfolio',
            unique_together={('name', 'years', 'period')},
        ),
    ]
