# This file is part of account_invoice_ar_currency module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.

from trytond.model import fields
from trytond.pool import PoolMeta
from trytond.pyson import Eval, Bool


class Company(metaclass=PoolMeta):
    __name__ = 'company.company'

    force_currency_invoice_out = fields.Boolean(
        "Set currency for customer invoice",
        help="Force specific currency for customer invoice.")
    currency_invoice_out = fields.Many2One('currency.currency',
        "Currency for invoice",
        states={
            'invisible': ~Bool(Eval('force_currency_invoice_out')),
            'required': Bool(Eval('force_currency_invoice_out')),
            })

    @classmethod
    def default_force_currency_invoice_out(cls):
        return False
