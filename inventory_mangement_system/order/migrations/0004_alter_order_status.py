# Generated by Django 5.0.1 on 2024-04-01 09:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0003_alter_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[(0, 'pending'), (1, 'completed'), (2, 'return'), (3, 'Damaged'), (4, 'cancel')], default=0, max_length=50),
        ),
    ]
