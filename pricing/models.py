from django.db import models
from cms.mixins import Numbered

class BWPrice(models.Model):
    amount = models.PositiveIntegerField('totaal aantal')
    price = models.DecimalField('prijs per zijde', max_digits=8, decimal_places=3)

    def __str__(self):
        return f'vanaf {self.amount} zijdes {self.price} per zijde)'

    class Meta:
        ordering = ['amount']
        verbose_name = 'Zwart/wit prijs'
        verbose_name_plural = 'Zwart/wit prijzen'

class FCPrice(models.Model):
    amount = models.PositiveIntegerField('totaal aantal')
    price = models.DecimalField('prijs per zijde', max_digits=8, decimal_places=2)

    def __str__(self):
        return f'vanaf {self.amount} zijdes {self.price} per zijde'

    class Meta:
        ordering = ['amount']
        verbose_name = 'Kleurenprijs'
        verbose_name_plural = 'Kleurenprijzen'
