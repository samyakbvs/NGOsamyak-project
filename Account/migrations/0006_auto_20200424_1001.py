# Generated by Django 3.0.3 on 2020-04-24 10:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Account', '0005_auto_20200424_0923'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='collection',
            name='Things',
        ),
        migrations.CreateModel(
            name='ThingsDonated',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=264)),
                ('quantity', models.IntegerField()),
                ('user', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='things', to='Account.Collection')),
            ],
        ),
    ]