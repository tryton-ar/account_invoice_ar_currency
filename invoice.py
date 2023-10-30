# This file is part of account_invoice_ar_currency module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.

from trytond.model import ModelView, fields
from trytond.wizard import Wizard, StateView, StateTransition, Button
from trytond.pool import PoolMeta, Pool
from trytond.pyson import Eval
from trytond.transaction import Transaction


class Invoice(metaclass=PoolMeta):
    __name__ = 'account.invoice'

    @classmethod
    def __setup__(cls):
        super().__setup__()
        cls._buttons.update({
            'update_currency': {
                'invisible': Eval('state') != 'draft'
                },
            })

    @classmethod
    @ModelView.button_action(
        'account_invoice_ar_currency.wiz_account_invoice_update_currency')
    def update_currency(cls, invoices):
        pass

    @classmethod
    def validate_invoice(cls, invoices):
        for invoice in invoices:
            if invoice.type == 'in' or \
                    invoice.company.force_currency_invoice_out is False:
                continue
            to_currency = invoice.company.currency_invoice_out
            if invoice.currency == to_currency:
                continue
            if invoice.pos and invoice.pos.pos_type == 'electronic' and \
                    invoice.pos.pyafipws_electronic_invoice_service == 'wsfex':
                continue
            invoice.change_currency(to_currency)
        super().validate_invoice(invoices)

    def change_currency(self, to_currency):
        pool = Pool()
        InvoiceLine = pool.get('account.invoice.line')
        Currency = pool.get('currency.currency')

        lines_to_save = []
        for l in self.lines:
            line = InvoiceLine(l.id)
            line.currency = to_currency
            with Transaction().set_context(
                    currency_rate=self.currency_rate,
                    date=self.currency_date):
                line.unit_price = Currency.compute(self.currency,
                    line.unit_price, to_currency)
            lines_to_save.append(line)
        if lines_to_save:
            InvoiceLine.save(lines_to_save)

        self.currency = to_currency
        self.currency_rate = (self.company.currency.rate /
            to_currency.rate)
        self.save()


class InvoiceUpdateCurrencyStart(ModelView):
    'Invoice Update Currency Start'
    __name__ = 'account.invoice.update_currency.start'

    currency = fields.Many2One('currency.currency', 'Currency', required=True)


class InvoiceUpdateCurrency(Wizard):
    'Invoice Update Currency'
    __name__ = 'account.invoice.update_currency'

    start = StateView(
        'account.invoice.update_currency.start',
        'account_invoice_ar_currency.update_currency_start_view_form', [
            Button('Cancel', 'end', 'tryton-cancel'),
            Button('Update', 'update', 'tryton-ok', default=True),
            ])
    update = StateTransition()

    def transition_update(self):
        pool = Pool()
        Invoice = pool.get('account.invoice')

        invoice = Invoice(Transaction().context['active_id'])
        # Export POS: do not change currency
        if invoice.pos and invoice.pos.pos_type == 'electronic' and \
                invoice.pos.pyafipws_electronic_invoice_service == 'wsfex':
            return 'end'
        if invoice.currency != self.start.currency:
            invoice.change_currency(self.start.currency)

        return 'end'
