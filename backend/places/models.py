from django.db import models


class Place(models.Model):
    address = models.CharField(
        max_length=100,
        verbose_name='адрес места',
        unique=True,
    )
    lng = models.DecimalField(
        verbose_name='долгота',
        max_digits=9,
        decimal_places=2,
        blank=True,
        null=True,
    )
    lat = models.DecimalField(
        verbose_name='широта',
        max_digits=9,
        decimal_places=2,
        blank=True,
        null=True,
    )
    date = models.DateTimeField(
        verbose_name='дата',
        auto_now=True,
        db_index=True,
    )

    class Meta:
        verbose_name = 'место'
        verbose_name_plural = 'места'

    def __str__(self):
        return self.address
