# Generated by Django 4.0.3 on 2022-04-04 18:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('facility', '0006_remove_order_orderline_id_orderline_order_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='comment',
            field=models.CharField(blank=True, default=0, max_length=2000, verbose_name='Comment'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='orderline',
            name='order_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='orderlines', to='facility.order'),
        ),
    ]
