# Generated by Django 2.1.5 on 2019-03-14 11:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('archive', '0002_auto_20190314_0412'),
    ]

    operations = [
        migrations.AddField(
            model_name='scholarship',
            name='disbursement',
            field=models.CharField(default=100, help_text='Ammount distributed', max_length=13, verbose_name='ISBN'),
            preserve_default=False,
        ),
    ]
