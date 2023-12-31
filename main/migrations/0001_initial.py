# Generated by Django 4.2.3 on 2023-07-04 18:40

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="CustomUser",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "is_superuser",
                    models.BooleanField(
                        default=False,
                        help_text="Designates that this user has all permissions without explicitly assigning them.",
                        verbose_name="superuser status",
                    ),
                ),
                (
                    "username",
                    models.CharField(
                        error_messages={
                            "unique": "A user with that username already exists."
                        },
                        help_text="Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.",
                        max_length=150,
                        unique=True,
                        validators=[
                            django.contrib.auth.validators.UnicodeUsernameValidator()
                        ],
                        verbose_name="username",
                    ),
                ),
                (
                    "first_name",
                    models.CharField(
                        blank=True, max_length=150, verbose_name="first name"
                    ),
                ),
                (
                    "last_name",
                    models.CharField(
                        blank=True, max_length=150, verbose_name="last name"
                    ),
                ),
                (
                    "email",
                    models.EmailField(
                        blank=True, max_length=254, verbose_name="email address"
                    ),
                ),
                (
                    "is_staff",
                    models.BooleanField(
                        default=False,
                        help_text="Designates whether the user can log into this admin site.",
                        verbose_name="staff status",
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(
                        default=True,
                        help_text="Designates whether this user should be treated as active. Unselect this instead of deleting accounts.",
                        verbose_name="active",
                    ),
                ),
                (
                    "date_joined",
                    models.DateTimeField(
                        default=django.utils.timezone.now, verbose_name="date joined"
                    ),
                ),
                (
                    "user_type",
                    models.CharField(
                        choices=[
                            (1, "ShipperCompany"),
                            (2, "CarrierCompany"),
                            (3, "Science Staff"),
                        ],
                        default=1,
                        max_length=10,
                    ),
                ),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.group",
                        verbose_name="groups",
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Specific permissions for this user.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.permission",
                        verbose_name="user permissions",
                    ),
                ),
            ],
            options={
                "verbose_name": "user",
                "verbose_name_plural": "users",
                "abstract": False,
            },
            managers=[
                ("objects", django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name="Box",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("count", models.IntegerField(verbose_name="Количество")),
                ("length", models.FloatField(verbose_name="Длина")),
                ("width", models.FloatField(verbose_name="Ширина")),
                ("height", models.FloatField(verbose_name="Высота")),
                ("weight", models.FloatField(verbose_name="Вес")),
            ],
        ),
        migrations.CreateModel(
            name="Cargo",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "box",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.RESTRICT, to="main.box"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="CarrierCompany",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "companyname",
                    models.CharField(max_length=85, verbose_name="Компания перевозчик"),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "reiting",
                    models.FloatField(verbose_name="Рейтинг компании перевозчика"),
                ),
                (
                    "role",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Container",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("count", models.IntegerField(verbose_name="Count")),
                (
                    "type",
                    models.CharField(
                        choices=[("20DC", "20DC"), ("40DC", "40DC"), ("40HC", "40HC")],
                        default="20DC",
                        max_length=10,
                        verbose_name="Тип контейнера",
                    ),
                ),
                ("cargoWeight", models.FloatField(verbose_name="Вес груза")),
                ("contanerWeight", models.FloatField(verbose_name="Вес контейнера")),
                ("totalWeight", models.FloatField(verbose_name="Общий вес")),
            ],
        ),
        migrations.CreateModel(
            name="Driver",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "FirstName",
                    models.CharField(max_length=75, verbose_name="Имя водителя"),
                ),
                (
                    "LastName",
                    models.CharField(max_length=75, verbose_name="Фамилия водителя"),
                ),
                ("LicenseGetYear", models.DateTimeField(verbose_name="Дата лицензии")),
                ("driveExperienceYeares", models.DateTimeField()),
                ("reiting", models.FloatField(verbose_name="Личный рейтинг водителя")),
            ],
        ),
        migrations.CreateModel(
            name="Truck",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "numberTruck",
                    models.CharField(
                        error_messages={
                            "unique": "Трак с таким номером уже существует!"
                        },
                        max_length=7,
                        unique=True,
                        verbose_name="Номер трака",
                    ),
                ),
                (
                    "modelTruck",
                    models.CharField(max_length=25, verbose_name="Модель трака"),
                ),
                ("engine", models.FloatField(verbose_name="Объем двигателя")),
                ("power", models.IntegerField(verbose_name="Мощность двигателя")),
                ("truckYear", models.DateTimeField(verbose_name="Год выпуска трака")),
                ("weight", models.IntegerField(verbose_name="Грузоподъемность")),
            ],
        ),
        migrations.CreateModel(
            name="TruckAndDriverInfo",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "typeOfTrailer",
                    models.CharField(
                        choices=[
                            ("DRYVAN", "DRYVAN"),
                            ("REEFER", "FEEFER"),
                            ("FLATBED", "FLATBED"),
                        ],
                        default="DRYVAN",
                        max_length=10,
                        verbose_name="Тип трейлера",
                    ),
                ),
                (
                    "maxLoading",
                    models.IntegerField(verbose_name="Максимальная вместимость"),
                ),
                (
                    "insurance",
                    models.CharField(max_length=75, verbose_name="Страхование"),
                ),
                ("rpm", models.FloatField(verbose_name="Цена за милю")),
                (
                    "company",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.RESTRICT,
                        to="main.carriercompany",
                    ),
                ),
                (
                    "driver",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.RESTRICT,
                        to="main.driver",
                        verbose_name="Водитель",
                    ),
                ),
                (
                    "truck",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.RESTRICT, to="main.truck"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ShipperCompany",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "companyname",
                    models.CharField(max_length=85, verbose_name="Компания заказчик"),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "role",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Order",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("FREE", "FREE"),
                            ("INPROCESS", "INPROCESS"),
                            ("DONE", "DONE"),
                        ],
                        default="FREE",
                        max_length=10,
                        verbose_name="Статус",
                    ),
                ),
                ("departureDate", models.DateTimeField(verbose_name="Дата отправки")),
                (
                    "departureCity",
                    models.CharField(max_length=85, verbose_name="Город отправки"),
                ),
                (
                    "departureAddress",
                    models.CharField(max_length=85, verbose_name="Адрес отправки"),
                ),
                ("destinationDate", models.DateTimeField(verbose_name="Дата доставки")),
                (
                    "destinationCity",
                    models.CharField(max_length=85, verbose_name="Город доставки"),
                ),
                (
                    "destinationAddress",
                    models.CharField(max_length=85, verbose_name="Адрес доставки"),
                ),
                ("description", models.TextField(verbose_name="Описание")),
                ("reiting", models.FloatField(null=True, verbose_name="Рейтинг")),
                (
                    "cargo",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.RESTRICT, to="main.cargo"
                    ),
                ),
                (
                    "company",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.RESTRICT,
                        to="main.carriercompany",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="cargo",
            name="container",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.RESTRICT, to="main.container"
            ),
        ),
    ]
