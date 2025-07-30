from django.db import models
from django.core.validators import MinValueValidator
from phonenumber_field.modelfields import PhoneNumberField
from django.db.models import Sum, F


class CustomQueryset(models.QuerySet):

    def total_price(self):
        price = self.annotate(
            total_price=Sum(
                F('order_elements__product__price') * F('order_elements__quantity')
            )
        )
        return price


class Restaurant(models.Model):
    name = models.CharField(
        'название',
        max_length=50
    )
    address = models.CharField(
        'адрес',
        max_length=100,
        blank=True,
    )
    contact_phone = models.CharField(
        'контактный телефон',
        max_length=50,
        blank=True,
    )

    class Meta:
        verbose_name = 'ресторан'
        verbose_name_plural = 'рестораны'

    def __str__(self):
        return self.name


class ProductQuerySet(models.QuerySet):
    def available(self):
        products = (
            RestaurantMenuItem.objects
            .filter(availability=True)
            .values_list('product')
        )
        return self.filter(pk__in=products)


class ProductCategory(models.Model):
    name = models.CharField(
        'название',
        max_length=50
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(
        'название',
        max_length=50
    )
    category = models.ForeignKey(
        ProductCategory,
        verbose_name='категория',
        related_name='products',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    price = models.DecimalField(
        'цена',
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    image = models.ImageField(
        'картинка'
    )
    special_status = models.BooleanField(
        'спец.предложение',
        default=False,
        db_index=True,
    )
    description = models.TextField(
        'описание',
        max_length=250,
        blank=True,
    )

    objects = ProductQuerySet.as_manager()

    class Meta:
        verbose_name = 'товар'
        verbose_name_plural = 'товары'

    def __str__(self):
        return self.name


class RestaurantMenuItem(models.Model):
    restaurant = models.ForeignKey(
        Restaurant,
        related_name='menu_items',
        verbose_name="ресторан",
        on_delete=models.CASCADE,
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='menu_items',
        verbose_name='продукт',
    )
    availability = models.BooleanField(
        'в продаже',
        default=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'пункт меню ресторана'
        verbose_name_plural = 'пункты меню ресторана'
        unique_together = [
            ['restaurant', 'product']
        ]

    def __str__(self):
        return f'{self.restaurant.name} - {self.product.name}'


class Order(models.Model):
    ORDER_CHOICES = [
        ('order collected', 'заказ собран'),
        ('unprocessed', 'необработанный'),
        ('handed over to the courier', 'передан курьеру'),
        ('completed', 'выполнен'),
    ]
    PAYMENT_METHOD_CHOICES = [
        ('electronically', 'Электронно'),
        ('in_cash', 'Наличностью')
    ]
    status = models.CharField(
        max_length=30,
        db_index=True,
        verbose_name='статус',
        choices=ORDER_CHOICES,
        default=ORDER_CHOICES[1][0]
    )
    address = models.CharField(
        verbose_name='адрес',
        max_length=200
    )
    firstname = models.CharField(
        verbose_name='имя',
        max_length=100
    )
    lastname = models.CharField(
        verbose_name='фамилия',
        max_length=100
    )
    phonenumber = PhoneNumberField(
        verbose_name='мобильный номер',
    )
    comment = models.TextField(
        max_length=200,
        verbose_name='комментарий',
        blank=True,
    )
    registered_at = models.DateTimeField(
        verbose_name='дата регистрации',
        auto_now_add=True,
        db_index=True,
    )
    called_at = models.DateTimeField(
        verbose_name='дата звонка',
        null=True,
        blank=True,
    )
    delivered_at = models.DateTimeField(
        verbose_name='дата доставки',
        null=True,
        blank=True,
    )
    payment_method = models.CharField(
        verbose_name='способ оплаты',
        max_length=30,
        db_index=True,
        choices=PAYMENT_METHOD_CHOICES,
        default=PAYMENT_METHOD_CHOICES[1][0]
    )
    restaurant = models.ForeignKey(
        Restaurant,
        verbose_name='рестораны',
        related_name='orders',
        blank=True,
        null=True,
        on_delete=models.CASCADE
    )
    objects = CustomQueryset.as_manager()

    class Meta:
        verbose_name = 'заказ'
        verbose_name_plural = 'заказы'

    def __str__(self):
        return f'{self.firstname} {self.lastname} {self.address}'


class OrderElement(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='order_elements'
    )
    product = models.ForeignKey(
        Product,
        verbose_name='товар',
        on_delete=models.CASCADE,
        related_name='order_elements'
    )
    quantity = models.IntegerField(
        verbose_name='количество',
        validators=[MinValueValidator(1)],
        db_index=True
    )
    price = models.DecimalField(
        verbose_name='цена',
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )

    class Meta:
        ordering = ['quantity']
        verbose_name = 'элемент заказа'
        verbose_name_plural = 'элементы заказов'
        unique_together = [
            ['order', 'product']
        ]

    def __str__(self):
        return self.product.name
