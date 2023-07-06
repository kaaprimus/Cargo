from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now

# Create your models here.

class CustomUser(AbstractUser):
    user_type_data = ((1, "ShipperCompany"), (2, "CarrierCompany"), (3, "Admin"))
    user_type = models.IntegerField(default=1, choices=user_type_data)

class Truck(models.Model):
    numberTruck = models.CharField(verbose_name="Номер трака", max_length=7, unique=True, error_messages={'unique':"Трак с таким номером уже существует!"})
    modelTruck = models.CharField(verbose_name="Модель трака", max_length=25)
    engine = models.FloatField(verbose_name="Объем двигателя")
    power = models.IntegerField(verbose_name="Мощность двигателя")
    truckYear = models.DateTimeField(verbose_name="Год выпуска трака", null=False)
    weight = models.IntegerField(verbose_name="Грузоподъемность")

    def __str__(self) -> str:
        return self.numberTruck

class Trailer(models.TextChoices):
    DRYVAN = "DRYVAN", "DRYVAN"
    REEFER = "REEFER", "FEEFER"
    FLATBED = "FLATBED", "FLATBED"

class StatusCargo(models.TextChoices):
    FREE = "FREE", "FREE"
    INPROCESS = "INPROCESS", "INPROCESS"
    DONE = "DONE", "DONE"

class ContainerType(models.TextChoices):
    FIRST = "20DC", "20DC"
    SECOND = "40DC", "40DC"
    THIRD = "40HC", "40HC"
    
class Driver(models.Model):
    FirstName = models.CharField(verbose_name="Имя водителя", max_length=75)
    LastName = models.CharField(verbose_name="Фамилия водителя", max_length=75)
    LicenseGetYear = models.DateTimeField(verbose_name="Дата лицензии", null=False)
    driveExperienceYeares = models.DateTimeField(null=False)
    reiting = models.FloatField(verbose_name="Личный рейтинг водителя")

    def __str__(self) -> str:
        return f"{self.FirstName} - {self.LastName}"
    
class CarrierCompany(models.Model):
    companyname = models.CharField(verbose_name="Компания перевозчик", max_length=85)
    role = models.OneToOneField(CustomUser, on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    reiting = models.FloatField(verbose_name="Рейтинг компании перевозчика")
    objects = models.Manager()

class ShipperCompany(models.Model):
    companyname = models.CharField(verbose_name="Компания заказчик", max_length=85)
    role = models.OneToOneField(CustomUser, on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

class TruckAndDriverInfo(models.Model):
    truck = models.ForeignKey(Truck, on_delete=models.RESTRICT)
    typeOfTrailer = models.CharField(max_length=10, verbose_name='Тип трейлера', choices=Trailer.choices, default=Trailer.DRYVAN) 
    maxLoading = models.IntegerField(verbose_name="Максимальная вместимость")
    driver = models.ForeignKey(Driver, on_delete = models.RESTRICT, verbose_name="Водитель")
    insurance = models.CharField(max_length=75, verbose_name="Страхование")
    rpm = models.FloatField(verbose_name="Цена за милю")
    company = models.ForeignKey(CarrierCompany, on_delete=models.RESTRICT)

class Container(models.Model):
    count = models.IntegerField(verbose_name="Count")
    type = models.CharField(max_length=10, verbose_name='Тип контейнера', choices=ContainerType.choices, default=ContainerType.FIRST)
    cargoWeight = models.FloatField(verbose_name="Вес груза")
    contanerWeight = models.FloatField(verbose_name="Вес контейнера")
    totalWeight = models.FloatField(verbose_name="Общий вес")

class Box(models.Model):
    count = models.IntegerField(verbose_name="Количество")
    length = models.FloatField(verbose_name="Длина")
    width = models.FloatField(verbose_name="Ширина")
    height = models.FloatField(verbose_name="Высота")
    weight = models.FloatField(verbose_name="Вес")

class Cargo(models.Model):
    container = models.ForeignKey(Container, on_delete=models.RESTRICT)
    box = models.ForeignKey(Box, on_delete=models.RESTRICT)

class Order(models.Model):
    cargo = models.ForeignKey(Cargo, on_delete=models.RESTRICT)
    status = models.CharField(max_length=10, verbose_name='Статус', choices=StatusCargo.choices, default=StatusCargo.FREE)
    departureDate = models.DateTimeField(verbose_name="Дата отправки")
    departureCity = models.CharField(verbose_name="Город отправки", max_length=85)
    departureAddress = models.CharField(verbose_name="Адрес отправки", max_length=85)
    destinationDate = models.DateTimeField(verbose_name="Дата доставки")
    destinationCity = models.CharField(verbose_name="Город доставки", max_length=85)
    destinationAddress = models.CharField(verbose_name="Адрес доставки", max_length=85)
    description = models.TextField(verbose_name="Описание")
    reiting = models.FloatField(verbose_name="Рейтинг", null=True)
    carrier_company = models.ForeignKey(CarrierCompany, on_delete=models.RESTRICT, null=True)
    shipper_company = models.ForeignKey(ShipperCompany, on_delete=models.RESTRICT, null=True)
    isDengerouse = models.BooleanField(default=False)

class Room(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Message(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    user = models.CharField(max_length=100)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user}: {self.content}'



