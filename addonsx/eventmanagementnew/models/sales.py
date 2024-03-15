from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta
try:
    import qrcode
except ImportError:
    qrcode = None
try:
    import base64
except ImportError:
    base64 = None
from io import BytesIO


#represents sales records associated with ticket transactions
class SalesDoodex (models.Model):
    _name = 'doodex.sales'
    _description = 'page_sales'
    _rec_name = 'ref_sales'

    ref_sales = fields.Char(string='No. Reference', required=True, readonly=True, default=lambda self:_('New'))
    payment_method = fields.Selection(string='Payment Method', selection=[('transferbank', 'Transfer Bank'), ('cashonmitra', 'Cash On Mitra')])
    state = fields.Selection(selection=[
        ('confirm', 'Confirm'),
        ('pending', 'Pending'), 
        ('paid', 'Paid')], 
        string='State', 
        required=True, default='confirm')

    sum_pay = fields.Integer(compute='_compute_sum_pay', string='Amount', store=True)
    total_qty = fields.Integer(compute='_compute_total_qty', string='Total Ticket')
    detailsales_ids = fields.One2many(comodel_name='doodex.detailsales', inverse_name='sales_id', string='Detail Payment')
    qr_code = fields.Char(compute='_compute_qr_code', string='QR Code')
    cust_id = fields.Many2one(comodel_name='res.partner', string='Customer', required=True)
    date_trans = fields.Datetime(string='Date of Transaction',readonly=True, default=fields.Datetime.now())
    amount = fields.Integer(compute='_compute_amount', string='Amount',store=True)

    # for calculate from subtotal
    @api.depends('detailsales_ids')
    def _compute_amount(self):
            for rec in self:
                a = self.env['doodex.detailsales'].search([('sales_id','=',rec.id)]).mapped('subtotal')           
                total = sum(a)
                rec.amount=total


    # action for states
    @api.depends('ref_sales')
    def action_confirm(self):
        self.write({'state':'confirm'})
    def action_pending(self):
        self.write({'state':'pending'})
    def action_paid(self):
        if not self.payment_method:
            raise ValidationError(_('Choose your Payment Method first!'))
        self.write({'state':'paid'})


    # calculate for quantity of payment
    @api.depends('detailsales_ids.qty_payment')
    def _compute_total_qty(self):
        for rec in self:
            total_qty = sum(rec.detailsales_ids.mapped('qty_payment'))
            rec.total_qty = total_qty

    # compute for QRCode
    @api.depends('ref_sales')
    def _compute_qr_code(self):
        for rec in self:
            if qrcode and base64:
                qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L,box_size=3, border=4)
                qr.add_data(rec.ref_sales)
                qr.make(fit=True)
                img = qr.make_image()
                temp = BytesIO()
                img.save(temp, format="PNG")
                qr_image = base64.b64encode(temp.getvalue())
                rec.update({'qr_code':qr_image})

       
    # no. referensi for payment
    @api.model
    def create (self, vals):
        if vals.get('ref_sales', _("New") == _("New")):
            vals['ref_sales'] = self.env['ir.sequence'].next_by_code('referensi.sales') or _("New")
        record = super(SalesDoodex, self).create(vals)
        return record

    # unlink
    def unlink(self):
        if self.filtered(lambda line:line.state == 'paid'):
            raise ValidationError('Cant delete ordered ticket!')
        elif self.detailsales_ids:
            a = []
            for detail in self:
                a = self.env['doodex.detailsales'].search([('sales_id','=',detail.id)])
            for ticket in a:
                ticket.event_id.qty += ticket.qty_payment
        record = super(SalesDoodex, self).unlink()
        return record



class DoodexDetailSales (models.Model):
    _name = 'doodex.detailsales'
    _description = 'model.technical.name'

    sales_id = fields.Many2one(comodel_name='doodex.sales',string='Sales', readonly=True)
    event_id = fields.Many2one(comodel_name='doodex.event', string='Tickets')
    event_name = fields.Char(compute='_compute_event_name', string='Event Name')
    qty_payment = fields.Integer('Qty Ticket', required=True)
    admin = fields.Char(compute='_compute_admin', string='Admin')
    unit_price = fields.Integer(compute='_compute_ticket', string='Unit Price', readonly=True)
    subtotal = fields.Integer(compute='_compute_subtotal', string='Subtotal')
    disc_price = fields.Integer(compute='_compute_disc_price', string='Disc Price')    
    sales_mode = fields.Char(string='Sales Mode', compute='_compute_sales_mode', store=True)
    
    
    
    # for calculate date of preorder, h1, and ots
    @api.depends('event_id', 'sales_mode')
    def _compute_sales_mode(self):
        for ticket in self:
            event_date = ticket.event_id.date
            event_state = fields.Selection(ticket.event_id.state)
            today = fields.Datetime.now()

            if event_date and event_state == 'endprogress':
                ticket.sales_mode = 'ots'
            elif event_date and today < event_date and today == event_date - timedelta(days=1):
                ticket.sales_mode = 'h1'
            elif event_date and today < event_date and today <= event_date - timedelta(days=2):
                ticket.sales_mode = 'preorder'


    # for calculate discount price
    @api.depends('sales_mode', 'event_id')
    def _compute_disc_price(self):
        for ticket in self:
            if ticket.sales_mode == 'preorder':
                ticket.disc_price = 0.5 * ticket.event_id.price  # 50% discount
            elif ticket.sales_mode == 'h1':
                ticket.disc_price = 0.75 * ticket.event_id.price  # 25% discount
            else:
                ticket.disc_price = ticket.event_id.price

    # for calculate price and quantity
    @api.depends('disc_price', 'event_id')
    def _compute_subtotal(self):
        for rec in self:
            rec.subtotal = rec.disc_price*rec.qty_payment
    
    # call sales_staff name
    @api.depends('event_id')
    def _compute_admin(self):
        for rec in self:
            rec.admin = rec.event_id.admin_name
    
    

    # call name of event
    @api.depends('event_id')
    def _compute_event_name(self):
        for rec in self:
            rec.event_name = rec.event_id.name
    

    

    # call price from event_id
    @api.depends('event_id')
    def _compute_ticket(self):
        for r in self:
            r.unit_price = r.event_id.price

    # to return the quanity
    @api.model
    def create(self, vals):
        # this is for no. reference sales model
        record = super(DoodexDetailSales, self).create(vals)
        if vals.get('ref_sales', _("New") == _("New")):
            vals['ref_sales'] = self.env['ir.sequence'].next_by_code('id.referensi.sales') or _("New")
        #t his is for exceptions, quantity of ticket is required
        if 'qty_payment' in vals and not vals['qty_payment']:
            raise ValidationError(_('Quantity of Ticket must be filled in!'))
        # this is for exception if ticket already sold out
        if record.event_id.qty <= 0:
            raise ValidationError( _("Ticket is SOLD OUT!"))
        # this is for reduce stock when ticket already added to sales (buy)
        if record.qty_payment:
            self.env['doodex.event'].search([('id', '=', record.event_id.id)]).write({'qty': record.event_id.qty - record.qty_payment})
        

        return record
