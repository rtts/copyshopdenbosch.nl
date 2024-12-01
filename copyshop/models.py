import string, random
from django.db import models
from django.urls import reverse
from cms.models import BasePage, BaseSection
from cms.fields import CharField
from cms.decorators import page_model, section_model

@page_model
class Page(BasePage):
    '''Add custom fields here. Already existing fields: title, slug,
    number, menu

    '''
    image = models.ImageField('afbeelding', blank=True)
    google_keywords = models.TextField('Google keywords', blank=True)
    google_description = models.TextField('Google description', blank=True)


@section_model
class Section(BaseSection):
    '''Add custom fields here. Already existing fields: title, type,
    number, content, image, video, href

    '''
    page = models.ForeignKey(Page, related_name='sections', on_delete=models.PROTECT)

class Download(models.Model):
    section = models.ForeignKey(Section, related_name='downloads', on_delete=models.CASCADE)
    title  = CharField('titel')
    description = CharField('Beschrijving', blank=True)
    file = models.FileField('Bestand')

    class Meta:
        ordering = ['pk']

class Hour(models.Model):
    DAYS = (
        ('Ma', 'Maandag'),
        ('Di', 'Dinsdag'),
        ('Wo', 'Woensdag'),
        ('Do', 'Donderdag'),
        ('Vr', 'Vrijdag'),
        ('Za', 'Zaterdag'),
        ('Zo', 'Zondag'),
    )
    section = models.ForeignKey(Section, related_name='hours', on_delete=models.CASCADE)
    day = models.CharField('Dag', choices=DAYS, max_length=2)
    hours = CharField('Geopend')
    note = CharField('Opmerking', blank=True)

    class Meta:
        ordering = ['pk']

ORDER_STATUSES = (
    # These are equal to the statuses that Mollie returns:
    ('open', 'nog niet betaald'),
    ('canceled', 'betaling geannuleerd'),
    ('expired', 'betaling verlopen'),
    ('failed', 'betaling mislukt'),
    ('paid', 'betaald'),
)

def get_token():
    length = 8
    chars = string.ascii_letters + string.digits
    unique = False
    while not unique:
        token = ''.join(random.choice(chars) for x in range(length))
        if not Order.objects.filter(token=token).exists():
            unique = True
    return token

class Order(models.Model):
    customer = CharField('naam')
    email = models.EmailField('e-mail')
    address = models.TextField('adres')
    phone = CharField('telefoonnummer')
    notes = models.TextField('opmerkingen', blank=True)

    total = models.DecimalField('totaalbedrag', max_digits=8, decimal_places=2)
    status = models.CharField('status', max_length=32, choices=ORDER_STATUSES, default=ORDER_STATUSES[0][0])
    created = models.DateTimeField('aangemaakt', auto_now_add=True)
    updated = models.DateTimeField('gewijzigd', auto_now=True)

    assignee = CharField('in behandeling door', blank=True)
    token = CharField(default=get_token)

    def __str__(self):
        return self.get_order_nr()

    def get_order_nr(self):
        year = self.created.year
        return f'C{year}{self.id:04d}'

    def get_description(self):
        return 'Bestelling met nummer ' + self.get_order_nr()

    class Meta:
        ordering = ['-created']
        verbose_name = 'bestelling'
        verbose_name_plural = 'bestellingen'
