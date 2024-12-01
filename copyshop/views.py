import logging

from django.urls import reverse
from django.conf import settings
from django.http import HttpResponse
from django.views.generic import edit
from django.core.mail import EmailMessage
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import SuspiciousOperation
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.decorators.http import require_http_methods
from django.shortcuts import render, redirect, get_object_or_404

from mollie.api.client import Client
from cms.decorators import section_view
from cms.views import SectionView, SectionFormView

from pricing.forms import CalculatorForm
from .models import Page, Order
from .forms import *

logger = logging.getLogger('django.request')
mollie_client = Client()
mollie_client.set_api_key(settings.MOLLIE_API_KEY)

@csrf_exempt
@require_http_methods(['POST'])
def webhook(request):
    try:
        payment_id = request.POST.get('id')
        payment = mollie_client.payments.get(payment_id)
        order_id = payment.metadata['order_id']
        order = Order.objects.get(id=order_id)
        if order.status == payment.status or order.status == 'paid':
            raise SuspiciousOperation(
                f'Something weird happened:'
                f'Mollie called the webhook with status = "{payment.status}"'
                f'but the order status is already "{order.status}"')
        order.status = payment.status
        order.save()
        if order.status == 'paid':
            send_email(order)

    except Exception:
        import traceback
        logger.error(traceback.format_exc())

    # Always return successfully, as to not leak information
    return HttpResponse()

def get_payment_url(order):
    amount = {
        'currency': 'EUR',
        'value': f'{order.total:.2f}',
        }
    description = order.get_description()
    webhookUrl = settings.CANONICAL_URL + reverse('webhook')
    redirectUrl = settings.CANONICAL_URL + '/betaald/'
    metadata = {'order_id': str(order.id)}
    payment = mollie_client.payments.create({
        'amount': amount,
        'description': description,
        'webhookUrl': webhookUrl,
        'redirectUrl': redirectUrl,
        'metadata': metadata,
    })
    return payment.checkout_url

def send_email(order):
    body = f'''Beste Copyshoppers,

Iemand heeft een betaling voltooid met iDeal. Dat betekent dat we nu
zo snel mogelijk aan de slag moeten om deze bestelling te printen en
te versturen!

Je kunt de details van deze bestelling bekijken op:
https://www.copyshopdenbosch.nl/admin/copyshop/order/{order.pk}/change/

Als je contact op wilt nemen met de besteller kan dat door simpelweg
op deze email te antwoorden. Het Reply-To adres is ingesteld op
{order.email}.

Vergeet niet deze tekst te verwijderen uit je antwoord :-)

Groeten,
De server op Copyshopdenbosch.nl
'''
    email = EmailMessage(
        to=settings.DEFAULT_TO_EMAIL,
        from_email=settings.DEFAULT_FROM_EMAIL,
        body=body,
        subject=order.get_description(),
        headers={'Reply-To': order.email},
    )
    email.send()

class Checkout(edit.UpdateView):
    model = Order
    form_class = CheckoutForm
    template_name = 'copyshop/checkout.html'

    def form_valid(self, form):
        order = form.save()
        if settings.DEBUG:
            send_email(order)
            return redirect('/betaald/')
        if order.status == 'paid':
            return redirect('/betaald/')
        payment_url = get_payment_url(order)
        return redirect(payment_url)

    def get_object(self):
        token = self.kwargs['token']
        return get_object_or_404(Order, token=token)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total'] = self.object.total
        return context

class CreateOrder(UserPassesTestMixin, edit.CreateView):
    model = Order
    form_class = CreateOrderForm
    template_name = 'copyshop/create_order.html'

    def test_func(self):
        return self.request.user.has_perm('copyshop.add_order')

    def get_success_url(self):
        return reverse('admin:copyshop_order_changelist')

@section_view
class Text(SectionView):
    verbose_name = 'Tekst'
    fields = ['content', 'image']
    template_name = 'copyshop/text.html'

@section_view
class Banner(SectionView):
    verbose_name = 'Banner'
    fields = ['content']
    template_name = 'copyshop/banner.html'

@section_view
class Products(SectionView):
    verbose_name = 'Producten'
    fields = []
    template_name = 'copyshop/products.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pages'] = Page.objects.filter(menu=True)
        return context

@section_view
class Hours(SectionView):
    verbose_name = 'Openingstijden'
    fields = ['hours']
    template_name = 'copyshop/hours.html'

@section_view
class Map(SectionView):
    verbose_name = 'Route'
    fields = []
    template_name = 'copyshop/map.html'

@section_view
class Contact(SectionFormView):
    verbose_name = 'Contact'
    fields = ['content']
    form_class = ContactForm
    template_name = 'copyshop/contact.html'

    def form_valid(self, form):
        response = HttpResponse(status=302)
        response["Location"] = form.save()
        return response

@section_view
class Calculator(SectionFormView):
    verbose_name = 'Berekenmodule'
    fields = ['content']
    form_class = CalculatorForm
    success_url = '/thanks/'
    template_name = 'copyshop/calculator.html'

    def form_valid(self, form):
        items, total = form.save()
        return render(self.request, 'copyshop/result.html', {
            'items': items,
            'total': total,
        })
