# Generated by Django 5.0.2 on 2024-03-28 09:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[(0, 'pending'), (1, 'completed')], default=0, max_length=50),
        ),
    ]
