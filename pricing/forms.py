from django import forms
from .models import *

def get_rate(Price, amount):
    rate = Price.objects.filter(amount__lte=amount).order_by('amount').last()
    nextrate = Price.objects.filter(amount__gt=rate.amount).order_by('amount').first()
    if nextrate:
        return min(amount * rate.price, nextrate.amount * nextrate.price)
    return amount * rate.price

class CalculatorForm(forms.Form):
    bw_pages = forms.IntegerField(label='aantal zijdes zwart/wit', min_value=0)
    fc_pages = forms.IntegerField(label='aantal zijdes kleur', min_value=0)
    amount = forms.IntegerField(label='aantal exemplaren', initial=1, min_value=1)

    def save(self):
        bw_pages = self.cleaned_data['bw_pages']
        fc_pages = self.cleaned_data['fc_pages']
        amount = self.cleaned_data['amount']

        items = []
        total = 0

        if bw_pages > 0:
            bw_amount = amount * bw_pages
            subtotal = get_rate(BWPrice, bw_amount)
            total += subtotal

            items.append({
                'amount': bw_amount,
                'description': 'Zwart/wit A4 prints',
                'subtotal': subtotal,
            })

        if fc_pages > 0:
            fc_amount = amount * fc_pages
            subtotal = get_rate(FCPrice, fc_amount)
            total += subtotal

            items.append({
                'amount': fc_amount,
                'description': 'Kleuren A4 prints',
                'subtotal': subtotal,
            })

        return (items, total)
