# Generated by Django 4.2.6 on 2023-10-26 17:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bank', '0004_remove_person_credit_alter_account_credit'),
    ]

    operations = [
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('content', models.TextField()),
                ('pub_date', models.DateTimeField()),
            ],
        ),
    ]
