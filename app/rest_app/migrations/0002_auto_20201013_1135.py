# Generated by Django 3.1.2 on 2020-10-13 11:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rest_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cache',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer', models.CharField(max_length=200)),
                ('spent_money', models.CharField(max_length=200)),
                ('gems', models.CharField(max_length=200)),
            ],
        ),
        migrations.AlterField(
            model_name='deal',
            name='date',
            field=models.DateTimeField(),
        ),
    ]