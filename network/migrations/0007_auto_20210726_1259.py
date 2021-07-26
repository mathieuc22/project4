# Generated by Django 3.2.5 on 2021-07-26 12:59

from django.db import migrations, models
import django.db.models.expressions


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0006_auto_20210726_1255'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='following',
            name='user_notequal_follower',
        ),
        migrations.AddConstraint(
            model_name='following',
            constraint=models.CheckConstraint(check=models.Q(('user', django.db.models.expressions.F('following')), _negated=True), name='user_notequal_follower'),
        ),
    ]
