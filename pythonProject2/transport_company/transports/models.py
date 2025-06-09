from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal


class Driver(models.Model):
    CLASS_CHOICES = [
        ('1', 'Первый класс'),
        ('2', 'Второй класс'),
        ('3', 'Третий класс'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    full_name = models.CharField(max_length=100, verbose_name="ФИО")
    passport_number = models.CharField(max_length=20, verbose_name="Номер паспорта")
    experience = models.PositiveIntegerField(verbose_name="Стаж работы (лет)")
    driver_class = models.CharField(max_length=1, choices=CLASS_CHOICES, verbose_name="Классность")
    partner = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Напарник")

    def __str__(self):
        return f"{self.full_name} (класс {self.driver_class})"

    class Meta:
        verbose_name = "Водитель"
        verbose_name_plural = "Водители"
        ordering = ['full_name']


class Trailer(models.Model):
    brand = models.CharField(max_length=50, verbose_name="Марка")
    company = models.CharField(max_length=50, verbose_name="Фирма")
    license_plate = models.CharField(max_length=20, unique=True, verbose_name="Гос. номер")
    load_capacity = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Грузоподъемность (тонн)")
    fuel_consumption = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Расход топлива (л/100 км)")
    trailer_length = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Длина прицепа (м)")
    cost_per_km = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Стоимость перевозки (руб/км)",
        default=50.00
    )
    driver = models.ForeignKey(
        Driver,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Основной водитель"
    )

    def __str__(self):
        return f"{self.brand} {self.license_plate} ({self.load_capacity}т)"

    class Meta:
        verbose_name = "Трейлер"
        verbose_name_plural = "Трейлеры"
        ordering = ['brand']
        ordering = ['brand']


class Order(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название заказа")
    weight = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        verbose_name="Вес груза (тонн)"
    )
    items_count = models.PositiveIntegerField(verbose_name="Количество мест")
    departure_point = models.CharField(max_length=100, verbose_name="Пункт отправления")
    destination_point = models.CharField(max_length=100, verbose_name="Пункт назначения")
    distance = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Расстояние (км)"
    )
    trailer = models.ForeignKey(
        Trailer,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Трейлер"
    )
    driver = models.ForeignKey(
        Driver,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Водитель"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    completed = models.BooleanField(default=False, verbose_name="Завершен")

    @property
    def has_partner(self):
        """Требуется ли напарник для рейса"""
        return self.distance > Decimal('500.00') and self.driver.partner is not None

    def calculate_cost(self):
        """Расчет стоимости перевозки с правильной обработкой типов Decimal"""
        if not self.trailer or not self.distance:
            return Decimal('0.00')

        try:
            distance = Decimal(str(self.distance))
            cost_per_km = self.trailer.cost_per_km
            return (distance * cost_per_km).quantize(Decimal('0.00'))
        except (TypeError, AttributeError):
            return Decimal('0.00')

    def __str__(self):
        return f"Заказ #{self.id}: {self.departure_point} → {self.destination_point} ({self.weight}т)"

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['departure_point', 'destination_point']),
            models.Index(fields=['created_at']),
        ]