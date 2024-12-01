import os
import math
from decimal import Decimal
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.conf import settings
from pricing.models import *
from homepage.utils import get_config
from .utils import *
from .models import *
from .forms import *

def calculate_invoice(prints):
    invoice = {}
    invoice['prints'] = []
    total = 0
    total_pages = 0
    total_fc_pages = 0
    total_bw_pages = 0
    total_amount = 0
    total_sheets = 0
    LOWVAT = 9
    STUDENT_DISCOUNT = 8

    for p in prints:
        items = []
        subtotal = 0
        lowvat = p.binding and p.sheets > 1
        if p.binding == 4 and p.papersize == 4:
            p.papersize = 3
        elif p.binding == 4 and p.papersize == 5:
            p.papersize = 4

        if p.binding == 4:
            lowvat = p.pages > 15

        if p.bw_pages > 0:
            if p.papersize == 3:
                multiplier = 2
            if p.papersize == 4:
                multiplier = 1
            if p.papersize == 5:
                multiplier = Decimal(.5)

            bw = BWPrice.objects.filter(amount__lte=total_bw_pages * multiplier).order_by('amount').last()
            nextbw = BWPrice.objects.filter(amount__gt=bw.amount).order_by('amount').first()
            amount = p.amount * p.bw_pages
            subsubtotal = amount * bw.price * multiplier if p.duplex == 1 else amount * bw.price_duplex * multiplier
            staffel = bw

            if nextbw:
                altsubsubtotal = nextbw.amount * nextbw.price if p.duplex == 1 else nextbw.amount * nextbw.price_duplex
                if altsubsubtotal < subsubtotal:
                    subsubtotal = altsubsubtotal
                    staffel = nextbw

            if lowvat:
                bare = subsubtotal / Decimal(1.21)
                subsubtotal = Decimal(1 + LOWVAT/100) * bare

            subtotal += subsubtotal

            items.append({
                'amount': amount,
                'description': 'A{} Zwart/wit prints'.format(p.papersize),
                'subsubtotal': subsubtotal,
                'staffel': staffel,
            })

        if p.fc_pages > 0:
            if p.papersize == 3:
                multiplier = 2
            if p.papersize == 4:
                multiplier = 1
            if p.papersize == 5:
                multiplier = Decimal(.5)

            fc = FCPrice.objects.filter(amount__lte=total_fc_pages * multiplier).order_by('amount').last()
            nextfc = FCPrice.objects.filter(amount__gt=fc.amount).order_by('amount').first()
            amount = p.amount * p.fc_pages
            subsubtotal = amount * fc.price * multiplier
            staffel = fc

            if nextfc:
                altsubsubtotal = nextfc.amount * nextfc.price
                if altsubsubtotal < subsubtotal:
                    subsubtotal = altsubsubtotal
                    staffel = nextfc
            
            if lowvat:
                bare = subsubtotal / Decimal(1.21)
                subsubtotal = Decimal(1 + LOWVAT/100) * bare

            subtotal += subsubtotal

            items.append({
                'amount': amount,
                'description': 'A{} Kleurenprints'.format(p.papersize),
                'subsubtotal': subsubtotal,
                'staffel': staffel,
            })

        if p.papertype.price:
            if p.papersize == 3:
                price = p.papertype.price * 2
            if p.papersize == 4:
                price = p.papertype.price
            if p.papersize == 5:
                price = Decimal(p.papertype.price / 2)
            if lowvat:
                bare = price / Decimal(1.21)
                price = Decimal(1 + LOWVAT/100) * bare

            amount = p.sheets * p.amount
            subsubtotal = amount * price
            subtotal += subsubtotal

            items.append({
                'amount': amount,
                'description': 'A{} {}'.format(p.papersize, p.papertype.name),
                'price': price,
                'subsubtotal': subsubtotal,
            })

            discount = PaperDiscount.objects.filter(amount__lte=p.sheets * p.amount).order_by('amount').last()
            if discount:
                price = discount.discount * subsubtotal / Decimal(100)
                subsubtotal = -price
                subtotal -= price
                items.append({
                    'amount': 1,
                    'description': '{}% papierkorting'.format(discount.discount),
                    'price': None,
                    'subsubtotal': subsubtotal,
                })

        if p.papersize == 3:
            price = Decimal(0.1) * subtotal
            subsubtotal = -price
            subtotal -= price
            items.append({
                'amount': 1,
                'description': '10% extra korting vanwege de A3 actie',
                'price': None,
                'subsubtotal': subsubtotal,
            })


        if p.binding in [1,2,3] and p.sheets > 1:
            if p.binding == 1:
                BindPrice = PlasticBindPrice
                description = 'Inbinden met plastic ring'
            if p.binding == 2:
                BindPrice = MetalBindPrice
                description = 'Inbinden met metalen ring'
            if p.binding == 3:
                BindPrice = GlueBindPrice
                description = 'Inbinden met lijmband'
            try:
                price = BindPrice.objects.filter(amount__lte=p.sheets).order_by('amount').last().price
                if p.papersize == 3 and p.binding != 3:
                    price = price * 2
                if lowvat:
                    bare = price / Decimal(1.21)
                    price = Decimal(1 + LOWVAT/100) * bare
            except:
                price = 0

            subsubtotal = p.amount * price
            subtotal += subsubtotal
            items.append({
                'amount': p.amount,
                'description': description,
                'price': price,
                'subsubtotal': subsubtotal,
            })

            discount = BindDiscount.objects.filter(amount__lte=total_amount).order_by('amount').last()
            if discount:
                price = discount.discount * subsubtotal / Decimal(100) # WARNING: this uses the previous subsubtotal
                subsubtotal = -price
                subtotal -= price
                items.append({
                    'amount': 1,
                    'description': '{}% inbindkorting'.format(discount.discount),
                    'price': None,
                    'subsubtotal': subsubtotal,
                })

            price = CoverPrice.objects.filter(amount__lte=p.amount).order_by('amount').last().price
            if p.papersize == 3:
                price = price * 2
            if lowvat:
                bare = price / Decimal(1.21)
                price = Decimal(1 + LOWVAT/100) * bare
            amount = p.amount * 2
            subsubtotal = price * amount
            subtotal += subsubtotal
            items.append({
                'amount': amount,
                'description': 'Plastic kaft',
                'price': price,
                'subsubtotal': subsubtotal,
            })

        if p.binding == 4:
            price = Decimal(0.25)
            if p.papersize == 3:
                price = price * 2
            if lowvat:
                bare = price / Decimal(1.21)
                price = Decimal(1 + LOWVAT/100) * bare
            amount = p.amount
            subsubtotal = price * amount
            subtotal += subsubtotal
            items.append({
                'amount': amount,
                'description': 'Vouwen + nieten',
                'price': price,
                'subsubtotal': subsubtotal,
            })

        if p.student_discount:
            price = Decimal(STUDENT_DISCOUNT/100) * subtotal
            subsubtotal = -price
            subtotal -= price
            items.append({
                'amount': 1,
                'description': '{}% studentenkorting'.format(STUDENT_DISCOUNT),
                'price': None,
                'subsubtotal': subsubtotal,
            })

        total += subtotal

        invoice['prints'].append({
            'print': p,
            'items': items,
            'subtotal': subtotal,
            'lowvat': lowvat,
        })

    invoice['total'] = total
    return invoice
