# Generated by Django 4.2.1 on 2023-05-14 19:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("ArtyProd", "0011_remove_equipe_img"),
    ]

    operations = [
        migrations.RemoveField(model_name="tache", name="titre",),
    ]