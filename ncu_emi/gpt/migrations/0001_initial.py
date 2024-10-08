# Generated by Django 5.1 on 2024-08-17 13:24

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Class",
            fields=[
                (
                    "class_id",
                    models.IntegerField(
                        db_column="Class_id", primary_key=True, serialize=False
                    ),
                ),
                (
                    "class_name",
                    models.CharField(
                        blank=True, db_column="Class_name", max_length=45, null=True
                    ),
                ),
                (
                    "class_path",
                    models.CharField(
                        blank=True, db_column="Class_path", max_length=45, null=True
                    ),
                ),
                (
                    "vector_store_id",
                    models.CharField(
                        blank=True,
                        db_column="Vector_store_id",
                        max_length=45,
                        null=True,
                    ),
                ),
            ],
            options={
                "db_table": "class",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="User",
            fields=[
                (
                    "user_id",
                    models.AutoField(
                        db_column="User_id", primary_key=True, serialize=False
                    ),
                ),
                ("user_name", models.CharField(db_column="User_name", max_length=45)),
                (
                    "user_account",
                    models.CharField(
                        db_column="User_account", max_length=45, unique=True
                    ),
                ),
                ("user_pw", models.CharField(db_column="User_pw", max_length=45)),
                ("is_active", models.IntegerField()),
                ("last_login", models.DateTimeField(blank=True, null=True)),
            ],
            options={
                "db_table": "user",
                "managed": False,
            },
        ),
    ]
