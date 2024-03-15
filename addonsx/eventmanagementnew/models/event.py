from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import datetime
# represent an event : name, desc, date, time, and venue

class EventDoodex (models.Model):
    _name = 'doodex.event'
    _description = 'page event'
    _rec_name = 'ref_event'

    ref_event = fields.Char(string='No. Reference', required=True, readonly=True, default=lambda self:_('New'))
    name = fields.Char(string='Event Name', required=True)
    desc = fields.Char(string='Description')
    date = fields.Datetime(string='Date', required=True)
    venue_id = fields.Many2one(comodel_name='doodex.venue', string='Venue', required=True)
    qty = fields.Integer(string='Quantity Avaiable', required=True)
    price = fields.Integer(string='Price', required=True)
    sales_staff_id = fields.Many2one(comodel_name='doodex.staff', string='Sales Staff', domain="[('staff','=','sales')]", required=True)
    
    name_venue = fields.Char(string='Place', readonly=True, related='venue_id.name')
    state = fields.Selection(selection=[
        ('draft', 'Draft'),
        ('onprogress', 'On Progress'),
        ('endprogress', 'End Progress'),
        ('cancel', 'Cancel'), 
        ], 
        string='State', 
        default='draft')
    
    admin_name = fields.Char(string='Admin', related='sales_staff_id.name', readonly=True, store=True)
    
    
    # action for state in event form
    def action_draft(self):
        self.write({'state':'draft'})
    def action_cancel(self):
        self.write({'state':'cancel'})
    def action_on(self):
        self.write({'state':'onprogress'})
    def action_end(self):
        self.write({'state':'endprogress'})

    # for no. reference of event
    @api.model
    def create (self, vals):
        if vals.get('ref_event', _("New") == _("New")):
            vals['ref_event'] = self.env['ir.sequence'].next_by_code('referensi.event') or _("New")
        record = super(EventDoodex, self).create(vals)
         # Check if the selected date and time is in the past
        selected_datetime = fields.Datetime.from_string(vals.get('date'))
        if selected_datetime and selected_datetime < fields.Datetime.now():
            raise ValidationError(_("Cannot select a date and time in the past."))
        return record

    def write(self, vals):
        # Check if the selected date and time is in the past
        if 'date' in vals:
            selected_datetime = fields.Datetime.from_string(vals['date'])
            if selected_datetime and selected_datetime < fields.Datetime.now():
                raise ValidationError(_("Cannot select a date and time in the past."))

        result = super(EventDoodex, self).write(vals)
        return result
    
    def unlink(self):
        if self.filtered(lambda line:line.state == 'onprogress'):
            raise ValidationError('Cant delete event ongoing!')

        record = super(EventDoodex, self).unlink()
        return record
