# Generated by Django 4.0.3 on 2022-04-05 15:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('facility', '0007_alter_order_comment_alter_orderline_order_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderline',
            name='eqModels_id',
        ),
        migrations.RemoveField(
            model_name='orderline',
            name='manufacturer_id',
        ),
        migrations.RemoveField(
            model_name='orderline',
            name='types_id',
        ),
        migrations.CreateModel(
            name='Equipement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.FloatField(help_text='Kaina', null=True)),
                ('eqModels_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='modelsequipements', to='facility.eqmodels')),
                ('manufacturer_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='manufactequipements', to='facility.manufacturers')),
                ('types_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='typesequipements', to='facility.types')),
            ],
        ),
        migrations.AddField(
            model_name='orderline',
            name='equipement_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='ordersline', to='facility.equipement'),
        ),
    ]