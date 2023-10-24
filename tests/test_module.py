# This file is part of Tryton.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.

from trytond.tests.test_tryton import ModuleTestCase


class InvoiceCurrencyTestCase(ModuleTestCase):
    'Test account_invoice_ar_currency module'
    module = 'account_invoice_ar_currency'


del ModuleTestCase
