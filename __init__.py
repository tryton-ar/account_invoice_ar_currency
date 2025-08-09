# This file is part of account_invoice_ar_currency module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.

from trytond.pool import Pool
from . import company
from . import invoice

__all__ = ['register']


def register():
    Pool.register(
        company.Company,
        invoice.Invoice,
        invoice.InvoiceUpdateCurrencyStart,
        module='account_invoice_ar_currency', type_='model')
    Pool.register(
        invoice.InvoiceUpdateCurrency,
        module='account_invoice_ar_currency', type_='wizard')
